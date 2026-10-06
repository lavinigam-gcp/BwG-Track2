# Security

## Reporting

Please report security issues by opening an issue in this repository. Do not include credentials,
tokens, or the contents of `~/.config/gcloud` in the report.

## What these scripts do to your machine

`setup/install.sh` installs software and writes only to:

- `~/novasmart-lab/` — the Python virtual environment and a log
- `~/Desktop/Session1`, `Session2`, `Session3` — lab workspaces
- your shell profile — one `PATH` line and one environment variable

On Linux and WSL2 it uses `sudo` for `apt-get`, and adds the Google Cloud CLI and NodeSource
package repositories with their signing keys. On macOS it uses Homebrew. Run
`bash setup/install.sh --dry-run` to see every command before anything executes.

## What they never do

- Never disable TLS verification. If a corporate proxy intercepts TLS, the scripts tell you to
  install your organisation's CA bundle rather than working around it.
- Never run Antigravity or Chrome with `--no-sandbox`.
- Never ask for, store, or transmit credentials. Google Cloud sign-in is done by `gcloud` itself,
  interactively, and the tokens stay in your own gcloud configuration.
