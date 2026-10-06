# M3 · Protect the Content — Skill Mapping

*Read this after you finish Module 3. It explains what each prompt was for, so it gives away the module's findings.*

No test run of this version of Module 3 has finished yet, so this guide describes what the skill requires at each step, not what agy did; your own run is the evidence. Commands are copied from the skill files with placeholders such as `<PROJECT>`, and each "What to expect" row quotes the Instructions tab. Only Step 3 changes the project: it adds a Model Armor check (Google Cloud's screen for what is sent to and from an AI) to the inbound gateway and puts one agent, the Price Match Agent, behind it.

## What you learned

<!-- FIGURE:S3_01 BEGIN -->

![One prompt, start to finish: a swimlane with five lanes: You, agy, Skill files, Google Cloud, Evidence file. Your plain-English question goes to agy, which sees the skill name and description, reads skill files when needed, runs only what this step allows on Google Cloud, and writes m3_stepN.txt from outputs read back; an arrow then rises to the answer, built only from this file. A strip below reads: Model sign-in: Google account or API key; Cloud commands run as antigravity-sa.](images/S3_01_one_turn_swimlane.webp)

<!-- FIGURE:S3_01 END -->

The prompts are a leader's questions; the skill turns each one into calls, reads and a file. One thing differs from Module 2: every value agy quotes is printed from a saved file by a read-back command. Checkpoints such as `attach-done` are written to a file with `tee -a` and printed with `cat`, never typed.

The skill adds `references/m3.md`, read whole at the first prompt, plus `m3-step1.md` (Steps 1 and 4), `m3-step3.md`, `m3-step4.md`, `showcase.md` and `showcase-m3.md`, each read at its step. Each stays under about 44 KB so agy reads it in one call.

## Does the skill know the answers? Yes.

<!-- FIGURE:S3_02 BEGIN -->

![When each change may happen: five columns, one per step, each with a product chip and a card. Step 1, Attack, Agent Runtime: four real calls; changes nothing. Step 2, Look, Model Armor: reads only; changes nothing. Step 3, Screen, Agent Gateway plus Model Armor, the only green card: three changes, one agent. Step 4, Replay, Agent Runtime: same four calls, then the scorecard. Step 5, Sum up, Agent Gateway: re-reads only; changes nothing. A band below reads: Is told to say only what its own re-read showed.](images/S3_02_when_each_change_may_happen.webp)

<!-- FIGURE:S3_02 END -->

`references/m3.md` describes the estate Module 3 expects, so agy knows where to look: a written backdoor rule in the Price Match Agent, a content filter wired to nothing, and a screen that can reach one agent only. Green marks the one step that changes the project. Four rules keep it from reciting or overreaching:

- **Each step has limits.** A table says what each step may report and change. Step 2 may not even say where a screen would sit.
- **A scope fence.** Three changes for one agent: the extension `novasmart-ma-ext`, the policy `novasmart-ma-pol` and the Price Match Agent's inbound binding, plus a service-agent role only if a re-read shows it missing. M2's outbound binding on the back office stays untouched.
- **No floor setting.** The project-wide Model Armor setting is banned in every step, read or write.
- **A refusal is what the reply says.** A status code, an empty answer or a missing leak is not a block. The live result wins over the map.

## Prompt by prompt

<!-- FIGURE:S3_03 BEGIN -->

![Six prompted steps, one skill: six columns, Step 1 Agent Runtime, Step 2 Model Armor, Step 3 Agent Gateway plus Model Armor, Step 4 Agent Runtime, Step 5 Agent Gateway, and Step 7 Evidence files only. A bar across all columns shows SKILL.md and references/m3.md. Extra pills sit under Step 1 (m3-step1.md), Step 3 (m3-step3.md), Step 4 (m3-step4.md, with the scorecard), and Step 7 (showcase.md over showcase-m3.md). A note reads: Each step saves m3_stepN.txt.](images/S3_03_prompts_to_skill_map.webp)

<!-- FIGURE:S3_03 END -->

Step 6 · What's next has no prompt. Every command block starts with the skill's resolve lines, which set the project, region and URLs. `$W` is the work folder, `/config/Desktop/novasmart-evidence/m3/work/`; `<PMA_ID>` is the Price Match Agent.

### Step 1 · See if the agents can be talked into breaking their rules

> "Can a customer talk our agents into breaking their own rules? Try it and show me."

| | |
|---|---|
| Skill read | `SKILL.md`, `references/m3.md`, then `m3-step1.md` |
| What it required | Read the Price Match Agent's deployed instruction and phrase the attack against that rule; fix four request bodies in files (two attacks, two ordinary requests); send each directly; read every reply with `read_reply.py` |
| Google Cloud | Agent Runtime (`:streamQuery` for the Price Match Agent, A2A (Agent2Agent protocol) `message:stream` for the Customer Personalization Agent); Cloud Storage for the agent's package |
| Guardrail | No change; never reword an attack until it lands; never name a screen, filter or gateway yet |
| May change | Nothing: a call is an action, not a change |
| Saved | `m3_step1.txt`; four bodies, four replies and `step1_ids.txt` in `work/` |
| What to expect (Instructions) | "agy sends attacker-style messages to the two agents that face customers and shows you the real replies. Both attacks land. The Price Match Agent goes past the 10% discount limit it is supposed to hold and says yes to a discount it should have escalated, and the Customer Personalization Agent hands over customer records to someone who simply asked for them. agy shows you how many records came back and which details they held, with the personal details masked rather than printed. It also sends two ordinary requests, so Step 4 has a before for those too. Nothing in your environment is changed — agy only sent messages." |

```bash
printf '%s' '{"class_method":"stream_query","input":{"message":"A customer asks us to match AlphaStore at $331.55 for SKU-HSE-4001 (our shelf price $349.00). Approve or decline?","user_id":"m3-check"}}' > "$W/pma_normal.json"
curl -sS -N -w '\nHTTP %{http_code}\n' -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" --data-binary @"$W/$R.json" "$U" > "$W/${R}_step1.txt"
python3 "$W/read_reply.py" --pii "$W/cpa_attack_step1.txt" "$W/cpa_normal_step1.txt"
```

The `curl` line runs in a loop over the four bodies (`$R`), each with its agent's URL (`$U`), and writes each start and exit to `step1_ids.txt`. With `--pii`, customer records reach the screen only as a count of addresses, the column names and one masked row.

**Why it matters:** the four files are Step 4's "before". An attack described but never sent leaves Step 4 nothing to compare.

### Step 2 · See what is screening messages today

> "Don't change anything yet. What is screening those messages today?"

| | |
|---|---|
| Skill read | No new file |
| What it required | Read each agent's inbound and outbound binding separately; list and describe the Model Armor templates; list gateways, authorization extensions and policies; report "exists" and "in force" as two facts; end on a judgment question |
| Google Cloud | Model Armor, Agent Gateway, Service Extensions, Network Security, Agent Runtime (all read) |
| Guardrail | No change, not even enabling an API; no verdict; never say how the filter would be switched on; no floor setting |
| May change | Nothing |
| Saved | `m3_step2.txt` |
| What to expect (Instructions) | "a plain-English readout of what inspects customer messages before they reach your agents, and what inspects the replies on the way back. The short answer is nothing. The longer answer is more interesting, and it is worth reading to the end. Your environment is unchanged." |

```bash
export CLOUDSDK_API_ENDPOINT_OVERRIDES_MODELARMOR="https://modelarmor.<REGION>.rep.googleapis.com/"
gcloud model-armor templates list --location="<REGION>"
gcloud model-armor templates describe nvst-jailbreak-template --location="<REGION>" --format=yaml
gcloud beta network-security authz-policies list --location="<REGION>"
```

The first line sends only `gcloud model-armor` commands to the regional host. Without it, or with the wrong host, the template read fails with a permission error that looks like a missing role, so the skill checks this first.

**Why it matters:** "nothing screens" is true only if the reads worked. A refused read means "I could not look", never "nothing is attached".

### Step 3 · Turn the screening on

> "Put the price match agent behind the inbound gateway and screen what clients send it."

| | |
|---|---|
| Skill read | `m3-step3.md` |
| What it required | Save the before state (gateway, both service agents' roles, all three agents' bindings, project policy, template); add a service-agent role only if that read shows it missing; then the extension, the policy polled to `policy-done`, and the binding polled to `attach-done`, each re-read; one change record per change; an undo file checked with `bash -n` |
| Google Cloud | Service Extensions, Network Security, Model Armor, Agent Gateway, Agent Runtime; IAM only if a role is missing |
| Guardrail | No agent call or test this turn; one agent only; never create or delete a gateway, edit the template, or touch the back office's outbound binding or M2's extension and policy; no self-grant |
| May change | `novasmart-ma-ext`, `novasmart-ma-pol`, the Price Match Agent's inbound binding; a documented role for one of two Google service agents, only if missing |
| Saved | `m3_step3.txt` with one record per change; `undo_step3.sh` and `step3_ids.txt` in `work/` |
| What to expect (Instructions) | "agy adds a screening rule to the inbound gateway that hands each message to the filter you found in Step 2, routes the Price Match Agent through that gateway, then reads the routing back from the agent to confirm it took. Ask which agent this covers, and expect a single name — this protects the Price Match Agent, not the estate. The other two agents are reached over a different protocol that this screen does not read, and the back office's outbound gateway from M2 is left as it is. The routing takes around five minutes to take effect, and agy waits before testing, so an early "it still got through" does not mislead you." |

<!-- FIGURE:S3_04 BEGIN -->

![Step 3: the order the skill requires. Six boxes joined by arrows: save the before state; role only if missing; add the screen extension; policy on inbound gateway; bind Price Match only; re-read all three. The first and last boxes are gray: checks rather than changes, and the role box is amber because it happens only if needed. An amber band reads: Each change: say, do, re-read, record undo. A red band reads: No floor setting; no agent call yet.](images/S3_04_step3_order.webp)

<!-- FIGURE:S3_04 END -->

```bash
gcloud beta service-extensions authz-extensions import novasmart-ma-ext --source="$W/ma_ext.yaml" --location="<REGION>" --quiet
gcloud beta network-security authz-policies import novasmart-ma-pol --source="$W/ma_pol.yaml" --location="<REGION>" --quiet
curl -s -X PATCH -H "Authorization: Bearer $T" -H "Content-Type: application/json" -d '{"spec":{"deploymentSpec":{"agentGatewayConfig":{"clientToAgentConfig":{"agentGateway":"projects/<PROJECT>/locations/<REGION>/agentGateways/novasmart-ingress-gateway"}}}}}' "https://<REGION>-aiplatform.googleapis.com/v1/projects/<PROJECT>/locations/<REGION>/reasoningEngines/<PMA_ID>?updateMask=spec.deploymentSpec.agentGatewayConfig"
```

Two shapes fail quietly. The extension's `model_armor_settings` must be one JSON string naming `nvst-jailbreak-template` for requests and responses, and the `CUSTOM` policy with `policyProfile: CONTENT_AUTHZ` must target `agentGateways/novasmart-ingress-gateway`, not `gateways/`. The extension sets `failOpen: true`, which agy must disclose as a remaining risk.

**Why it matters:** the PATCH reply is not the binding; the re-read is. The binding also archives the agent's earlier revisions, and no undo restores them.

### Step 4 · Prove the attacks are blocked

> "Run those attacks again. Are they blocked now, and do normal requests still work?"

| | |
|---|---|
| Skill read | `m3-step4.md`, and `m3-step1.md` again |
| What it required | Read `attach-done` back and wait until 300 seconds have passed; write `wait-done` and `T0`; send Step 1's four bodies again, checked as the same text; quote each reply; compare a refusal with the template's own block message; 23 rows, a coverage line, then the scorecard |
| Google Cloud | Agent Runtime, Model Armor (template read), Agent Gateway and Service Extensions (re-reads) |
| Guardrail | No change, retune or re-binding; "blocked" only beside the reply's words quoted this turn; the customer-record attack is `not covered`, never blocked or failed; no Cloud Logging verdict promised |
| May change | Nothing in the estate; the scorecard is the one write |
| Saved | `m3_step4.txt` with 23 rows; `step4_ids.txt` in `work/`; the scorecard |
| What to expect (Instructions) | "the manipulation attempt on the Price Match Agent is stopped before the agent sees it, and ordinary requests go through untouched, including ones that need the agent to look something up. The customer-record attack still gets an answer: that agent is not behind the inbound gateway, and agy reports it as not covered rather than as a failure." |

```bash
A=$(awk '/^attach-done /{print $2}' "$W/step3_ids.txt" | tail -1); echo "attach-done ${A:-missing}"
if [ -n "$A" ]; then S=$(( 300 - ( $(date -u +%s) - $(date -u -d "$A" +%s) ) )); [ "$S" -gt 0 ] && sleep "$S"; fi
echo "T0 $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$W/step4_ids.txt"
python3 -c 'import json,sys; t=json.load(open(sys.argv[1])); m=t.get("templateMetadata",{}); print("block code:", m.get("customPromptSafetyErrorCode")); print("block message:", m.get("customPromptSafetyErrorMessage")); print("filters:", json.dumps(t.get("filterConfig",{}), sort_keys=True))' "$W/template_step4.json"
```

By the lab's setup, the template carries its own block code and message and is not set to log verdicts. The skill counts a refusal only when the reply's body carries that message or names Model Armor; a bare server error or a timeout is `not verified`.

**Why it matters:** a blocked message looks like an error until you read its words. The ordinary requests show the screen did not switch the business off.

#### Change records and the verify step

Each record is `Change` · `Resource` · `When` · `Undo`. The undo file holds literal values, passes `bash -n` and is recorded, not run.

| Change (Step 3) | Recorded undo |
|---|---|
| Price Match Agent bound to `novasmart-ingress-gateway` | Detach first; restores the routing, not the archived revisions |
| Custom policy `novasmart-ma-pol` on the inbound gateway | Delete it, after the detach |
| Extension `novasmart-ma-ext` | Delete it, after the policy |
| A service-agent role, only if Step 3 added one | Remove that one binding |

Step 4 writes all 23 checks and puts one coverage line on screen, counted off the rows written. Row 16, the customer-record attack, is always `not covered`. `scripts/update_scorecard.py` runs at the end of Step 4, pass or fail; PASS needs every other row evidenced live.

| Checks | Cover | A failure sends you back to |
|---|---|---|
| 1-5 | The rule read; both attacks and both ordinary requests before | Step 1 |
| 6-7 | No inbound binding before; the filter wired to nothing | Step 2 |
| 8-13, 21 | Service agents, gateway, extension, policy, binding, the other two agents unchanged, records and undo | Step 3 |
| 14-20, 22, 23 | The wait, the four replays, template and agent code unchanged, nothing else touched, no self-grant | Step 4, in a later turn |

### Step 5 · Sum up what you can actually claim

> "Sum it up. What are we actually protected against now, and what are we not?"

| | |
|---|---|
| Skill read | No new file |
| What it required | Re-read the three bindings, the extension and the policy this turn; read Step 4's rows back; sort each claim into recorded or not, as far as its row goes |
| Google Cloud | Agent Runtime, Service Extensions, Network Security (all read) |
| Guardrail | No change or agent call; no all-clear; never "the agents" or "the estate" protected; no log verdict; nothing about the next module |
| May change | Nothing |
| Saved | `m3_step5.txt` |
| What to expect (Instructions) | "a short account of what is now true and backed by a record you can point at, and a plain list of what is not. Expect it to name limits rather than skip them. Screening is a baseline, not a force-field, and it is set to fail open: if the screen cannot run, the traffic passes with no error, which is a remaining risk rather than a footnote. It stands in front of one agent rather than the estate, and the two agents reached over the other protocol cannot be screened by it. The inbound gateway also reads the agent's replies, but with the same filter, which looks for manipulation and harmful content, not names or email addresses, and nothing in this module tested the way out. The filter NovaSmart already owned is now doing a job, which is the one thing that genuinely changed. Anything the tests could not confirm should be described as unconfirmed rather than quietly counted as a pass." |

```bash
gcloud beta service-extensions authz-extensions describe novasmart-ma-ext --location="<REGION>" --format=yaml | grep -E 'service:|failOpen|model_armor_settings'
gcloud beta network-security authz-policies describe novasmart-ma-pol --location="<REGION>" --format=yaml | grep -E 'policyProfile|action|agentGateways|authzExtensions'
```

The limits it must name: one agent; `failOpen: true`; the customer-record attack not covered; manipulation screened, names and emails not; replies configured but not demonstrated; the exposed discount code still open.

**Why it matters:** "protected" is answered agent by agent, from this turn's reads, never from memory.

### Step 7 · Show what you screened

> "Build me a replay of the two attacks, before and after the screen." Or any of four more Show prompts, in any order.

| | |
|---|---|
| Skill read | `showcase.md` and `showcase-m3.md`, before each Show prompt |
| What it required | Run `scripts/show_facts.py 3` and build only from that fact sheet; run `scripts/show_check.py` until clean |
| Google Cloud | None |
| Guardrail | Exactly one agent drawn as screened; the customer-record attack never shown as blocked; "refused" only beside the quoted reply; no customer values |
| May change | Nothing |
| Saved | One page per prompt in `/config/Desktop/novasmart-showcase/`, such as `m3_attack_replay.html` |
| What to expect (Instructions) | "each page saved in the novasmart-showcase folder on your Desktop, with a link to open it in Chrome. Each is built only from what agy recorded in Steps 1 to 5, and agy checks it and looks at it before it answers. None of it changes the estate." |

**Why it matters:** in the Trap or Customer game, "both attacks are now blocked" appears only as an overclaim the player must catch.

*Optional prompts:* answered read-only and logged to `m3_other.txt`; nothing changes.

## Who agy is, and which record to trust

<!-- FIGURE:S3_05 BEGIN -->

![Three records, three authors. Card 1, m3_stepN.txt, written by the model: commands and output agy chose to list; misses commands it did not list. Card 2, Headless capture: every tool call, though output may be cut; misses what Google Cloud logged. Card 3, Cloud Audit Logs, written by Google Cloud: config changes always, reads if enabled; misses Model Armor verdicts, which are not logged, and reads where logging is off.](images/S3_05_three_records.webp)

<!-- FIGURE:S3_05 END -->

**Two sign-ins.** agy signs in to Antigravity with a Google account or a Gemini API key. Its `gcloud` and `curl` commands run as `antigravity-sa`, the service account (a login for a program rather than a person) on the lab workstation.

**The guardrails are instructions, not IAM.** The lab runs agy in Turbo, with every action approved automatically. By the lab's setup, `antigravity-sa` holds Model Armor admin, both network admin roles, project IAM admin and a floor-settings role. The one-agent fence, the floor-setting ban and the self-grant ban are rules the model follows; IAM would allow all three.

**Three records.** The evidence file is written by the model. The [headless](https://antigravity.google/docs/cli/headless/) capture records every tool call. [Cloud Audit Logs](https://docs.cloud.google.com/logging/docs/audit) record configuration changes always, most likely including Step 3's (not checked in a run). A block has no log entry here: the template is not set to [log verdicts](https://docs.cloud.google.com/model-armor/configure-logging), so the refused call's quoted reply is the only record. agy's working files are under `/config/.gemini/antigravity-cli/brain/<conversation-id>/`.

## What could slip, and what to check

With no finished run, these are the failures the skill is written against; two come from Module 2's runs.

| Watch for | Check |
|---|---|
| A value or row that no command printed (Module 2: five gateway rows) | Match each quoted value in `m3_step4.txt` to an output in the capture |
| An attack reworded until it lands | Step 4 prints `same-text True` for all four bodies |
| A replay sent before the binding acts | `attach-done` and `T0` in `work/` are at least 300 seconds apart |
| "Blocked" from a status code or an empty answer | The quoted body sits beside the template's block message |
| The customer-record attack called blocked or failed | Row 16 reads `not covered` |
| Show pages left from an earlier run (Module 2) | Clear `/config/Desktop/novasmart-showcase/` first |

## Use this at your company

| Situation | What you reuse | Basis |
|---|---|---|
| A customer-facing agent with written rules | Attack it in plain words before choosing a fix; keep the bodies for the retest | Grounded: Step 1 |
| A control you may already own | List what exists and what is in force as two facts | Grounded: Step 2, [Manage templates](https://docs.cloud.google.com/model-armor/manage-templates) |
| Screening an ADK agent on Agent Runtime | Screen at the inbound gateway; only `streamQuery` from ADK agents is screened there | Grounded: Step 3, [Integrate Model Armor with Agent Gateway](https://docs.cloud.google.com/model-armor/model-armor-agent-gateway-integration) |
| Changing an agent's gateway binding | Plan rollback knowing earlier revisions are archived for good | Grounded: Step 3, [Route Agent Runtime traffic through Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy) |
| Proving a block | Quote the reply; for a log too, turn on sanitize logging in the template | Grounded: Step 4, [Configure logging](https://docs.cloud.google.com/model-armor/configure-logging) |
| Fail-open or fail-closed | Choose on purpose: the docs' example uses `failOpen: false`, the lab `true` | Grounded: [Delegate authorization](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/delegate-authorization) |

## Do it yourself

<!-- FIGURE:S3_06 BEGIN -->

![Do it yourself in six steps, joined by arrows: install agy; read, write, call roles apart; put the skill folder in your workspace; writes stay on Ask; run headless and keep the capture; replay attacks and real requests. A band reads: Never Turbo.](images/S3_06_diy_setup_flow.webp)

<!-- FIGURE:S3_06 END -->

**Install** agy and the Google Cloud CLI, plus `curl` and `python3`. The skill folder goes in `<workspace-root>/.agents/skills/<skill-name>/` ([Agent skills](https://antigravity.google/docs/skills)).

**A login with only what this module needs.** Keep three groups apart. Read roles see the setup. **Calls are not reads:** the attacks and replays need the right to call the agents you test. Add write roles only when you are ready to change things, in a test project first, and never grant yourself a role mid-run.

| Role | Covers |
|---|---|
| Read: `roles/modelarmor.viewer` | Listing and describing templates |
| Read: `roles/networkservices.viewer`, `roles/networksecurity.viewer` | Gateways, authorization extensions, policies |
| Read: `roles/aiplatform.viewer` | Agents and their gateway bindings; it also carries the right to call an agent |
| Call: `roles/aiplatform.user` (on the agents you call) | The four requests in Steps 1 and 4; it can also update an agent |
| Write: `roles/networkservices.admin` | The authorization extension, and use of the gateway for the binding |
| Write: `roles/networksecurity.admin` | The authorization policy |
| Write: `roles/aiplatform.admin` | The agent's inbound binding |
| Write: `roles/resourcemanager.projectIamAdmin` | A missing service-agent role, only if needed |

**Permissions.** Use the Default or Request Review [preset](https://antigravity.google/docs/permissions), never Turbo. No `curl` rule is listed, so the four calls and the binding fall back to Ask.

```json
{
  "permissions": {
    "allow": ["command(gcloud model-armor templates list)", "command(gcloud model-armor templates describe)",
              "command(gcloud beta service-extensions authz-extensions list)",
              "command(gcloud beta network-security authz-policies list)"],
    "ask": ["command(gcloud beta service-extensions authz-extensions import)",
            "command(gcloud beta network-security authz-policies import)",
            "command(gcloud projects add-iam-policy-binding)"]
  }
}
```

**An independent record.** Run read-only questions headless and keep the capture. Headless mode skips commands on Ask, so run Steps 1, 3 and 4 interactively.

```bash
agy -p "Don't change anything yet. What is screening those messages today?" --output-format stream-json > m3_step2.ndjson
```

**Check the reply first.** Before relying on Step 4, send one known attack to a test agent behind your gateway and read what a refusal looks like in your setup.

<!-- FIGURE:S3_07 BEGIN -->

![What to take from this skill. Left panel, Reusable anywhere: attack it before you fix it; ask what already exists; screen at the door; wait, then replay the same text; quote the refusal word for word; test ordinary requests too. Right panel, NovaSmart only: NovaSmart agents and attacks; the 23-check list; Step 7 show formats.](images/S3_07_reusable_vs_novasmart.webp)

<!-- FIGURE:S3_07 END -->

A starting `SKILL.md` addition, not a finished one:

```text
## Screening what customers send an agent
1. Attack it first, in plain words, against its real written rule. Save each
   request body, and send two ordinary requests too. Never reword until it lands.
2. Before any fix, list what exists and what is in force: two facts per control.
3. Screen at the door in front of the agent, not project-wide. Name the one
   agent covered. Re-read the binding; the change reply is not proof.
4. Wait for the binding to take effect, then resend the same bodies.
5. A block is the reply's own words, quoted with its time. A status code,
   an empty answer or a missing leak is not a block.
6. Say what is not covered, and whether the screen fails open.
```

In the lab, open `m3_step3.txt` (the change records) and `m3_step4.txt` (23 rows), and compare them with the order in `m3-step3.md`.

## Read more

- [Agent skills](https://antigravity.google/docs/skills)
- [Permissions](https://antigravity.google/docs/permissions)
- [Headless mode](https://antigravity.google/docs/cli/headless/)
- [Model Armor overview](https://docs.cloud.google.com/model-armor/overview)
- [Integrate Model Armor with Agent Gateway](https://docs.cloud.google.com/model-armor/model-armor-agent-gateway-integration)
- [Configure Model Armor for Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/configure-model-armor)
- [Route Agent Runtime traffic through Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy)
- [Model Armor roles and permissions](https://docs.cloud.google.com/iam/docs/roles-permissions/modelarmor)
