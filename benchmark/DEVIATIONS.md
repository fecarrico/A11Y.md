# Deviations from the pre-registered protocol

> Every departure from [`METHODOLOGY.md`](METHODOLOGY.md) as registered ([osf.io/pg6r5](https://osf.io/pg6r5)), dated, with what changed and why. Deviations are documented, never hidden — that is the entire point of pre-registering. Newest first.

---

## 2026-08-16 — Protocol tag is annotated, not GPG-signed

- **Registered text:** "The repository tag marking the frozen protocol is signed."
- **What happened:** no GPG signing key is configured on the collection machine; the tag `benchmark-protocol-v2.0` was created annotated but unsigned.
- **Why it does not weaken the freeze:** the tamper-evident anchor was never the tag — it is the OSF registration itself, which is immutable, timestamped by a third party, and carries the SHA-256 of every frozen file. The tag is a repository-side convenience pointer to the same tree.
- **Remedy if it matters later:** a signed tag can be added over the same commit once a key exists; the hashes in the registration make any rewrite detectable either way.
