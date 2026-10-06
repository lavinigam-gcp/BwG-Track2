# M2 Step 5 — Lock down what the back office can reach and do · the procedure

> Read this when the leader reaches **M2 Step 5**. `../SKILL.md` and `m2.md` still apply: `m2.md` §3 item 2
> is the change set, §6·5 the allowlist, §9 the 26 rows, §5 the resolve lines. **Start every block with the
> resolve lines plus the first two lines of §3.1** (`T`, and `MSA_P` = the back office's badge).
>
> ⛔ **Step 5 acts, then verifies.** Make the changes in §3, each re-read. Then run the proof (§4). From the
> first proof call on, nothing in the estate is written except the scorecard; a failing row is reported,
> never repaired this turn. **No DENY policy of any kind.** Never attach another agent; never run
> `grant_agent_egress.py`.
>
> ⛔ **Background tasks (`../SKILL.md` §0 rule 11):** the polls, the waits and the log reads here often run
> long and go to the background. Their output exists only once "finished with result" arrives: await it.
> No entry line, table row, picture or answer is written from a task that has not finished.

## 1. Two controls, two questions — never conflated

- **The egress gateway** decides **where** the back office may go. An allow from it says the back office
  may reach BigQuery; it says nothing about changing data there.
- **The back office's own BigQuery permissions** decide **what** it may do there. Today it holds project
  `bigquery.admin`, so a change it attempts succeeds until the narrowing lands.
- Agent Gateway documents tool-level MCP rules; this lab does not use them. Never say the gateway is
  unable to see a request; say it is not what draws the read/write line here.

## 2. The order

1. Pre-reads (§3.1), all saved to `$W`.
2. Authz extension (§3.2) → CUSTOM authz policy (§3.3), polled until it targets the gateway: the poll prints
   **`policy-done <UTC>`**. An attached gateway with no authz policy denies everything the agent sends.
3. Registry-wide `iap.egressor`, etag first (§3.4).
4. Start the attach (§3.5) — **only after `policy-done` is printed**. While its operation runs (about four
   minutes), do the narrowing (§3.6). Note the UTC time of the last IAM change.
5. Poll the attach until `done: true`, then re-read every agent's `agentGatewayConfig`: the block prints
   **`attach-done <UTC>`** only when both hold (§3.5).
6. The wait (§3.7) prints **`wait-done <UTC>`**, at least 3 minutes after the last IAM change.
7. The proof (§4) opens with **`T0 <UTC>`**, saved to `$W/proof_ids.txt` with every later proof checkpoint;
   then the records (§5, which opens by reading that file back), the table and the scorecard (§7).

**The gate before the proof is checkable:** `policy-done`, `attach-done` and `wait-done` each appear in
this turn's OUTPUTS with a UTC time **earlier than `T0`**. A proof call made before all three does not count
for rows 18–21: say so, and make the proof calls again (they are calls, not changes). Missing a checkpoint
(the attach never finished) → rows 14 and 18–21 are `not verified`.

Write each change's record as you go: `Change:` · `Resource:` · `When:` · `Undo:` (§6), one block per
change. Keep every yaml and JSON in `$W`, never in `Session1`.

⛔ **The entry records what ran and what you saw — not a tidy version of it** (`../SKILL.md` §3):
- **COMMANDS copies each block exactly as it ran**: the resolve lines, `$(date …)`, loops and `sleep` stay
  as written. Never replace an expression with the value it printed, and never collapse a poll loop to one
  call.
- **A block that exited non-zero is recorded** with its exit code; its re-run is the next numbered
  command. `### Where the proof is` counts it as failed.
- **Every checkpoint, `T0`, messageId and reply in OUTPUTS was printed by a command you read.** A long
  output loses its head on screen. When that happens, read the value back from its file (§5 (0)). Never
  fill it in from timing, the request you sent or memory.

## 3. The changes

### 3.1 Pre-reads

```
T=$(gcloud auth print-access-token)
EI=$(curl -s -H "Authorization: Bearer $T" "$API/<MSA_ID>" | python3 -c 'import json,sys; print(json.load(sys.stdin)["spec"]["effectiveIdentity"])'); MSA_P="principal://${EI#principal://}"; echo "badge: $MSA_P"
curl -s -H "Authorization: Bearer $T" "$API/<MSA_ID>" | python3 -c 'import json,sys; s=json.load(sys.stdin)["spec"]; print(s.get("identityType"), s.get("effectiveIdentity"), s.get("deploymentSpec",{}).get("agentGatewayConfig"))'
gcloud beta network-services agent-gateways list --location="$REGION"
gcloud beta service-extensions authz-extensions list --location="$REGION"
gcloud beta network-security authz-policies list --location="$REGION"
curl -s -X POST -H "Authorization: Bearer $T" -H "Content-Type: application/json" -d '{}' \
  "https://iap.googleapis.com/v1/projects/${PROJECT_NUMBER}/locations/global/iap_web/agentRegistry:getIamPolicy" | tee "$W/iap_policy_before.json"
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" --filter="bindings.members:$MSA_P" --format="table(bindings.role)"
for DS in novasmart_pricing competitor_data; do bq show --format=prettyjson "$PROJECT:$DS" > "$W/ds_${DS}_before.json" && echo "saved $DS"; done
bq show --format=json "$PROJECT:novasmart_pricing.wholesale_costs" | python3 -c 'import json,sys; t=json.load(sys.stdin); print("lastModifiedTime", t["lastModifiedTime"], "numRows", t["numRows"])'
```

Expect `AGENT_IDENTITY` (a `400 FAILED_PRECONDITION` on the attach means it is not — M1's work, not this
step's), `agentGatewayConfig` `None`, two gateways, no authz policy. The last line is the **before** ground
truth for row 20. Anything already present from an earlier attempt: describe it; don't re-create it.

### 3.2 The authz extension

```
cat > "$W/ext.yaml" <<EOF
name: projects/${PROJECT}/locations/${REGION}/authzExtensions/novasmart-iap-ext
service: iap.googleapis.com
failOpen: true
timeout: 1s
metadata:
  iapPolicyVersion: "V1"
EOF
gcloud beta service-extensions authz-extensions import novasmart-iap-ext --source="$W/ext.yaml" --location="$REGION" --quiet
gcloud beta service-extensions authz-extensions describe novasmart-iap-ext --location="$REGION"
```

**`failOpen: true` — say it in the answer:** if the IAP check fails or times out, traffic is let through.
The documented setting is `false`; this lab measured `V1` with `true` working (2026-08). State that as a
remaining risk, never as a control.

### 3.3 The CUSTOM authz policy on the egress gateway

```
cat > "$W/pol.yaml" <<EOF
name: projects/${PROJECT}/locations/${REGION}/authzPolicies/novasmart-iap-pol
target:
  resources:
  - projects/${PROJECT}/locations/${REGION}/agentGateways/novasmart-egress-gateway
policyProfile: REQUEST_AUTHZ
action: CUSTOM
customProvider:
  authzExtension:
    resources:
    - projects/${PROJECT}/locations/${REGION}/authzExtensions/novasmart-iap-ext
EOF
gcloud beta network-security authz-policies import novasmart-iap-pol --source="$W/pol.yaml" --location="$REGION" --quiet
for i in $(seq 1 12); do gcloud beta network-security authz-policies describe novasmart-iap-pol --location="$REGION" --format=yaml > "$W/pol_now.yaml" 2>&1; grep -q agentGateways "$W/pol_now.yaml" && break; sleep 15; done; echo "reads: $i"; cat "$W/pol_now.yaml"
grep -q agentGateways "$W/pol_now.yaml" && echo "policy-done $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Creation is asynchronous: an early describe shows `target: {}`, and a second import while it is being
created returns `ABORTED`. Poll; never re-import. The import may take 2–3 minutes.

### 3.4 `roles/iap.egressor`, registry-wide — read with its etag first

```
python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); m=sys.argv[2]; b=p.get("bindings",[]); e=[x for x in b if x["role"]=="roles/iap.egressor" and "condition" not in x]; (e[0]["members"].append(m) if m not in e[0]["members"] else None) if e else b.append({"role":"roles/iap.egressor","members":[m]}); print(json.dumps({"policy":{"version":p.get("version",1),"etag":p["etag"],"bindings":b}}))' "$W/iap_policy_before.json" "$MSA_P" > "$W/iap_policy_new.json"
cat "$W/iap_policy_new.json"
curl -s -X POST -H "Authorization: Bearer $T" -H "Content-Type: application/json" -d @"$W/iap_policy_new.json" \
  "https://iap.googleapis.com/v1/projects/${PROJECT_NUMBER}/locations/global/iap_web/agentRegistry:setIamPolicy"
curl -s -X POST -H "Authorization: Bearer $T" -H "Content-Type: application/json" -d '{}' \
  "https://iap.googleapis.com/v1/projects/${PROJECT_NUMBER}/locations/global/iap_web/agentRegistry:getIamPolicy"
```

The new policy is built from the read and carries its `etag`, so every existing binding survives. **Global
and registry-wide:** Google's managed MCP servers and endpoints sit in the global registry, and a
per-resource grant would replace this one for that resource, stranding everything else the agent reaches.

### 3.5 The attach — the back office only, polled to done

```
curl -s -X PATCH -H "Authorization: Bearer $T" -H "Content-Type: application/json" \
  -d '{"spec":{"deploymentSpec":{"agentGatewayConfig":{"agentToAnywhereConfig":{"agentGateway":"projects/'"$PROJECT"'/locations/'"$REGION"'/agentGateways/novasmart-egress-gateway"}}}}}' \
  "https://${REGION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_NUMBER}/locations/${REGION}/reasoningEngines/<MSA_ID>?updateMask=spec.deploymentSpec.agentGatewayConfig" | tee "$W/attach_op.json"
```

After the narrowing, poll it (a `done` field appears only when it finishes) and re-read:

```
OP=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["name"])' "$W/attach_op.json")
for i in $(seq 1 30); do curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://${REGION}-aiplatform.googleapis.com/v1beta1/$OP" > "$W/attach_op_now.json"; python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("done") else 1)' "$W/attach_op_now.json" && break; sleep 20; done; echo "reads: $i"; cat "$W/attach_op_now.json"
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" "$API" | python3 -c 'import json,sys; [print(e["displayName"], "|", e.get("spec",{}).get("deploymentSpec",{}).get("agentGatewayConfig")) for e in json.load(sys.stdin).get("reasoningEngines",[])]' | tee "$W/attach_reread.txt"
python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("done") else 1)' "$W/attach_op_now.json" && grep -q novasmart-egress-gateway "$W/attach_reread.txt" && echo "attach-done $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

`done: true` with no `error`, then the back office showing `novasmart-egress-gateway` and every other agent
`None`. Not done after 10 minutes → row 14 `not verified`, said in the answer; the attach is then **not
confirmed**, and nothing claims the back office is behind the gateway. The attach redeploys the agent: its
next call starts a fresh instance.

### 3.6 The narrowing — remove and grant back in one change

```
gcloud projects remove-iam-policy-binding "$PROJECT" --member="$MSA_P" --role=roles/bigquery.admin --quiet --format="value(etag)"
gcloud projects add-iam-policy-binding "$PROJECT" --member="$MSA_P" --role=roles/bigquery.jobUser --quiet --format="value(etag)"
for DS in novasmart_pricing competitor_data; do python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["access"].append({"role":"READER","iamMember":sys.argv[2]}); print(json.dumps(d))' "$W/ds_${DS}_before.json" "$MSA_P" > "$W/ds_${DS}_new.json" && bq update --source "$W/ds_${DS}_new.json" "$PROJECT:$DS"; done
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" --filter="bindings.members:$MSA_P" --format="table(bindings.role)"
for DS in novasmart_pricing competitor_data; do echo "== $DS"; bq show --format=prettyjson "$PROJECT:$DS" | grep -B1 -A1 "reasoningEngines/<MSA_ID>"; done
```

- `jobUser` lets a query run and reads nothing; the dataset `READER` entries are the reads. Without both,
  the agent is stranded and answers from its instruction instead of saying so.
- `bq update --source` replaces the whole `access[]`: the new file is the read plus one entry, so every
  other entry (yours included) survives. Read both datasets back.
- `mcp.toolUser` and `aiplatform.user` stay: the back office keeps its tool and model access.

### 3.7 The wait — at least 3 minutes after the last IAM change

```
LAST="<UTC of the last IAM change>"; S=$(( 180 - ( $(date -u +%s) - $(date -u -d "$LAST" +%s) ) )); [ "$S" -gt 0 ] && sleep "$S"; echo "wait-done $(date -u +%Y-%m-%dT%H:%M:%SZ) last-IAM-change $LAST"
```

State the wait in the answer with its length. IAM can take 7 minutes or more: a proof that still shows the
old behavior is retried once after another wait, never reported as the result.

## 4. The proof — after `policy-done`, `attach-done` and `wait-done`

`T0` is the first line of the proof block and must be later than all three checkpoints (§2). Call the back
office **directly with your own token**, and say in the answer that this
works because your login holds a project-wide role that carries the ability to call any agent (read it:
the project policy filtered on `antigravity-sa`, row 26's read). Never present this route as the business
path.

```
T0=$(date -u +%Y-%m-%dT%H:%M:%SZ); RID="m2-read-$(date +%s)"; echo "T0 $T0 read-id $RID" | tee "$W/proof_ids.txt"
curl -sS -N -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "$API/<MSA_ID>/a2a/v1/message:stream" \
  -d '{"request":{"messageId":"'"$RID"'","role":"ROLE_USER","content":[{"text":"What is the margin floor and wholesale cost for SKU-HSE-4001?"}]}}' > "$W/proof_read.txt"; echo "read-exit $?" | tee -a "$W/proof_ids.txt"
CID="m2-change-$(date +%s)"; echo "change-start $(date -u +%Y-%m-%dT%H:%M:%SZ) change-id $CID" | tee -a "$W/proof_ids.txt"
curl -sS -N -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "$API/<MSA_ID>/a2a/v1/message:stream" \
  -d '{"request":{"messageId":"'"$CID"'","role":"ROLE_USER","content":[{"text":"Permanently drop the floor price for SKU-HSE-4001 to 50."}]}}' > "$W/proof_change.txt"; echo "change-exit $?" | tee -a "$W/proof_ids.txt"
echo "change-call-done $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/proof_ids.txt"
```

- The streams go to files, not the screen: §5 (0) prints from them each request's messageId and task,
  every tool call with its SQL, each result's `isError`, the reply and the final state. Expect
  `execute_sql_readonly` for the read and `execute_sql` with an `UPDATE` for the change. **Margin values
  stay in the file** — no dollar cost or floor on screen, in the picture or in the scorecard proof; on
  screen, *"it returned the cost and floor"*.
- A 429 or an empty answer (§5 (0) prints `no stream events`) → wait a minute, retry once; then the row is
  `not verified`.
- **The agent's reply is not the proof.** Entries reach the logs minutes late: after `change-call-done`,
  wait and state it, then read the platform's records (§5) — never sooner:

```
sleep 180; echo "records-wait-done $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/proof_ids.txt"
```

  A record read that ran before `records-wait-done` and misses an entry is re-run after the wait; it is
  never reported as an absence.

## 5. The records — each stated exactly as far as it goes

**(0) What the proof printed — read it back first.** Every proof value in the entry and the answer
(`T0`, the checkpoints, the messageIds, each tool call and its SQL, `isError`, the reply, the final
state) is copied from this output:

```
cat "$W/proof_ids.txt"
for F in proof_read proof_change; do echo "== $F"; python3 -c '
import json,re,sys
t=open(sys.argv[1]).read(); ev=[]
for b in t.split("\n\n"):
    if b.strip().startswith("data:"):
        try: ev.append(json.loads(re.sub(r"(?m)^data: ?","",b)))
        except ValueError: print("unparsed event")
if not ev: print("no stream events:", t[:300]); sys.exit(1)
for e in ev:
    u=e.get("statusUpdate",{}); s=u.get("status",{}); m=s.get("message",{})
    if m.get("role")=="ROLE_USER": print("request", m.get("messageId"), "task", u.get("taskId"))
    for p in m.get("content",[]):
        d=p.get("data",{}).get("data",{})
        if "args" in d: print("call", d.get("name"), d["args"].get("query",""))
        if "response" in d: r=d["response"]; print("result", d.get("name"), "isError", r.get("isError", False), (r.get("content") or [{}])[0].get("text","")[:160] if r.get("isError") else "")
    for p in e.get("artifactUpdate",{}).get("artifact",{}).get("parts",[]): print("answer", p.get("text"))
    if u.get("final"): print("state", s.get("state"))
' "$W/$F.txt"; done
```

The record reads below take `T0` from the same file (the first line of each block), so it is never
typed.

**(a) BigQuery audit, under the back office's badge** (BigQuery records data access by default):

```
T0=$(awk '/^T0 /{print $2}' "$W/proof_ids.txt"); echo "T0 $T0"
gcloud logging read 'protoPayload.serviceName="bigquery.googleapis.com" AND protoPayload.authenticationInfo.principalSubject:"reasoningEngines/<MSA_ID>" AND timestamp>="'"$T0"'"' \
  --freshness=30m --order=asc --format="table(timestamp,protoPayload.methodName,severity,protoPayload.status.code,protoPayload.status.message)"
gcloud logging read 'protoPayload.serviceName="bigquery.googleapis.com" AND protoPayload.authenticationInfo.principalSubject:"reasoningEngines/<MSA_ID>" AND protoPayload.status.code=7 AND protoPayload.methodName="jobservice.jobcompleted" AND timestamp>="'"$T0"'"' \
  --freshness=30m --limit=1 --format=json
```

The read: `jobservice.query`, `JobService.Query` and `jobservice.jobcompleted` with no status (row 18). The
refusal: the same methods with `status.code: 7`; quote the message, e.g. *"Permission
bigquery.tables.updateData denied on table …wholesale_costs"*, and the `UPDATE` text from
`metadata.jobChange.job.jobConfig.queryConfig.query` (row 19). The identity is
`authenticationInfo.principalSubject` — there is no `principalEmail` for an agent badge. The job's own
`bigquery.jobs.create` shows **granted** (that is `jobUser`); the refused permission is only in the message.

**(b) The table did not change** (row 20): re-run the §3.1 `bq show … wholesale_costs` line. Same
`lastModifiedTime` as before → no change landed. You cannot query the table yourself (`m2.md` §1), so this metadata
is your ground truth.

**(c) The gateway's verdict** (row 21):

```
T0=$(awk '/^T0 /{print $2}' "$W/proof_ids.txt"); echo "T0 $T0"
gcloud logging read 'logName:"networkservices.googleapis.com%2Fgateway_requests" AND resource.type="networkservices.googleapis.com/Gateway" AND httpRequest.requestUrl:"bigquery" AND timestamp>="'"$T0"'"' \
  --freshness=1h --order=asc --format="table(timestamp,httpRequest.requestUrl,httpRequest.status,jsonPayload.agentGatewayInfo.mcpInfo.method,jsonPayload.authzPolicyInfo.result)"
```

Entries are `https://bigquery.googleapis.com/mcp` with a method — the session setup (`initialize`,
`notifications/initialized`, `tools/list`) and, after a lag, the tool calls (`tools/call`) — each with a
verdict such as `ALLOWED`. Which ones appear varies between runs. **Row 21 quotes only entries that appear
in this turn's actual output of this command, each with a timestamp at or after `T0`** — copied, never
retyped or expected. The query returned nothing at or after `T0` (or did not finish) → row 21 is `not verified`, the
scorecard is `FAIL`, and the answer and picture state no gateway verdict. An entry from before `T0` (an
earlier run, the attach's startup) never fills the row. When entries do come back, **name the methods
this output lists, and nothing more**: e.g. *"the gateway allowed the back office's BigQuery session setup
and one tool call at <its time>"* only if those rows are there. A `tools/call` is tied to the read or the
change only by its timestamp against BigQuery's entry; say so, and never claim one that is not listed. The
entries carry **no caller identity** (they are the back office's by timing and because it is the only
attached agent). The refusal is BigQuery's, never the gateway's. With no `DENIED` entry, never say the
gateway blocks or prevents anything.

**(d) Your own calls** (disclosure) — your login, `reasoningEngines.query` granted:

```
T0=$(awk '/^T0 /{print $2}' "$W/proof_ids.txt"); echo "T0 $T0"
gcloud logging read 'protoPayload.serviceName="aiplatform.googleapis.com" AND protoPayload.resourceName:"reasoningEngines/<MSA_ID>" AND timestamp>="'"$T0"'"' --freshness=30m --format="table(timestamp,protoPayload.methodName,protoPayload.authenticationInfo.principalEmail,protoPayload.authorizationInfo[0].granted)"
```

**(e) The change set** (row 24) and **self-grant** (row 26):

```
gcloud projects get-iam-policy "$PROJECT" --format=json > "$W/project_policy_step5.json"
python3 -c 'import json,sys; P=lambda f:{(b["role"],m) for b in json.load(open(f)).get("bindings",[]) for m in b["members"]}; a,b=P(sys.argv[1]),P(sys.argv[2]); [print("REMOVED",*x) for x in sorted(a-b)]; [print("ADDED",*x) for x in sorted(b-a)]' "$W/project_policy_step1.json" "$W/project_policy_step5.json"
```

Expected: `REMOVED roles/bigquery.admin` and `ADDED roles/bigquery.jobUser` on the back office's badge. The
platform may add `roles/networksecurity.authzServiceAgent` for its own network-security service agent when
the authz policy is created: name it as made by the platform, not by you. Anything else, or any line naming
`antigravity-sa` → the row shows it. No Step 1 snapshot → say so; the row is `not verified`.

**Row 11, if Step 4 left it `not verified`:** you may run the escalation once more now (a call, not a
change) and use that result, labelled with this turn's time; it counts only if the back office's decision
comes back (`m2-step4.md` §4):

```
curl -sS -N -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  "https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT}/locations/${REGION}/reasoningEngines/<PMA_ID>:streamQuery?alt=sse" \
  -d '{"class_method":"stream_query","input":{"message":"A customer asks us to match BetaBuy at $296.65 for SKU-HSE-4001 (our shelf price $349.00). Approve or decline?","user_id":"m2-check"}}' | tee "$W/escalation_step5.txt"
```

## 6. Undo lines — literal values, checked with `bash -n`

Write each undo with literal values (no shell variables a fresh shell lacks) to `$W/undo_step5.sh`, run
`bash -n "$W/undo_step5.sh"` and record both. One `Undo:` per change record:

```
# authz policy, then extension
gcloud beta network-security authz-policies delete novasmart-iap-pol --location=<REGION> --quiet
gcloud beta service-extensions authz-extensions delete novasmart-iap-ext --location=<REGION> --quiet
# registry egressor: restore the saved bindings with a fresh etag
T=$(gcloud auth print-access-token); U='https://iap.googleapis.com/v1/projects/<PROJECT_NUMBER>/locations/global/iap_web/agentRegistry'; curl -s -X POST -H "Authorization: Bearer $T" -H 'Content-Type: application/json' -d '{}' "$U:getIamPolicy" > /tmp/m2_now.json && python3 -c 'import json,sys; b=json.load(open(sys.argv[1])); n=json.load(open(sys.argv[2])); print(json.dumps({"policy":{"version":b.get("version",1),"etag":n["etag"],"bindings":b.get("bindings",[])}}))' /config/Desktop/novasmart-evidence/m2/work/iap_policy_before.json /tmp/m2_now.json > /tmp/m2_undo.json && curl -s -X POST -H "Authorization: Bearer $T" -H 'Content-Type: application/json' -d @/tmp/m2_undo.json "$U:setIamPolicy"
# attach (update mask with the field absent clears it; not exercised in this lab - say so)
curl -s -X PATCH -H "Authorization: Bearer $(gcloud auth print-access-token)" -H 'Content-Type: application/json' -d '{"spec":{"deploymentSpec":{}}}' 'https://<REGION>-aiplatform.googleapis.com/v1beta1/projects/<PROJECT_NUMBER>/locations/<REGION>/reasoningEngines/<MSA_ID>?updateMask=spec.deploymentSpec.agentGatewayConfig'
# BigQuery: admin back first, then jobUser off, then the two READER entries
gcloud projects add-iam-policy-binding <PROJECT> --member='<MSA_BADGE>' --role=roles/bigquery.admin --quiet --format='value(etag)' && gcloud projects remove-iam-policy-binding <PROJECT> --member='<MSA_BADGE>' --role=roles/bigquery.jobUser --quiet --format='value(etag)'
for DS in novasmart_pricing competitor_data; do bq show --format=prettyjson "<PROJECT>:$DS" > /tmp/m2_ds.json && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["access"]=[a for a in d["access"] if a.get("iamMember")!=sys.argv[2]]; print(json.dumps(d))' /tmp/m2_ds.json '<MSA_BADGE>' > /tmp/m2_ds_undo.json && bq update --source /tmp/m2_ds_undo.json "<PROJECT>:$DS"; done
```

## 7. The answer, the table and the scorecard

- **Bold line first**: what is now true about where the back office may go and what it may change, as far
  as the records showed. Disclose every change, one plain line each, and your direct call and the role
  that allowed it.
- `### Why this matters`: the two controls, each with its evidence — the gateway's `ALLOWED` on the MCP
  session only if row 21 holds post-`T0` entries (the methods it lists, no caller named), otherwise *"no
  gateway verdict was recorded after the proof started"*; the read answered; the change refused in BigQuery's own
  record under the back office's badge; the table's last-modified time unchanged. Then what each does
  **not** cover: other principals can still change the pricing data (re-read who holds project
  `bigquery.admin` if you say who); `failOpen: true` beside any gateway claim; the project-wide callers.
  Roles in plain words on screen (*change every table*, *run queries*, *read two datasets*).
- **The picture — REQUIRED, BEFORE/AFTER on REACH, two distinct controls drawn as two distinct things.**
  **Where it may reach:** BEFORE (§3.1) the back office with no gateway attached; AFTER the back office →
  `novasmart-egress-gateway` → BigQuery, `may reach`, labelled with the allowed methods row 21 lists (e.g.
  *session setup allowed*), otherwise *no verdict recorded*. **What it may do:** BEFORE *change every table in the project*; AFTER *run queries ·
  read two datasets*, with the refused change drawn only because you observed it in the audit log. AFTER
  only from this turn's re-reads and observed results; an unconfirmed attach is drawn *attach not
  confirmed*. No pass/fail marks; nothing joins the two controls into one. Caption: what was read, from
  where, when.
- **The table:** all 26 rows of `m2.md` §9 into `m2_step5.txt` after OUTPUTS. **Rows 1–13 are read back,
  never retyped:** run this and record it as a command, then copy each event row's Result from its output;
  re-read the state rows (8, 13) live:

```
awk '/^ENTRY /{b=""} {b=b $0 "\n"} END{printf "%s", b}' /config/Desktop/novasmart-evidence/m2/m2_step4.txt | grep -E '^\| *([1-9]|1[0-3]) \|'
```

  Rows 14–26 come only from this turn's outputs. On screen, `### What I checked` is one line: *"25 of the
  26 checks are evidenced live; 1 is not verified."*, counted off the rows written.
- **The scorecard — every time, pass or fail**, last:

```
python3 /config/Desktop/Session1/.agents/skills/novasmart-governance-lab/scripts/update_scorecard.py \
  --mission M2 --status <PASS or FAIL> --checks-json '[{"name":"<§9 check>","proof":"<value quoted this turn>"}]'
```

  `--status` follows the table: `PASS` only when all 26 rows are evidenced live and every one shows the
  control holding. **`FAIL` when any row is `not verified`, shows a control not holding, or rests on output
  that did not come back this turn** (a background task not awaited, a value no command printed) — that
  row is counted `not verified` in the coverage line too. The status must agree with the coverage line.
  One object per row; no single quote inside any value. **Run this command directly in the shell, exactly
  as written** — never through a `python3`/`subprocess` wrapper or a script file — and record that same
  command line, with its real `--checks-json`, and its output in the entry. **PASS:** one plain line of
  achievement. **FAIL:** name the failing row and the step to return to (rows 1–5 → Step 1; 6–8 → Step 3;
  9–13 → Step 4; 14–26 → this step, in a later turn once the cause is fixed). **Always** print:
  `📊 **Live Scorecard:** [http://localhost:8088/governance_scorecard.html](http://localhost:8088/governance_scorecard.html)`
- `### Where the proof is`: `m2_step5.txt`, its command count and failures (every non-zero exit this turn,
  re-runs included), the undo clause.

## 8. Don't mislabel

- The agent's own reply is never evidence of a refusal or of a read.
- A configuration re-read is not a refusal; a refusal is drawn and claimed only from the audit entry.
- The gateway did not stop the change, and the BigQuery permissions do not decide where the agent may go.
- "Attached only to the back office" is not "all its traffic goes through the gateway"; never *exclusively*,
  *governs all outbound*, *prevents*, *actively authorizes*.
- "Read-only" always carries *for the back office*.
- A failed or rejected command is in the file and named in the answer, never described as in place.
- Don't attach other agents, add a DENY policy, or "tidy" any other binding you saw.

## 9. How to close

`m2.md` §2 Close check, row 5. Questions about the gap each control leaves: who else can still change the
pricing data, what a gateway record without a caller name is worth to an auditor, what the next agent would
need before it holds something as sensitive.
