# M4 Step 4 — Make the change and see what is actually running · the procedure

> Read this when the leader reaches **M4 Step 4**. `../SKILL.md` and `m4.md` still apply: `m4.md` §5 holds
> the resolve lines (`W`, `L`), the agents list and the results read-back block; §9 holds all 22 rows;
> `m4-step2.md` §5 holds the run's contract for the local copy.
>
> ⛔ **One edit, on the local copy: Step 3's change, and nothing else.** Nothing in the estate is changed
> or deployed. One answer, two halves: make the change and measure it on the same cases; then turn to
> what is deployed and say what is still true there. The second half is the module's point — never soften
> it with the first.
>
> ⛔ **Background tasks (`../SKILL.md` §0 rule 11):** the run goes to the background. No comparison, row,
> picture or entry line until "finished with result" arrives; then read the values back from files.

## 1. Back up, apply only Step 3's change, re-read

Step 3 saved its change to `$L/step3_change.json` (`line`, `old`, `new`). Apply exactly that:

```
A="$L/m4-local/app/agent.py"; sha256sum "$A"
cp "$A" "$L/agent.py.before-step4"
python3 - "$A" "$L/step3_change.json" <<'PY'
import json,sys
c=json.load(open(sys.argv[2])); lines=open(sys.argv[1]).read().split("\n"); i=c["line"]-1
if lines[i]!=c["old"]: sys.exit("not applied: line %d no longer reads as Step 3 showed it" % c["line"])
lines[i]=c["new"]; open(sys.argv[1],"w").write("\n".join(lines)); print("applied at line", c["line"])
PY
diff "$L/agent.py.before-step4" "$A"; echo "diff-exit $?"
```

- The starting hash must equal the one Step 3 printed (row 15); read it back from `m4_step3.txt`, never
  from memory. Different → the file moved since Step 3: say so, and apply nothing until the diff is shown
  again.
- `diff` is the re-read: expect exactly Step 3's `-` and `+` lines (`diff-exit 1` means "differs").
  Anything more → restore the backup (`cp` back), say what happened, and stop the edit there.
- **Change record:** `(nothing changed in the estate in this step)`, then `Local edit:` the file path and
  `Backup:` the backup path, labelled *a file in a folder on this workstation, not the estate*. No `Undo:`.

## 2. Replay the same cases — never synthesize again

```
sha256sum -c "$L/cases.sha256"; echo "replay-start $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee "$L/step4_ids.txt"
```

`cases.json: OK` or nothing runs. **No `synthesize` this turn**: a re-synthesized set is a different set,
its later turns depend on the agent's replies, and it may not be compared case by case.

The procedure is **exactly Step 2's** (`m4-step2.md` §5) — the same script, the same frozen file, the same
judge model (`gemini-3.8-flash`) and policy metric — run on the edited copy:

```
JUDGE="projects/${PROJECT}/locations/global/publishers/google/models/gemini-3.8-flash"
python3 "$W/m4_eval.py" "$L/cases.json" "$L/results_step4.jsonl" --project "$PROJECT" --region "$REGION" \
  --agent "local:$L/m4-local/app/agent.py" --judge-model "$JUDGE" > "$L/step4_eval.log" 2>&1; echo "eval-exit $? $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$L/step4_ids.txt"
grep '^M4EVAL' "$L/step4_eval.log" | tee -a "$L/step4_ids.txt"
grep -h 'M4EVAL script sha256\|judge model' "$L/step2_ids.txt" "$L/step4_ids.txt"
```

- The last line puts Step 2's and Step 4's script hash and judge model side by side: they must be equal.
  Different → the two runs are not comparable case by case; say so, and report each run on its own.
- Failures follow `m4-step2.md` §5 (no replies → `not run`; no judge → `m4-step1.md` §2c item 2).

## 3. Read back and compare, case by case

`cat "$L/step4_ids.txt"`, the `m4.md` §5 results block on `results_step4.jsonl`, then:

```
python3 - "$L/results_step2.jsonl" "$L/results_step4.jsonl" <<'PY'
import json,sys
def load(p): return {str(r.get("case")): r for r in map(json.loads, filter(str.strip, open(p)))}
a, b = load(sys.argv[1]), load(sys.argv[2])
def cut(s): s=" ".join(str(s or "").split()); return s if len(s)<=300 else s[:300]+" [... cut ...]"
for k in sorted(set(a)|set(b), key=lambda x: (len(x), x)):
    x, y = a.get(k, {}), b.get(k, {})
    va, vb = x.get("verdict", "missing"), y.get("verdict", "missing")
    print("case", k, "|", va, "->", vb, "| moved" if va != vb else "| same", "| expected changed" if x.get("expected") != y.get("expected") else "")
    if va != vb: print("  reply after:", cut(y.get("reply"))); print("  reason after:", cut(y.get("reason")))
print("cases before", len(a), "| cases after", len(b))
PY
```

## 4. What good looks like — the movement

- One table, Step 2's columns plus the two verdicts side by side, on **Step 2's `N`**; each run's
  `n matched · f did not · u not run` line as printed. No arithmetic between them, no percentage, no
  "improved by".
- A paragraph on **which cases moved and what changed in the reasoning**, quoting the reply after. A case
  that moved for a reason its reply does not show is unexplained: say so. A case marked `expected changed`
  means the judge read the policy differently between runs: name it; it is not movement.
- **Expect movement, not a clean sweep.** A judge is a model and two runs can disagree on an unchanged
  case; a movement is evidence, not proof. Ran it more than once? Say how many times and report each.
- Cases that failed on the copy's price lookup or on escalation say nothing about this change.

## 5. The deployed side — read this turn

Run the `m4.md` §5 agents list with `| tee "$W/agents_step4.txt"`, then:

```
grep -i -A2 'price match' "$W/agents_step4.txt"; grep -i -A2 'price match' "$W/step1_ids.txt"
gcloud storage cp "gs://novasmart-seed-bucket-${PROJECT}/agent.zip" "$W/agent_step4.zip"
python3 - "$W/agent_step4.zip" "$L/step3_change.json" <<'PY'
import json,sys,zipfile
z=zipfile.ZipFile(sys.argv[1]); src=z.read([n for n in z.namelist() if n.endswith("price_match_agent.py")][0]).decode()
print("Step 3's old line present in the seed source:", json.load(open(sys.argv[2]))["old"] in src)
print("lines carrying the policy-disclosure rule:", sum(1 for x in src.split("\n") if "Secret Policy Disclosure" in x))
PY
```

- The agent record holds **no instruction text**: the seed bucket's `agent.zip` is the closest read of what
  it runs. Say so in the body; never call it the running artifact.
- **What is still true in production**, each clause tied to a read above: the deployed agent's `updated`
  time is the one Step 1 read, so it has not been redeployed and **does not have the change**; the line
  Step 3 targeted is still in the source; the policy-disclosure rule is still there — **the code's value
  stays in the file**, never on screen or in a picture; the screen: `gateway:` attached → a fail-open
  screen sits in front of this one agent, and it **held** only for rows where Step 1 quoted its message;
  `ABSENT` → no screen is attached. Step 1's run is still the only measurement of the deployed agent.
- The strongest honest sentence available: *a better instruction exists on this workstation; nothing
  customers reach has changed.*

## 6. The picture — REQUIRED, RULE, side by side

- **Left, the local copy:** its rule as the edited file reads now (from the `diff` re-read), with the
  changed branch visible as a change, not a rewrite of everything;
- **right, what is deployed:** the same rule as the seed source carries it, captioned *from the source in
  the seed bucket; the agent record holds no instruction*, and its record's last-updated time; the
  disclosure rule shown as *present* without the code; the screen in front of the deployed side only if
  `gateway:` showed it attached this turn, labelled *attached*, never *held*, unless Step 1 quoted a block;
- one line: *the edit exists on the left only; nothing was deployed*; anything not read this turn marked
  **unknown**, with the command beneath the picture;
- a caption: both sides read this turn, and from where.

No verdict word (*vulnerable*, *hardened*, *protected*, *fixed*), no tick, count, path or code value.

## 7. The checklist — all 22 rows, read back, then the coverage line

Rows 1-15 are event rows from Steps 1-3: run this, record it as a command, and copy each row from its
output — never retyped:

```
for f in m4_step1 m4_step2 m4_step3; do echo "== $f"; awk '/^ENTRY /{b=""} {b=b $0 "\n"} END{printf "%s", b}' "/config/Desktop/novasmart-evidence/m4/$f.txt" | grep -E '^\| *([1-9]|1[0-5]) \|'; done
```

Rows 16-19 come from this turn's outputs. **State rows 20-21 are re-read now:**

```
grep -E 'step1_cases.csv|updated' "$W/step1_ids.txt"
gcloud storage cat "gs://novasmart-seed-bucket-${PROJECT}/evaluation_dataset.csv" | sha256sum
gcloud projects get-iam-policy "$PROJECT" --flatten="bindings[].members" --filter="bindings.members:antigravity-sa" --format="value(bindings.role)" | sort | diff "$W/sa_roles_step1.txt" -; echo "roles-diff-exit $?"
```

A missing row from an earlier step stays, `not verified`, with the reason (the step was not run, or its
file has no row). On screen, `### What I checked` is the one coverage line (`m4.md` §9).

## 8. Don't mislabel

- An improvement on the local copy is not an improvement in production, in either direction.
- Never "fixed", "eliminated", "proved" or "hardened"; at most the door held, and only where Step 1 quoted it.
- Never deploy, offer to, or frame deployment as the obvious next step; the gap is the finding, and it
  belongs to the team that owns the agent, with a review.
- Never mention a screen the gateway read did not show.
- No launch position, and nothing about what you would fix first or watch after launch: the leader's own
  questions come after this step.

## 9. How to close

`m4.md` §2 Close check, row 4. Questions from the distance you just described: how long a change like this
normally sits between writing and a customer feeling it; who would have to agree before it reached the live
agent; what would tell NovaSmart that the version customers talk to is the version somebody reviewed.
