# Security Policy

## What "security" means in this repository

A11Y.md is portable markdown — it has no runtime, no build step and no dependencies, so most vulnerability classes do not apply to the standard itself. Two things here are executable or executed-adjacent, and they are the scope of this policy:

1. **The scripts in [`tools/`](tools/)** (`verify-a11y.py`, `lint-standard.py`) — stdlib-only Python that adopters run locally and in CI, sometimes fetched by URL.
2. **The standard as agent input.** The core file and its guides are injected into AI coding agents as trusted context. Content in this repository that could steer an agent into doing something harmful — a malicious edit, a link swapped for a hostile destination, an instruction smuggled into a guide — is a supply-chain issue for every adopter, and we treat it as a vulnerability, not as vandalism.

## Reporting a vulnerability

Use **[GitHub private vulnerability reporting](https://github.com/fecarrico/A11Y.md/security/advisories/new)** for anything you believe should not be public before a fix — especially anything in category 2 above. For everything else, a regular issue is fine.

You will get a first response within **7 days**. There is no bug bounty; there is credit in the CHANGELOG, which this project takes seriously.

## Hardening guidance for adopters

- **Pin to a tag, never to `main`**, when fetching `tools/` scripts in CI. A moving branch is executable code you have not reviewed. The [tools README](tools/README.md) shows the pinned form and this repository keeps tags 1:1 with CHANGELOG versions.
- **Pointing your agent at the GitHub URL** (the Quick Start default) means trusting this repository's `main` branch as agent context. If your threat model does not allow that, use the offline copy flow in the [Quick Start](README.md#-quick-start-under-2-minutes): vendor `docs/` into your repository at a reviewed commit and point the rule at the local path.

## Supported versions

Only the latest tagged release receives corrections. The standard is a pair of markdown trees — upgrading is a diff, and the [CHANGELOG](CHANGELOG.md) documents every normative change, including a migration note when a release breaks an existing artifact.
