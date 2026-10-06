# M3 Step 3 — Turn the screening on · the procedure

> Read this when the leader reaches **M3 Step 3**. `../SKILL.md` and `m3.md` still apply: `m3.md` §3 is the
> change set, §6·5 the allowlist, §5 the resolve lines and the bindings block. **Start every block with the
> resolve lines plus `T=$(gcloud auth print-access-token)`.**
>
> ⛔ **The one acting step, and it does not test.** Make the changes below, each re-read. **No agent call
> this turn**: the replay, the wait and every claim about what the check stops belong to Step 4. Never
> create or delete a gateway, edit the template, or touch the back office's binding or M2's extension and
> policy. **No floor setting.**
>
> ⛔ **Background tasks (`../SKILL.md` §0 rule 11):** the polls run for minutes and often go to the
> background. A checkpoint exists only once "finished with result" arrives and `cat "$W/step3_ids.txt"`
> prints it.

## 1. The order

1. Pre-reads (§2), all saved to `$W`.
2. A service-agent role **only if** the pre-read shows it missing (§3).
3. The authorization extension (§4).
4. The CUSTOM policy, polled until it targets the inbound gateway: **`policy-done <UTC>`** (§5). The policy comes
   before the binding: a gateway with an agent bound and no authorization policy may refuse everything.
5. The binding — the Price Match Agent only — polled until the operation is done **and** the re-read shows
   the inbound gateway on it: **`attach-done <UTC>`** (§6).
6. The inbound gateway's card and the post-change re-reads (§7).
7. One record per change and the undo file (§8); then the answer and the picture (§9).

Every checkpoint goes to `$W/step3_ids.txt` with `tee -a`; `cat` it before writing the entry. COMMANDS copies
each block as it ran (`m3.md` §0); a non-zero block is recorded with its exit code and counted as failed.

## 2. Pre-reads — the before state

```
T=$(gcloud auth print-access-token)
gcloud beta network-services agent-gateways describe novasmart-ingress-gateway --location="$REGION" --format=yaml > "$W/ingress_gw_before.yaml"; echo "describe-exit $?"; grep -E '^(name|createTime|updateTime):|governedAccessPath|agentGatewayCard|serviceExtensionsServiceAccount' "$W/ingress_gw_before.yaml"
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" --filter="bindings.members:(gcp-sa-dep OR gcp-sa-aiplatform-re)" --format="table(bindings.members,bindings.role)" | tee "$W/sa_roles_before.txt"
gcloud beta service-extensions authz-extensions list --location="$REGION" | tee "$W/ext_before.txt"
gcloud beta network-security authz-policies list --location="$REGION" | tee "$W/pol_before.txt"
gcloud projects get-iam-policy "$PROJECT" --format=json > "$W/project_policy_before.json" && echo "project policy saved"
gcloud model-armor templates describe nvst-jailbreak-template --location="$REGION" --format=json > "$W/template_before.json" && echo "template saved"
curl -s -H "Authorization: Bearer $T" "$API" | python3 -c 'import json,sys,hashlib
for e in json.load(sys.stdin).get("reasoningEngines",[]):
    s=e.get("spec",{}); d=s.get("deploymentSpec",{}); g=d.get("agentGatewayConfig") or {}
    fp=hashlib.sha256(json.dumps([s.get("packageSpec"), d.get("env")], sort_keys=True).encode()).hexdigest()[:16]
    print(e["name"].rsplit("/",1)[1], "|", e.get("displayName"), "| inbound:", g.get("clientToAgentConfig","none"), "| outbound:", g.get("agentToAnywhereConfig","none"), "| code+config", fp, "| traffic", json.dumps(e.get("trafficConfig") or s.get("trafficConfig")))' | tee "$W/agents_before.txt"
```

Expect: the inbound gateway present, `CLIENT_TO_AGENT`; the two service agents holding the roles in `m3.md` §6·5; no
agent with an inbound binding and the back office with its outbound one; only M2's `novasmart-iap-ext` and
`novasmart-iap-pol`; the Price Match Agent with all traffic on its latest revision (a binding change is only
allowed then). The `code+config` fingerprint is the before value for §9 row 20.

- **Gateway absent** → a blocker (`m3.md` §6·7): Terraform owns it; never create one.
- **Traffic not all on the latest revision** → stop before the binding; report it as a blocker.
- **`novasmart-ma-ext` or `novasmart-ma-pol` already present** (an earlier attempt) → describe it, say so,
  don't re-create it; record that it pre-existed.

## 3. A missing service-agent role — only then

Compare `sa_roles_before.txt` with `m3.md` §6·5 (i) and (ii). For each role that is **missing**, and only
then, add that one binding and re-read; each is its own change with its own record:

```
gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-dep.iam.gserviceaccount.com" --role="roles/modelarmor.calloutUser" --condition=None --format="value(etag)"
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" --filter="bindings.members:(gcp-sa-dep OR gcp-sa-aiplatform-re)" --format="table(bindings.members,bindings.role)" | tee "$W/sa_roles_after.txt"
```

The example adds one role to (i); change only the member and role to the missing one. Never
`serviceUsageConsumer` on (ii) — the docs do not ask for it. Nothing missing → no grant, and say *"both
service agents already held their roles"*.

## 4. The authorization extension

```
cat > "$W/ma_ext.yaml" <<EOF
name: projects/${PROJECT}/locations/${REGION}/authzExtensions/novasmart-ma-ext
service: modelarmor.${REGION}.rep.googleapis.com
failOpen: true
timeout: 1s
metadata:
  model_armor_settings: '[{"request_template_id":"projects/${PROJECT}/locations/${REGION}/templates/nvst-jailbreak-template","response_template_id":"projects/${PROJECT}/locations/${REGION}/templates/nvst-jailbreak-template"}]'
EOF
cat "$W/ma_ext.yaml"
gcloud beta service-extensions authz-extensions import novasmart-ma-ext --source="$W/ma_ext.yaml" --location="$REGION" --quiet
gcloud beta service-extensions authz-extensions describe novasmart-ma-ext --location="$REGION" --format=yaml | tee "$W/ma_ext_now.yaml"
```

- `service` is the **regional** Model Armor host; `model_armor_settings` is **one JSON string** (the single
  quotes keep it a string in YAML). An object there is accepted and never consulted.
- **`failOpen: true` — say it in the answer:** if the check fails or times out, the message goes through
  unscreened. The docs' sample uses `false`; this lab measured `true` working (2026-08-02). It is a
  remaining risk, never a control.
- The same template screens requests and responses. It looks for manipulation and harmful content, not
  names or emails; say nothing about screening customer data.

## 5. The CUSTOM authorization policy, polled

```
cat > "$W/ma_pol.yaml" <<EOF
name: projects/${PROJECT}/locations/${REGION}/authzPolicies/novasmart-ma-pol
target:
  resources:
  - projects/${PROJECT}/locations/${REGION}/agentGateways/novasmart-ingress-gateway
policyProfile: CONTENT_AUTHZ
action: CUSTOM
customProvider:
  authzExtension:
    resources:
    - projects/${PROJECT}/locations/${REGION}/authzExtensions/novasmart-ma-ext
EOF
cat "$W/ma_pol.yaml"
gcloud beta network-security authz-policies import novasmart-ma-pol --source="$W/ma_pol.yaml" --location="$REGION" --quiet
for i in $(seq 1 12); do gcloud beta network-security authz-policies describe novasmart-ma-pol --location="$REGION" --format=yaml > "$W/ma_pol_now.yaml" 2>&1; grep -q agentGateways "$W/ma_pol_now.yaml" && break; sleep 15; done; echo "reads: $i"; cat "$W/ma_pol_now.yaml"
grep -q 'agentGateways/novasmart-ingress-gateway' "$W/ma_pol_now.yaml" && echo "policy-done $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/step3_ids.txt"
```

The target is **`agentGateways/`**, never `gateways/` (a `gateways/` policy is created and binds nothing).
Creation is asynchronous: an early describe shows `target: {}`, and a second import while it is being
created returns `ABORTED` — poll, never re-import. No `policy-done` after 3 minutes → do not bind; report it
and mark rows 11 and 12 `not verified`.

## 6. The binding — the Price Match Agent only, polled to done

Only after `policy-done` is printed:

```
curl -s -X PATCH -H "Authorization: Bearer $T" -H "Content-Type: application/json" \
  -d '{"spec":{"deploymentSpec":{"agentGatewayConfig":{"clientToAgentConfig":{"agentGateway":"projects/'"$PROJECT"'/locations/'"$REGION"'/agentGateways/novasmart-ingress-gateway"}}}}}' \
  "$API1/<PMA_ID>?updateMask=spec.deploymentSpec.agentGatewayConfig" | tee "$W/attach_op.json"
echo "attach-start $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/step3_ids.txt"
```

If `v1` rejects the field (a 400 naming `agentGatewayConfig`), send the same body once to
`https://${REGION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_NUMBER}/locations/${REGION}/reasoningEngines/<PMA_ID>?updateMask=spec.deploymentSpec.agentGatewayConfig`
(the form M2 measured), as a new numbered command. Then poll and re-read (`v1` below; use `v1beta1` in the
poll URL if that is what accepted the PATCH):

```
OP=$(python3 -c 'import json,sys; n=json.load(open(sys.argv[1])).get("name",""); print(n if "/operations/" in n else "")' "$W/attach_op.json"); echo "operation: ${OP:-none returned}"
for i in $(seq 1 30); do [ -z "$OP" ] && break; curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://${REGION}-aiplatform.googleapis.com/v1/$OP" > "$W/attach_op_now.json"; python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("done") else 1)' "$W/attach_op_now.json" && break; sleep 20; done; echo "reads: $i"; [ -n "$OP" ] && cat "$W/attach_op_now.json"
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" "$API" | python3 -c 'import json,sys
for e in json.load(sys.stdin).get("reasoningEngines",[]):
    g=e.get("spec",{}).get("deploymentSpec",{}).get("agentGatewayConfig") or {}
    print(e["name"].rsplit("/",1)[1], "|", e.get("displayName"), "| inbound:", g.get("clientToAgentConfig","none"), "| outbound:", g.get("agentToAnywhereConfig","none"))' | tee "$W/attach_reread.txt"
{ [ -z "$OP" ] || python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get("done") and not d.get("error") else 1)' "$W/attach_op_now.json"; } && grep '<PMA_ID>' "$W/attach_reread.txt" | grep -q 'novasmart-ingress-gateway' && echo "attach-done $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/step3_ids.txt"
cat "$W/step3_ids.txt"
```

- **`attach-done` needs both:** the operation done with no `error` (or none returned), **and** the re-read
  showing `novasmart-ingress-gateway` as the Price Match Agent's inbound binding. The back office must still
  show its outbound binding and the website agent none.
- Not done after 10 minutes → row 12 is `not verified`, said in the answer; the binding is **not
  confirmed**, and nothing claims the agent is behind the inbound gateway.
- The binding redeploys the agent and **archives every earlier revision for good** (`m3.md` §1): say so in
  the answer and in the record.

## 7. After the binding — the inbound gateway's card

```
gcloud beta network-services agent-gateways describe novasmart-ingress-gateway --location="$REGION" --format=yaml > "$W/ingress_gw_after.yaml"; grep -iE 'agentGatewayCard|serviceExtensionsServiceAccount' "$W/ingress_gw_after.yaml" || echo "no card shown"
echo "expected: service-${PROJECT_NUMBER}@gcp-sa-dep.iam.gserviceaccount.com"
```

The card names the account the inbound gateway calls Model Armor as (the outbound gateway's card named another
project's account in one lab). The same account as expected → say so. Another account → a finding (`m3.md`
§6·5): with `failOpen: true` the check may never run, and Step 4 would show it. No card → *"not shown"*, row
9 says so.

## 8. Records and the undo

One record per change, in the order made: `Change:` · `Resource:` · `When:` · `Undo:` (`../SKILL.md` §3g) —
the extension, the policy, the binding, and any service-agent role. The binding's `Change:` line adds:
*"the platform archived the agent's earlier revisions; no undo restores them."*

Write the undo with **literal values** (no variable a fresh shell lacks) to `$W/undo_step3.sh`, run
`bash -n "$W/undo_step3.sh"`, and record both. Order: detach first (a bound agent with no policy may refuse
everything), then the policy, then the extension:

```
# 1 detach the Price Match agent - restores the routing, not the archived revisions (body not in the docs; not exercised here)
curl -s -X PATCH -H "Authorization: Bearer $(gcloud auth print-access-token)" -H 'Content-Type: application/json' -d '{"spec":{"deploymentSpec":{}}}' 'https://<REGION>-aiplatform.googleapis.com/v1/projects/<PROJECT>/locations/<REGION>/reasoningEngines/<PMA_ID>?updateMask=spec.deploymentSpec.agentGatewayConfig'
# 2 the policy, then the extension
gcloud beta network-security authz-policies delete novasmart-ma-pol --location='<REGION>' --quiet
gcloud beta service-extensions authz-extensions delete novasmart-ma-ext --location='<REGION>' --quiet
# 3 only for a service-agent role this step added
gcloud projects remove-iam-policy-binding '<PROJECT>' --member='serviceAccount:service-<PROJECT_NUMBER>@gcp-sa-dep.iam.gserviceaccount.com' --role='<ROLE>' --condition=None --format='value(etag)'
```

Never in the undo: the inbound gateway, the template, the back office or anything M2 made.

## 9. The answer and the picture

- **Bold line — the configuration, not the coverage**, and only after `attach-done`: *"messages sent to the
  Price Match Agent now pass through a content check on the inbound gateway before the agent sees them."*
  Whether it stops anything is Step 4's question.
- **Disclose every change**, one plain line each, and each grant you did or did not need.
- `### Why this matters`: one agent — the website agent and the back office are reached over a protocol
  this check does not read (`m3.md` §1); `failOpen: true` as a remaining risk; the archived revisions; the
  check looks for manipulation and harmful content, not names or emails; the binding takes about five
  minutes, and Step 4 waits it out. The inbound gateway's card as §7 found it.
- **The picture — REQUIRED, BEFORE/AFTER on SCREEN**, built only after the re-read: BEFORE (`agents_before.txt`)
  the client reaching the Price Match Agent with nothing between; AFTER (`attach_reread.txt`) the inbound
  gateway carrying the template in front of it, *messages checked here before the agent sees them*; the other
  two agents in both halves, unchanged, nothing in front of them, the back office's outbound binding drawn as
  read and labelled *where it may reach (M2)*. Caption: which half came from which read, and when. An
  unconfirmed binding is drawn *binding not confirmed*. No refusal, no tick.

## 10. Don't mislabel

- The PATCH reply, a `200` or an operation name is not the binding: the re-read is.
- *"Attacks are now blocked"*, *"protected"*, *"screened"* as an outcome — Step 4's, after a reply is read.
- Never *your agents*, *every agent*, *the estate*; never offer the outbound path for the other two.
- A failed or rejected command is in the file and named in the answer, never described as in place.
- `failOpen: true` is never described as a safety feature.

## 11. How to close

`m3.md` §2 Close check, row 3. Questions about the gap: what would tell NovaSmart that this check had quietly
stopped running, who owns the decision to leave it fail-open, what the other two agents would need before
they faced customers alone.
