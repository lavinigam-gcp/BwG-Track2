# Contributing

This repository sets up a laptop for the Build with Google Track 2 lab. It is small on purpose.

## Reporting a problem

Open an issue with the output of:

```bash
bash setup/preflight.sh
bash setup/verify.sh --fix-hints
```

Include your operating system and version, and whether you are on Apple Silicon, Intel, or WSL2.
Those two outputs are almost always enough to diagnose a setup failure.

## Changing the scripts

Before opening a pull request:

```bash
bash -n setup/preflight.sh && bash -n setup/install.sh && bash -n setup/verify.sh
bash setup/preflight.sh
bash setup/install.sh --dry-run
```

Rules the scripts follow, and that changes should keep:

- **Idempotent.** Re-running a completed step does nothing.
- **Nothing destructive without consent.** Existing directories are reused or need `--force`.
- **`--dry-run` changes nothing at all**, including creating directories.
- **`verify.sh` is the only arbiter of success.** Do not weaken a check to make a run pass.
- **Portable shell.** macOS ships bash 3.2 and BSD userland: no `mapfile`, no `readlink -f`,
  no GNU-only `sed -i` (use `sed -i.bak` and delete the backup), and guard `"$@"` under `set -u`.
- **A path rewrite must match whole path components.** `/config` also appears inside `/configure`.

## Pinned versions

`setup/requirements-lock.txt` mirrors a reference environment. Do not bump a package on its own;
the whole set is resolved together and `verify.sh` asserts the exact count.
