# Images & Media Bytes Guide

> **Scope:** Formats, responsive sizing, decode cost, LCP images

## The rule behind every rule

Images are the heaviest bytes on most pages and the most common LCP element. Every image on a route answers four questions: is it the right **format**, at the right **size**, arriving at the right **time**, into **reserved space**? A yes to all four is the whole guide; everything below is the mechanics.

## Good Examples

### 1. The LCP hero
```html
<img src="hero-1280.avif"
     srcset="hero-640.avif 640w, hero-1280.avif 1280w, hero-1920.avif 1920w"
     sizes="100vw"
     width="1280" height="720"
     fetchpriority="high" decoding="async">
```
- **Why:** discoverable in the initial HTML (no CSS background, no JS insertion), priority-hinted so the preload scanner fetches it first, sized so layout is stable, and served in a modern format at the display resolution — not the original upload.

### 2. Below-the-fold discipline
```html
<img src="product-400.webp" srcset="product-400.webp 400w, product-800.webp 800w"
     sizes="(min-width: 900px) 33vw, 50vw"
     width="400" height="300" loading="lazy" decoding="async">
```
- **Why:** `loading="lazy"` defers bytes until approach; `sizes` matches the grid so a 400-pixel card never downloads 1600 pixels; explicit dimensions reserve the box.

### 3. Art direction without double downloads
```html
<picture>
  <source media="(max-width: 600px)" srcset="crop-square-600.avif">
  <img src="wide-1200.avif" width="1200" height="500">
</picture>
```
- **Why:** each viewport downloads its one appropriate crop. Hiding the unused variant with CSS downloads both.

## Bad Examples

### 1. The 4K thumbnail
```html
<img src="IMG_8842-original.jpg" style="width: 120px">
```
- **Why it fails:** four megabytes decoded to paint 120 pixels. The browser pays network, decode *and* memory for resolution nobody sees. Resize at build or CDN; the DOM is not an image editor.

### 2. Lazy-loading the LCP
```html
<img src="hero.avif" loading="lazy">  <!-- first thing the user sees -->
```
- **Why it fails:** the lazy observer waits for layout to know the image is in-viewport — adding a round trip of delay to the one image the LCP clock is measuring. Above-the-fold images load eagerly, with priority.

### 3. Background-image heroes
```css
.hero { background-image: url(hero.jpg); }
```
- **Why it fails:** invisible to the preload scanner until CSS is parsed and the element styled — routinely the difference between a 1.8 s and a 3.5 s LCP. Content images are `<img>`; CSS backgrounds are for texture.

### 4. Unsized embeds
```html
<img src="banner.png">
```
- **Why it fails:** no dimensions means zero reserved height; the page assembles, then jumps when bytes arrive. `width`/`height` (or `aspect-ratio`) cost nothing and eliminate the shift.

## Checklist
- [ ] AVIF/WebP with sensible fallback; SVG for line art and icons.
- [ ] `srcset`/`sizes` present and matched to rendered sizes — audit with DevTools' "actual vs intrinsic".
- [ ] Every image carries `width`/`height` or `aspect-ratio`.
- [ ] Above the fold: eager + `fetchpriority="high"` on the LCP candidate. Below: `loading="lazy" decoding="async"`.
- [ ] No image serves more than ~2× its largest rendered resolution.
- [ ] Icon systems ship as SVG sprite or inline — not as a font, not as PNGs.
- [ ] Hero variants exist at the breakpoints the design actually uses — a `srcset` of one file is a caption, not a strategy.
- [ ] Decode is `async` everywhere; nothing above the fold waits on a below-fold decode.
