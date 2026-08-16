# Charts & Heavy Rendering Guide

> **Scope:** Data visualization, canvas vs SVG, dashboards, real-time series

## The rule behind every rule

A chart is a rendering budget with axes. Its cost has three independent components — **data preparation** (parse, aggregate, decimate), **scene construction** (nodes or draw calls), and **update frequency** (how often the first two repeat) — and the guide's whole job is keeping each one proportional to what the user can actually perceive. A screen is ~2,000 pixels wide; a series of 200,000 points offers the user at most 2,000 distinguishable positions. Rendering the other 198,000 is cost without information.

## Choosing the substrate

| Situation | Substrate | Why |
| :--- | :--- | :--- |
| ≤ ~1,000 elements, interactivity per element (hover, click, tooltips) | **SVG** | DOM events, CSS styling and inspectability for free; node count is the limit |
| 1,000–100,000 points, redraw-heavy, pan/zoom | **Canvas 2D** | one node, draw-call cost instead of tree cost; you own hit-testing |
| > 100k points, continuous streaming, multiple linked charts | **WebGL / offscreen** | GPU-side geometry; the only substrate where "all the data" is even discussable |
| Sparklines, static thumbnails | **Inline SVG or pre-rendered image** | no runtime at all beats every runtime |

The decision is recorded in `PERF-DECISIONS.md` with the scale that drove it (§5 of the core). A dashboard that picked SVG at 300 points and now renders 30,000 does not "optimize the SVG" — it crosses the substrate boundary the original decision named.

## Good Examples

### 1. Decimate to the pixel grid
```js
// LTTB (largest-triangle-three-buckets) down to ~2 points per pixel
const width = canvas.clientWidth;
const drawable = lttb(series, width * 2);
draw(ctx, drawable);
```
- **Why:** the eye cannot resolve more than the pixel grid; LTTB keeps the visual shape (peaks, outliers) while cutting draw cost by orders of magnitude. Decimation happens on data change, not on every frame.

### 2. Prepare off-thread, draw on-thread
```js
worker.postMessage({ raw, width }, [raw.buffer]);   // transfer, don't copy
worker.onmessage = ({ data }) => {
  prepared = data;                                   // typed array back
  scheduleDraw();
};
```
- **Why:** parsing and aggregating a large payload is CPU work with no DOM dependency — exactly what workers are for. The main thread receives draw-ready typed arrays; transferables make the handoff free.

### 3. One frame, one draw
```js
let pending = false;
function scheduleDraw() {
  if (pending) return;
  pending = true;
  requestAnimationFrame(() => { pending = false; render(prepared); });
}
```
- **Why:** twelve state changes between frames produce one render, not twelve. Every data source, resize and interaction funnels through the same scheduler; the frame budget is spent once.

### 4. Resize without thrash
```js
const ro = new ResizeObserver(entries => {
  const { inlineSize, blockSize } = entries[0].contentBoxSize[0];
  canvas.width = inlineSize * devicePixelRatio;
  canvas.height = blockSize * devicePixelRatio;
  scheduleDraw();
});
ro.observe(container);
```
- **Why:** `ResizeObserver` delivers geometry without polling or layout reads in a resize handler; scaling by `devicePixelRatio` keeps the chart sharp without CSS-pixel overdraw on high-density screens.

### 5. Streaming with a ring buffer
```js
const buf = new Float32Array(WINDOW);   // fixed memory
function push(v) { buf[i++ % WINDOW] = v; dirty = true; }
setInterval(() => { if (dirty && !document.hidden) { dirty = false; scheduleDraw(); } }, 100);
```
- **Why:** a live chart's memory does not grow with uptime, redraws are capped at 10 fps (plenty for telemetry) and stop entirely in hidden tabs. The alternative — `data.push()` forever plus draw-per-message — is a leak with a frame cost attached.

## Bad Examples

### 1. The DOM as plotter
```js
points.forEach(p => {
  const dot = document.createElement('div');
  dot.style.cssText = `left:${x(p)}px; top:${y(p)}px`;
  chart.append(dot);   // 40,000 absolutely-positioned divs
});
```
- **Why it fails:** forty thousand nodes cost style, layout and memory before the first pixel paints, and every hover recalculates against all of them. This is the unbounded-list anti-pattern drawn as a picture.

### 2. Redraw per datum
```js
socket.on('tick', (point) => {
  data.push(point);
  chart.destroy();
  chart = new Chart(ctx, { data });   // full reconstruction, 60×/s
});
```
- **Why it fails:** construction cost (scales, layout, legend) is paid per message instead of per visible change. Streams mutate buffers and schedule frames; they never reconstruct.

### 3. Animated everything
```js
options.animation = { duration: 800 };  // on a dashboard of 12 charts
```
- **Why it fails:** twelve charts × 800 ms of entrance tweening is ten seconds of aggregate main-thread animation for information the user came to *read*. Dashboards render settled; animation is reserved for state *changes* the user triggered, and stays under 250 ms.

### 4. The hidden dashboard that keeps drawing
```js
setInterval(fetchAndRedrawAll, 5000);   // runs in background tabs
```
- **Why it fails:** a wall of charts redrawing in a tab nobody is looking at is the polling anti-pattern at its most expensive. Gate on `document.hidden`, and on re-show, fetch once and settle.

## Dashboards specifically

- **Charts share one scheduler.** N charts each with their own `requestAnimationFrame` loop contend; one coordinator draws the dirty subset per frame, in priority order (viewport first).
- **Below-the-fold charts don't exist yet.** Construct on approach (`IntersectionObserver`), render a static placeholder image or empty reserved box until then.
- **Linked interactions batch.** A crosshair moving across six linked charts updates six overlays in one frame — overlays being cheap layers (a line, a label), never full redraws of the six scenes.
- **The data layer dedupes.** Six charts over the same series hold one copy of the prepared arrays, not six transformations of the same fetch.

## Checklist
- [ ] Substrate chosen from the table and recorded with its scale threshold.
- [ ] Points drawn ≤ ~2× horizontal pixels; decimation on data change.
- [ ] Heavy preparation in a worker with transferables past ~1 MB of data.
- [ ] All redraws funnel through one rAF scheduler; no draw outside it.
- [ ] Streaming charts: fixed-size buffers, visibility-gated, capped fps.
- [ ] Resize via `ResizeObserver`, scaled by `devicePixelRatio`.
- [ ] Dashboard: lazy construction below fold, shared scheduler, deduped data.
- [ ] Entrance animation absent or ≤ 250 ms; hidden tabs draw nothing.
- [ ] Tooltip and crosshair layers are overlays; base scenes redraw only on data or geometry change.
