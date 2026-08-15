# Interactive Maps Guide

> **Scope:** Embedded and interactive maps — store locators, delivery tracking, area pickers, coverage displays. The component most often shipped as an inaccessible third-party island, and the clearest case of Principle Zero: if the task can only be completed on the map, the task cannot be completed.

## 0. The rule everything else follows

**The list is the map's alternative — and it is not a fallback, it is the primary path for a large share of users.**

```tsx
<section aria-labelledby="stores-h">
  <h2 id="stores-h">Stores near 01310-100</h2>
  <div id="map" aria-label="Map of nearby stores" role="application">{/* … */}</div>
  <ol>
    <li>
      <h3>Paulista branch</h3>
      <p>Av. Paulista 1000 — 1.2 km away — open until 10pm</p>
      <a href="/stores/paulista">Details</a>
    </li>
  </ol>
</section>
```

Everything the map communicates — what is here, how far, in what order, what happens if I pick it — exists in text, in the same page, updating with the same filters. Once that list exists, most of the map's accessibility burden is discharged, and what remains is making the map itself not actively hostile.

**Never make the map the only way to:** choose an address, pick a delivery area, select a store, confirm a location, or see a status. A drag-a-pin flow with no address field is a keyboard-inaccessible form.

## 1. Decide what kind of map it is

| Kind | Example | What it owes |
| :--- | :--- | :--- |
| **Decorative** | a stylized city illustration behind a heading | `aria-hidden="true"` — and the address written out in text, as always |
| **Static informative** | a rendered image of one location | it is an image: `alt` with the information, not "map" — see [Images](guide-images.md) |
| **Interactive** | pan, zoom, clickable markers, filters | everything below |

A static image whose `alt` reads *"Map showing our location"* has told the reader nothing. The alternative is the address.

## 2. Keyboard

1. **The map container is a single tab stop** that can be entered and — critically — **left**. A map that traps arrow keys is a keyboard trap (SC 2.1.2); `Esc` must always return to the page.
2. **Panning and zooming have keyboard equivalents** (arrows to pan, `+`/`-` to zoom), and zoom controls are real `<button>`s with names, not `<div>`s carrying icons.
3. **Markers are focusable controls with accessible names** — *"Paulista branch, 1.2 km"* — or, better, the list beside the map is the way to reach them and the map follows the list's selection. The second design is easier to get right and better for everyone.
4. **Nothing depends on hover.** Information revealed by hovering a marker must be reachable by focus (see [Tooltips & Popovers](guide-tooltips-popovers.md)) and present in the list.
5. **Gestures have single-pointer alternatives (SC 2.5.1):** pinch-to-zoom and two-finger pan need buttons too; drag-to-place-a-pin needs an address input (see [Drag & Drop](guide-drag-drop.md)).

> **`role="application"` is a loaded gun.** It hands raw keystrokes to the widget and disables the screen reader's own reading commands. Use it only on a map that genuinely implements full keyboard interaction, never on the whole page or on a container the user merely reads.

## 3. Announce what changed

Pan, zoom and filter change the visible content silently. Announce the **result** from a polite status region, never the movement:

```tsx
<div role="status" aria-live="polite" className="sr-only">
  {`${results.length} stores in view`}
</div>
```

The same rule as any dashboard: announce the outcome ("4 stores in view"), not the event ("map moved"). Live tracking that updates continuously needs a pause (SC 2.2.2) and must not re-announce on every tick.

## 4. Color, contrast and labels on the tiles

- Route lines, area shading and markers are meaningful graphics: **3:1 against their surroundings** (SC 1.4.11) — and against each other, when two routes or zones sit side by side.
- **Never encode category by color alone** (SC 1.4.1): marker shape, numbering or a label carries it too. A "green = available / red = full" map is unreadable for a large share of users, including this project's own maintainer.
- Text baked into map tiles does not resize with the page and often fails contrast. Anything that matters is repeated in the DOM.
- Map text is exempt from nothing: the labels *you* place on the map follow the active profile's typography floor.

## 5. Third-party providers

Most maps come from Google Maps, Mapbox, Leaflet or an equivalent. **The obligation does not transfer with the embed** — the same rule as consent platforms (see [Consent & Cookie Banners](guide-consent-banners.md)).

- Test the provider's default widget with keyboard and a screen reader **before** adopting it. Several ship keyboard support behind a configuration flag.
- Give the `<iframe>` a `title` that says what it contains — an untitled map iframe is announced as "frame".
- Where the provider's control cannot be fixed in this cycle, that is an `EXCEPTIONS.md` entry with owner, issue and expiry — and the text alternative is what keeps the feature usable meanwhile, which is why it is never optional.

## Success criteria mapped

| SC | Level | What it requires here |
| :--- | :--- | :--- |
| 1.1.1 Non-text Content | A | the information on the map exists as text |
| 2.1.1 Keyboard | A | pan, zoom, markers and selection operable without a mouse |
| 2.1.2 No Keyboard Trap | A | the map can always be left |
| 2.5.1 Pointer Gestures | A | pinch and drag have single-pointer alternatives |
| 1.4.1 Use of Color | A | category never carried by color alone |
| 1.4.11 Non-text Contrast | AA | routes, zones and markers at 3:1 |
| 4.1.3 Status Messages | AA | changes in view or results announced |

## Tip for the AI:

Complete the task with the map hidden — `display: none` on the container, then finish the flow. If you cannot find the store, choose the address or confirm the delivery area, the interface is broken for everyone who cannot use the map, and no amount of ARIA on the canvas will fix it. Build the list first; the map is the enhancement.
