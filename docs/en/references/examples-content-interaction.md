# Accessibility: Content, Interaction & Timing

> Scope: Microcopy, timeout management, aria-live feedback, multimedia accessibility, and AI content guidance.

## 1. Microcopy & Clarity
Language should be as simple as possible to reduce cognitive load.
- **Clear Instructions:** Avoid jargon. Use action verbs (e.g., "Submit" instead of "Process").
- **Field Identification:** Instructions about formats (e.g., "DD/MM/YYYY") must be outside the input and linked via `aria-describedby`.
- **Heading Content:** The text of the headings must clearly describe the section that follows.

## 2. Timing Management (Timeouts)
Many users take more time to read or interact with the system.
- **Do Not Remove Time Without Warning:** If a session is going to expire, the user **MUST** be warned in advance and have the option to extend the time.
- **Moving Content:** Carousels or self-updating content **MUST** have a "Pause" button.

## 3. System Feedback & Status Messages (Aria-live)
Dynamic changes that do not cause a page reload must be announced.
- **Status Updates:** Use `aria-live="polite"` for non-critical notifications (e.g., "Item added to cart").
- **Critical Errors:** Use `aria-live="assertive"` or `role="alert"` for errors that prevent immediate progress.
- **Progress:** If an action takes time, use a programmatic progress indicator that informs the task status.

## 4. Sensory and Multimedia
- **Sensory Language:** **MUST NOT** give instructions based solely on senses (e.g., "Click the round button on the right" or "Listen for the tone to begin"). Use text/context references (e.g., "Click the Submit button at the end of the form").
- **Captions and Transcripts:** Audio and video **MUST** have text alternatives or synchronized captions.

## 5. Tip for Content AI
When generating text for the interface, the AI must validate if the instruction survives without the visual context: *"If I couldn't see the screen, would this instruction still make sense?"*.
