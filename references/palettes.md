# Palettes (solid, flattened for the medium)

Because gradients are forbidden, color identity comes from **a few committed solid hexes** and
the figure-ground contrast between them. Each palette below gives: a canvas/background, an ink
(near-black text), and 1–3 accents with a matching **light tint** (for chip fills / highlighted
columns) and a **dark text** color to use on that tint. Pick one palette per board and commit.

To simulate a gradient "progression" across staged lanes, step one hue family from dark→light
(e.g. indigo → blue → teal in **Riptide**), giving each stage one solid accent.

## Riptide (cool · blue→teal · systems, compliance, gov/LE) — default for serious product maps
```
canvas   #F4F7FB     ink     #0F172A     sub-text #475569
accent-1 #2A4BC4  tint #DCE5FF  on-tint #1E3A8A   (indigo — stage 1)
accent-2 #1487C9  tint #D6EEFB  on-tint #0B5C8A   (blue   — stage 2)
accent-3 #13877A  tint #D2F3EC  on-tint #0B5F54   (teal   — stage 3)
cyan-link #0EA5C4   (connector arrows / hubs)
dock     #14233F  panel #21324F  dock-title #5EEAD4  dock-text #CBD5E1
chip     fill #EEF3F8  border #D7E0EC  text #1E293B
alert    fill #FBEAEA  border #F0C4C4  label #D11F44  text #9F1239
```

## Ember (warm · product / marketing / friendly)
```
canvas   #FBF7F2     ink #1F2937     sub #6B5E54
accent-1 #C2410C  tint #FFE8DA  on-tint #9A3412   (burnt orange)
accent-2 #B45309  tint #FDEFD6  on-tint #92400E   (amber)
accent-3 #7C5E3B  tint #EFE6D8  on-tint #5B4527   (clay)
link     #EA7317   dock #2A211C  panel #3A2E25  dock-title #FBBF77  dock-text #E7DCD0
```

## Forest (calm · editorial / research / grounded)
```
canvas   #F4F6F1     ink #1A2421     sub #4B5A53
accent-1 #2F6B4F  tint #DCECE2  on-tint #1C4A35   (forest)
accent-2 #5B7A3A  tint #E6EFD8  on-tint #3D5424   (moss)
accent-3 #8A6D3B  tint #EFE6D2  on-tint #5E4823   (bark)
link     #2F6B4F   dock #1F2A26  panel #2E3C36  dock-title #9DE3BE  dock-text #CBD8D0
```

## Mono (restrained · institutional / text-first · no accent color)
```
canvas   #F7F7F8     ink #18181B     sub #52525B
accent   #27272A  tint #E7E7EA  on-tint #18181B   (graphite — the only "color")
link     #3F3F46   dock #18181B  panel #27272A  dock-title #E4E4E7  dock-text #A1A1AA
chip     fill #EFEFF1 border #D4D4D8 text #27272A
```
Use weight, scale, and one graphite block-vs-panel role-swap to carry hierarchy.

## Berry (balanced · fresh · dashboards / playful-but-clean)
```
canvas   #FBF6FA     ink #1E1B2E     sub #5B5470
accent-1 #B0246B  tint #FBDDEC  on-tint #841B50   (raspberry)
accent-2 #5B59C7  tint #E2E1FA  on-tint #3F3D99   (periwinkle)
accent-3 #2A8FA8  tint #D5EEF4  on-tint #14687E   (teal)
link     #B0246B   dock #211B33  panel #322A47  dock-title #F4A6CE  dock-text #D8D2E6
```

---
**Usage in the generator:** pass these hexes straight into `board.py` calls — `fill=` for blocks,
`key_fill / key_stroke / key_tx` for highlighted chips, the dock colors for a base band. Keep
**dark text on light tints, light text on saturated blocks**, and never put sub-16px text directly
on a saturated canvas (put it in a panel).
