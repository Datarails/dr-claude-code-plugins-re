# Logos used by this template (base64 PNG)

The agent cannot read binary files from a skill, so each logo is inlined here. Insert with `sheet.shapes.addImage(base64)` (no `data:` prefix), then set the position and size from the spec's picture lines: displayed width/height in **pixels** (points = px × 0.75), position = the anchor cell's `left`/`top` plus the stated offset in pixels × 0.75. The displayed width and height can differ by a pixel from the PNG's own proportions, so **unlock the aspect ratio, set both dimensions, then lock it again**. Never stretch to fit a cell.

```js
const a = sheet.getRange("B1"); a.load("left,top"); await context.sync();
const img = sheet.shapes.addImage(LOGO_BASE64);
img.name = "logo-datarails-white"; img.lockAspectRatio = false;   // set both dimensions, then lock
img.left = a.left + dxPx * 0.75; img.top = a.top + dyPx * 0.75;
img.width = wPx * 0.75; img.height = hPx * 0.75;
img.lockAspectRatio = true;
await context.sync();
```

This template has no pictures.
