# M2 Step 1 — See who can call the back office · the procedure (re-read at Step 4)

> Read this when the leader reaches **M2 Step 1**, and again at **Step 4** for the rogue block (§2) and
> the holders list (§3). `../SKILL.md` and `m2.md` still apply: the resolve lines, the agents list, the
> back office's own list and the project-wide callers block are in `m2.md` §5.
>
> ⛔ **Step 1 changes nothing.** You read two lists and make one call. The call is the "before" half of
> Step 4's before/after, so its URL, body and reply are saved to files Step 4 replays.
>
> ⛔ **Background tasks (`../SKILL.md` §0 rule 11):** the callers block and the call's stream often go to
> the background. No count, reply, table row or picture comes from them until "finished with result"
> arrives.

## 1. The integrity check — first, before the call

```
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" \
  --filter="bindings.members:test-agent-caller" --format="table(bindings.role)"     # expect: empty
gcloud run services list --format="table(metadata.name,spec.template.spec.serviceAccountName)"
# and the back office's own list (m2.md §5)                                          # expect: one binding naming it
```

Expect: no project roles · runs nothing · one binding on the back office. Anything else → **lead the answer
with it**: the leftover login is not otherwise unprivileged, so a later 403 would not isolate your change
and a later 200 would not prove it failed. Say what it holds, label every later attribution uncertain, and
**repair nothing** — removing a role from a live service's identity can take that service down.

## 2. The rogue call — Step 1 makes it, Step 4 replays it

Step 1 fixes the request once in two files. Step 4 reuses both unchanged, so the replay differs only in the
clock and the token. Mint, delete the throwaway config, and call **in one command** (each command is a
fresh shell):

```
# Step 1 only - fix the request
echo "$API/<MSA_ID>/a2a/v1/message:stream" > "$W/rogue_url.txt"
printf '%s' '{"request":{"messageId":"m2-rogue-1","role":"ROLE_USER","content":[{"text":"Which pricing tables can you read? Reply with their names only."}]}}' > "$W/rogue_body.json"

# Steps 1 and 4 - mint in an isolated config, delete it, call
RCFG=$(mktemp -d)
gcloud storage cp "gs://novasmart-seed-bucket-${PROJECT}/test-agent-caller.json" "$RCFG/key.json" --quiet
CLOUDSDK_CONFIG="$RCFG" gcloud auth activate-service-account --key-file="$RCFG/key.json" --quiet
ROGUE_TOKEN=$(CLOUDSDK_CONFIG="$RCFG" gcloud auth print-access-token)
rm -rf "$RCFG"; ls -d "$RCFG" 2>&1          # expect: No such file or directory
date -u +%Y-%m-%dT%H:%M:%SZ
curl -sS -N -w '\nHTTP %{http_code}\n' -X POST -H "Authorization: Bearer $ROGUE_TOKEN" \
  -H "Content-Type: application/json" --data-binary @"$W/rogue_body.json" "$(cat "$W/rogue_url.txt")" \
  | tee "$W/rogue_step<N>.txt"
```

- **Never print the key or the token**, and never impersonate the account by granting yourself token
  creation (a self-grant). `activate-service-account` stores the credential inside the config directory,
  which is why the whole directory goes, not only the key file.
- **Read the stream:** the answer is in the `artifactUpdate` event's `parts[].text`; `TASK_STATE_COMPLETED`
  with `final: true` ends it. Quote the HTTP status, the state and the answer text (table names only — no
  values). A 200 carrying only `TASK_STATE_SUBMITTED` means the call went to `message:send`: fix the
  endpoint, never claim an answer.
- **A 403 at Step 1 is a result.** Check §1's results first. **Never change the request until it returns
  200 and call that the before.**
- The prompt asks for table names on purpose: it shows the reach without putting margin values on screen.

## 3. The two lists, and who is on them (Step 4 re-uses this section)

1. **The back office's own list** — `:getIamPolicy` (`m2.md` §5). The short, deliberate list. Expect one
   binding naming the leftover login.
2. **The project-wide holders** — the `m2.md` §5 callers block, run to completion: it prints *roles
   checked*, *roles granting invoke*, the role-and-principal lines, and *principals who can invoke
   project-wide*. **No completed loop → no number**: say the check did not finish and what is missing;
   never infer a total from rows that scrolled past.

**Pin the population before you quote a figure.** The number counts principals holding a project-level
role that carries one of the three invoke permissions — not roles, and not the agent's own list. Two names
in it are not third-party callers: **the back office's own badge** (the agent itself) and **the front
desk's badge** (the approved caller). Quote the raw figure, say which two you set aside, give the adjusted
one. Never reconcile it against a count from a different population. **Every group you name adds up to the
figure you state**, and the back office is never counted as a caller of itself: a headline's *"N other
identities"* excludes it.

**Name them on screen by short label, not by string** — the full list, verbatim, goes in the file:

| In the file | On screen |
| :-- | :-- |
| `serviceAccount:<NUM>-compute@…` | *the default compute account (the store portal signs in as it)* |
| `serviceAccount:service-<NUM>@gcp-sa-…` | *Google's own service agents* — say how many |
| `serviceAccount:<name>@<project>.iam…` | its short name, with what it is if you read that (`antigravity-sa`, *my own login*) |
| `principal://…/reasoningEngines/<ID>` | *the Price Match agent's own badge* (agent name from the listing) |
| `user:<name>@…` | *a person's login* `<name>` |

Each with what its role lets it do, in plain words (*full control of the project*, *view the project*,
*use and manage agents*). **Look for a person's login** — read the file; never assert one is there or is
not. If one is, it is the most persuasive line in the module: name it on its own line.

## 4. The storefront's direct route

Read it, don't infer it: `gcloud run services describe novasmart-store-portal --region="$REGION"
--format=yaml` → the `STRATEGY_AGENT_ID` env value, compared with the back office's ID from the live
listing; then its `serviceAccountName`, and that account's project roles (`gcloud projects get-iam-policy`
filtered on it) — never the fence's word for them. The route is **permitted, not observed**: nothing here
calls it.

## 5. Snapshot the project policy

`gcloud projects get-iam-policy "$PROJECT" --format=json > "$W/project_policy_step1.json"` — Step 5's
change-set check and the self-grant row compare against it. Record it like any command.

## 6. What good looks like — a fixed shape, filled only from live output

```
| Who | Where their access comes from (own list / project role) | Which command showed me | What that lets them do | Should they? |
```

- **The `Which command showed me` cell is compulsory.** A row whose provenance cell is empty is a claim,
  not a finding, and does not go in. One row is required whatever else you found: **the project-wide
  holders**, with the count, the roles in plain words and the command.
- Headline: what the call returned, in plain words — e.g. *"a leftover test login just got an answer from
  the agent holding your margin logic"* only if the stream carried an answer.
- One distinction in the leader's words: **"can read the data" and "can call the agent" are two different
  permissions.** M1 settled the first; nobody ever chose the second here — it is a side effect of roles
  handed out project-wide.

## 7. The picture — REQUIRED, CALL

- the back office as the destination, named as the listing named it;
- **group 1, its own caller list:** the members `:getIamPolicy` returned — the leftover login marked as
  the one route exercised, with the status it returned;
- **group 2, reaching it from above the list:** the front desk's badge, the store portal's direct route (if
  §4 found it), and the remaining project-wide holders as one count — the raw figure **minus** the back
  office's own badge and every holder drawn separately (the front desk's badge, the store portal's
  account) — each marked permitted-but-unobserved;
- a legend for the two markings, plus one line: *an unobserved route is settled by placing that call and
  reading the status*;
- a caption: what was read, from where, when — including that the store route comes from the portal's
  configuration.

Anything not read is `unknown` with its command; never omit a group. Never upgrade the front desk or the
store route to observed: this step makes one call.

## 8. Don't mislabel

- A call you did not make is not a finding — and it destroys Step 4.
- "One binding on the agent" and "N principals project-wide" come from different commands; say which.
- A count of roles is not a count of callers; say which any number is.
- The gateway is attached to nothing; it is not a control here.
- No fix, no lock, no role, no badge named as what would close it — not even as a hypothetical (*"even if
  that key were removed…"*). No *verified* anywhere, the table included: say what the call returned.
- Never *"yet the escalation works"*: the front desk's ability is an inference from policy, not an
  observation.

## 9. How to close

`m2.md` §2 Close check, row 1. Questions grow from the gap: what a caller list on margin logic ought to
look like, who would put their name to it, how NovaSmart would notice a new name arriving.
