# Study 2 — governance at journey scale

Study 1 ([`../METHODOLOGY.md`](../METHODOLOGY.md), registered at
[osf.io/pg6r5](https://osf.io/pg6r5)) measures machine-detectable violations
in isolated components. This study measures what that design cannot see:
**consistency, reuse, governance and amortized cost across a whole journey,
in one real agent session** — the regime the standard was built for.

| Piece | File |
|---|---|
| Protocol (draft) | [`PROTOCOL.md`](PROTOCOL.md) |
| Frozen journey prompt | [`PROMPTS.md`](PROMPTS.md) |
| Consistency classifier spec | [`CLASSIFIER.md`](CLASSIFIER.md) |
| Deviations journal | [`DEVIATIONS.md`](DEVIATIONS.md) |

## Status

- [x] Protocol drafted (2026-08-18)
- [ ] Pilot run and discarded; lessons written into the protocol
- [ ] Classifier frozen (SHA-256 in `CLASSIFIER.md`)
- [ ] Registered on OSF (own registration — **before Study 1 publishes**)
- [ ] Collection
- [ ] Report

The ordering is the point: the classifier freezes before registration,
registration precedes collection, and Study 1's publication waits for the
registration so its limitations section can point at a live public test.
