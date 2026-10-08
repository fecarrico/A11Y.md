# Accessibility statement

🇧🇷 Leia em português: [ACCESSIBILITY.pt-BR.md](./ACCESSIBILITY.pt-BR.md)

A11Y.md is a standard that AI coding agents read before they generate an interface. This file is the statement the standard asks every adopter to publish about their own product, written here about this project's own surfaces: the documents in this repository, the project website, the Wiki and the scripts in `tools/`. The rules themselves are in [`docs/en/A11Y.md`](docs/en/A11Y.md).

You are reading this through GitHub. The accessibility of that interface is [GitHub's own statement](https://accessibility.github.com/) to make. What follows is what this project controls.

## What this project holds itself to

- **Profile:** Shield (AAA), the strictest of the standard's three [compliance profiles](docs/en/references/guide-compliance-profiles.md), for every interface produced from this repository.
- **Standard version:** 2.3.0.
- **The same evidence we ask of adopters.** The website keeps the three artifacts the standard requires, in public: a [verification report](https://github.com/fecarrico/a11ymd/blob/main/REPORT.en.md), an [exceptions log](https://github.com/fecarrico/a11ymd/blob/main/EXCEPTIONS.md) and a [decisions log](https://github.com/fecarrico/a11ymd/blob/main/A11Y-DECISIONS.md). The status in the table is read from them, not from memory.

## Where things stand

| Surface | What was verified | Status |
| :--- | :--- | :--- |
| [Website](https://fecarrico.github.io/a11ymd/) | axe-core 4.13.0 with the AAA rule set on all eight routes, at 1280 px and 320 px. Keyboard pass with computed styles over the menu, the disclosure and the lightbox. 200% zoom and text spacing. The standard's static gate: PASS. | ⚠️ CONDITIONAL. The screen-reader pass has not been done by a person. |
| The standard and its guides (`docs/`) | Plain Markdown in two editions kept at parity by `tools/lint-standard.py`: same files, same headings, same rule count. Heading levels nest without skips in every file under `docs/` and in the root documents, no link reads "click here", and the images in the README carry alt text. | Maintained. Not audited by a third party. |
| Scripts in `tools/` | Output is plain text with no colour. The last line says PASS or FAIL in words and gives the counts. | Maintained. The level of each finding is told by a leading marker, not a word (see known barriers). |
| [Wiki](https://github.com/fecarrico/A11Y.md/wiki) | Markdown with the same conventions as `docs/`. | Not audited. |

`benchmark/` is research material. The pages the studies generated are published as a dataset with its own DOI, and many of them are inaccessible on purpose, because that is what the studies measure. Nothing there is an example to follow.

## Known barriers

Everything here is also an open item in the website's report or exceptions log. Nothing is held back from this list.

1. **The website has not been tested with a screen reader by a person.** Every automated and keyboard checkpoint passes. The standard forbids an agent from claiming a screen-reader test it could not hear, so the status stays CONDITIONAL until someone runs the script in [REPORT §3](https://github.com/fecarrico/a11ymd/blob/main/REPORT.en.md#3-behavior-and-task-return). If you use NVDA, JAWS, VoiceOver or TalkBack and have twenty minutes, this is the single most useful thing you can do for this project. Your name goes in the report.
2. **No colour-vision simulator has been run on the website.** Contrast ratios are measured and recomputed by the gate. Functional loss through colour is not.
3. **Three decisions on the website await the author:** right-aligned text in the timeline, the spacing between paragraphs on the home (both House Rule relaxations against NBR 17225 5.12.5 and 5.12.3), and whether the logos in the timeline are decorative. Until the third is confirmed, those logos carry an empty alt.
4. **Headings in the READMEs start with an emoji.** A screen reader announces the symbol before the heading text. The structure underneath is correct. They stay for visual scanning, and we are not sure that is the right call. Tell us if it costs you.
5. **The scripts mark the level of each finding with a symbol.** An error line starts with `✗` and a warning with `!`. The words appear only in the summary at the end.

## How to report a barrier

Open an [issue](https://github.com/fecarrico/A11Y.md/issues/new) in this repository. No template is needed. Say what you were trying to do, which assistive technology or input method you were using, and what happened. A barrier on the website can be reported here too, and we move it to the site's repository ourselves.

If an issue is not the right medium for you, start a thread in [Discussions](https://github.com/fecarrico/A11Y.md/discussions).

You will get a first response within **7 days**, the same window as the [security policy](SECURITY.md). A confirmed barrier becomes an entry in the exceptions log, with an owner and a review date, until it is fixed. The fix is credited in the [CHANGELOG](CHANGELOG.md).

## If you contribute

An interface built for this project is built under the standard's own invocation line and the Shield profile, and ships with the same three artifacts expected from any adopter. For Markdown, the bar is the one measured in the table: heading levels nest without skipping, link text says where the link goes, an image carries alt text or is marked decorative, and no meaning rides on colour or on an emoji alone. The [contributing guide](CONTRIBUTING.md) has the rest.

## Who answers for this

Felipe Carriço maintains this repository and this statement. It is reviewed whenever the website's report changes status, an exception opens or closes, or a release ships. Last reviewed on 2026-10-08, against version 2.3.0 of the standard.

Reading this with an AI agent? The rules it should follow are in `docs/en/A11Y.md`, and the one line to add to its configuration is in the [README](README.md#-quick-start-under-2-minutes).
