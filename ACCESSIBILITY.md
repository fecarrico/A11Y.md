# Accessibility statement

🇧🇷 Leia em português: [ACCESSIBILITY.pt-BR.md](./ACCESSIBILITY.pt-BR.md)

A11Y.md is a set of Markdown documents: a standard that AI coding agents read before they generate an interface, the guides and templates it points to, and two small scripts. There is no app here. This statement covers what a person using assistive technology will find when reading, running or contributing to those documents, and where the project's one interface, its website, keeps its own evidence.

## What you will find here, and in what shape

- **Plain Markdown, in two editions.** Everything under `docs/` exists in English and in Portuguese, kept at parity by `tools/lint-standard.py`: same files, same headings, same number of rules. A screen reader gets the same structure in either language.
- **Structure you can navigate.** Heading levels nest without skipping in every file under `docs/` and in the documents at the root. Link text says where the link goes. Code samples sit under headings that say "Good Examples" and "Bad Examples", in words.
- **Nothing carried by colour or symbol alone.** The severity levels pair a coloured dot with the word (🔴 CRITICAL). The compliance profiles pair an icon with the name.
- **Images.** The only image is the banner in the README, with alt text. The badges under it are images with alt text.
- **The scripts** print plain text with no colour, and the last line says PASS or FAIL in words.
- **Reading with an agent.** The standard is meant to be fed to an AI agent, and the agent reads the same Markdown a person does. The one line that does it is in the [README](README.md#-quick-start-under-2-minutes).
- **The page around this text is GitHub's.** For the accessibility of GitHub itself, their statement is at [accessibility.github.com](https://accessibility.github.com/).

`benchmark/` is research material. The pages the studies generated are published as a dataset with its own DOI, and many of them are inaccessible on purpose, because that is what the studies measure. Nothing there is an example to follow.

## The website

The project's only interface is [fecarrico.github.io/a11ymd](https://fecarrico.github.io/a11ymd/). It lives in [its own repository](https://github.com/fecarrico/a11ymd) and is built under this standard's Shield (AAA) profile, with the three artifacts the standard requires kept in public: the [verification report](https://github.com/fecarrico/a11ymd/blob/main/REPORT.en.md), the [exceptions log](https://github.com/fecarrico/a11ymd/blob/main/EXCEPTIONS.md) and the [decisions log](https://github.com/fecarrico/a11ymd/blob/main/A11Y-DECISIONS.md). Its status today is ⚠️ **CONDITIONAL**: axe-core 4.13.0 with the AAA rule set passes on all eight routes at 1280 px and 320 px, the keyboard pass and the 200% zoom pass are done, the standard's static gate says PASS, and the screen-reader pass has not been done by a person.

## Known barriers

Nothing is held back from this list. The website items are also open in its report or exceptions log.

In this repository:

1. **Headings in the READMEs start with an emoji.** A screen reader announces the symbol before the heading text. The structure underneath is correct. They stay for visual scanning, and we are not sure that is the right call. Tell us if it costs you.
2. **The scripts mark the level of each finding with a symbol.** An error line starts with `✗` and a warning with `!`. The words appear only in the summary at the end.

On the website:

1. **No screen-reader pass by a person.** The standard forbids an agent from claiming a screen-reader test it could not hear, so the status stays CONDITIONAL until someone runs the script in [REPORT §3](https://github.com/fecarrico/a11ymd/blob/main/REPORT.en.md#3-behavior-and-task-return). If you use NVDA, JAWS, VoiceOver or TalkBack and have twenty minutes, this is the single most useful thing you can do for this project. Your name goes in the report.
2. **No colour-vision simulator has been run.** Contrast ratios are measured and recomputed by the gate. Functional loss through colour is not.
3. **Three decisions await the author:** right-aligned text in the timeline, the spacing between paragraphs on the home (both House Rule relaxations against NBR 17225 5.12.5 and 5.12.3), and whether the logos in the timeline are decorative. Until the third is confirmed, those logos carry an empty alt.

## How to report a barrier

Open an [issue](https://github.com/fecarrico/A11Y.md/issues/new) in this repository. No template is needed. Say what you were trying to do, which assistive technology or input method you were using, and what happened. A barrier on the website can be reported here too, and we move it to the site's repository ourselves.

If an issue is not the right medium for you, start a thread in [Discussions](https://github.com/fecarrico/A11Y.md/discussions).

You will get a first response within **7 days**, the same window as the [security policy](SECURITY.md). A confirmed barrier becomes an entry in the exceptions log, with an owner and a review date, until it is fixed. The fix is credited in the [CHANGELOG](CHANGELOG.md).

## If you contribute

Markdown here is held to the shape described in the first section: heading levels nest without skipping, link text says where the link goes, an image carries alt text or is marked decorative, and no meaning rides on colour or on an emoji alone. Issues and pull requests use GitHub's own forms. An interface built for the project, the website today, is built under the standard's own invocation line and the Shield profile, and ships with the same three artifacts expected from any adopter. The [contributing guide](CONTRIBUTING.md) has the rest.

## Who answers for this

Felipe Carriço maintains this repository and this statement. It is reviewed whenever the website's report changes status, an exception opens or closes, or a release ships. Last reviewed on 2026-10-08, against version 2.3.0 of the standard.

Reading this with an AI agent? The rules it should follow are in `docs/en/A11Y.md`, and the one line to add to its configuration is in the [README](README.md#-quick-start-under-2-minutes).
