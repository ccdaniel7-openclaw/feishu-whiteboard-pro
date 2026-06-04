# Palettes (solid, flattened for the medium)

Because gradients are forbidden, color identity comes from **a few committed solid hexes** and
the figure-ground contrast between them. Each palette gives: a canvas/background, an ink
(near-black text), 1–3 accents — each with a matching **light tint** (chip fills / highlighted
columns) and a **dark on-tint** color to use on that tint — a **link** color (connector arrows),
and **dock** colors (a dark base band: panel fill + title + body text). Pick one palette per board
and commit. To simulate a gradient "progression" across staged lanes, step one accent family from
dark→light, giving each stage one solid accent.

## Pick by mood
| Want… | Try |
|---|---|
| Serious systems / compliance / gov | **Riptide**, **Slate**, **Steel** |
| Clean, airy, friendly tech | **Sky**, **Teal Mint** |
| Warm product / marketing | **Ember**, **Sunset** |
| Editorial / grounded / natural | **Forest**, **Sandstone**, **Moss & Clay** |
| Premium / finance / luxe | **Gold Ink**, **Indigo Night** |
| Bold / creative / playful | **Berry**, **Grape**, **Plum Rose**, **Lagoon** |
| Urgent / important | **Crimson** |
| Restrained / text-first | **Mono** |

Shared defaults (any palette): `chip fill #EEF3F8 border #D7E0EC text #1E293B` for neutral chips,
and an alert/pain accent `fill #FBEAEA border #F0C4C4 label #D11F44 text #9F1239`. Each palette below
may override these for tighter harmony.

---

## Cool

### Riptide — blue → teal · systems, compliance, gov/LE (default for serious product maps)
```
canvas   #F4F7FB     ink #0F172A     sub #475569
accent-1 #2A4BC4  tint #DCE5FF  on-tint #1E3A8A   (indigo — stage 1)
accent-2 #1487C9  tint #D6EEFB  on-tint #0B5C8A   (blue   — stage 2)
accent-3 #13877A  tint #D2F3EC  on-tint #0B5F54   (teal   — stage 3)
link     #0EA5C4   dock #14233F  panel #21324F  dock-title #5EEAD4  dock-text #CBD5E1
```

### Slate — cool neutral blue-gray · corporate, restrained, professional
```
canvas   #F4F6F9     ink #1B2432     sub #5A6678
accent-1 #2B4A6F  tint #DCE6F2  on-tint #1B3858   (steel blue)
accent-2 #4A6076  tint #E3E9EF  on-tint #33485C   (slate)
link     #2B4A6F   dock #1B2432  panel #2C3848  dock-title #9CC2E8  dock-text #C4CDD9
```

### Sky — light blue + cyan · airy, friendly tech, dashboards
```
canvas   #F2F8FE     ink #15293D     sub #4D6173
accent-1 #2D8FE0  tint #D7EAFB  on-tint #16608F   (sky blue)
accent-2 #18B4D4  tint #D2F1F7  on-tint #0C7287   (cyan)
link     #2D8FE0   dock #15293D  panel #213B52  dock-title #87CEF5  dock-text #C6D6E2
```

### Steel — cool gray + electric blue · industrial, engineering
```
canvas   #F1F3F5     ink #1A1F26     sub #565E68
accent-1 #2563EB  tint #DCE7FD  on-tint #1A47B0   (electric blue)
accent-2 #475A6B  tint #E0E6EC  on-tint #313F4C   (steel gray)
link     #2563EB   dock #1A1F26  panel #2A323C  dock-title #93B4FA  dock-text #C5CCD4
```

### Teal Mint — teal + aqua · fresh, clean, healthcare-adjacent
```
canvas   #EFF8F6     ink #10302B     sub #496B64
accent-1 #0E8C7F  tint #CFEDE8  on-tint #0A5F56   (teal)
accent-2 #2BB8A3  tint #D6F4ED  on-tint #157A6C   (mint-green)
accent-3 #3A86A8  tint #D7ECF4  on-tint #1E5A75   (aqua-blue)
link     #0E8C7F   dock #0E2A26  panel #1C3D38  dock-title #6FE0CE  dock-text #C4DCD7
```

## Warm

### Ember — burnt orange + amber · product, marketing, friendly
```
canvas   #FBF7F2     ink #1F2937     sub #6B5E54
accent-1 #C2410C  tint #FFE8DA  on-tint #9A3412   (burnt orange)
accent-2 #B45309  tint #FDEFD6  on-tint #92400E   (amber)
accent-3 #7C5E3B  tint #EFE6D8  on-tint #5B4527   (clay)
link     #EA7317   dock #2A211C  panel #3A2E25  dock-title #FBBF77  dock-text #E7DCD0
```

### Sunset — coral + amber + pink · energetic, launches, campaigns
```
canvas   #FFF6F0     ink #3A1F1A     sub #7A5248
accent-1 #E4572E  tint #FBE3D8  on-tint #A8341A   (coral-orange)
accent-2 #F2A007  tint #FDEFCF  on-tint #9A6500   (amber)
accent-3 #D6336C  tint #FBDDE8  on-tint #971C46   (pink)
link     #E4572E   dock #2E1A16  panel #43261F  dock-title #FBB582  dock-text #EAD7CF
```

### Sandstone — terracotta + olive + clay · earthy, editorial, grounded
```
canvas   #F7F2E9     ink #2E2519     sub #6B5A45
accent-1 #B5651D  tint #F1E2CC  on-tint #7A410F   (terracotta)
accent-2 #8A8B3C  tint #EBECCF  on-tint #5A5B22   (olive)
accent-3 #9C5A3C  tint #EFDCD0  on-tint #6A3823   (clay)
link     #B5651D   dock #2A2114  panel #3C3122  dock-title #E2B97E  dock-text #D8CDB8
```

### Crimson — crimson + maroon · bold, urgent, "this matters"
```
canvas   #FBF4F3     ink #2C1416     sub #6E4B4C
accent-1 #C0223B  tint #F7D8DD  on-tint #8A1326   (crimson)
accent-2 #7A1E2B  tint #EFD4D8  on-tint #561019   (maroon)
link     #C0223B   dock #2A1214  panel #3E1E22  dock-title #F2A1AC  dock-text #E2C9CC
```

### Gold Ink — navy + gold · premium, finance, luxe
```
canvas   #F7F4EC     ink #16213A     sub #4F5A6E
accent-1 #1E3A5F  tint #D7E1ED  on-tint #142A47   (navy)
accent-2 #B8860B  tint #F2E6C4  on-tint #7A5800   (gold)
link     #B8860B   dock #16213A  panel #243352  dock-title #E6C667  dock-text #CBD3DF
```

## Nature

### Forest — parchment + forest green · calm, research, grounded
```
canvas   #F4F6F1     ink #1A2421     sub #4B5A53
accent-1 #2F6B4F  tint #DCECE2  on-tint #1C4A35   (forest)
accent-2 #5B7A3A  tint #E6EFD8  on-tint #3D5424   (moss)
accent-3 #8A6D3B  tint #EFE6D2  on-tint #5E4823   (bark)
link     #2F6B4F   dock #1F2A26  panel #2E3C36  dock-title #9DE3BE  dock-text #CBD8D0
```

### Moss & Clay — moss + clay · natural, sustainability, outdoorsy
```
canvas   #F3F5EC     ink #232A1B     sub #57614A
accent-1 #5B7B2F  tint #E2EBCF  on-tint #3C5418   (moss)
accent-2 #A66A3C  tint #F0DECC  on-tint #6E4221   (clay)
link     #5B7B2F   dock #1F2616  panel #313A26  dock-title #AED57E  dock-text #CFD6BE
```

### Lagoon — deep teal + lime · bold, energetic, eco-tech
```
canvas   #EFF7F4     ink #0F2A28     sub #466660
accent-1 #0B6E6E  tint #CCE9E7  on-tint #084B4B   (deep teal)
accent-2 #84CC16  tint #E8F5CC  on-tint #4D7A0C   (lime pop)
link     #0B6E6E   dock #0C2422  panel #173733  dock-title #B6E84F  dock-text #C2DAD5
```

## Bold / Creative

### Berry — raspberry + periwinkle + teal · fruity, fresh, dashboards
```
canvas   #FBF6FA     ink #1E1B2E     sub #5B5470
accent-1 #B0246B  tint #FBDDEC  on-tint #841B50   (raspberry)
accent-2 #5B59C7  tint #E2E1FA  on-tint #3F3D99   (periwinkle)
accent-3 #2A8FA8  tint #D5EEF4  on-tint #14687E   (teal)
link     #B0246B   dock #211B33  panel #322A47  dock-title #F4A6CE  dock-text #D8D2E6
```

### Indigo Night — indigo + violet + magenta · premium, confident, product
```
canvas   #F3F2FB     ink #1A1538     sub #564E7A
accent-1 #4338CA  tint #E0DEFB  on-tint #2E2796   (indigo)
accent-2 #7C3AED  tint #EDE4FE  on-tint #5B21B6   (violet)
accent-3 #DB2777  tint #FBE0EE  on-tint #9D174D   (magenta pop)
link     #4338CA   dock #1A1538  panel #2C2553  dock-title #C4B5FD  dock-text #D4CFE8
```

### Grape — purple + plum · creative, expressive
```
canvas   #F6F2FA     ink #271A33     sub #5E4E72
accent-1 #7B2CBF  tint #ECE0F7  on-tint #561C86   (purple)
accent-2 #C2255C  tint #F8DCE6  on-tint #8A1741   (plum)
link     #7B2CBF   dock #221531  panel #352247  dock-title #CDA8F0  dock-text #D6CBE2
```

### Plum Rose — plum + rose · soft, lifestyle, warm-creative
```
canvas   #FBF3F6     ink #2E1A24     sub #6E5460
accent-1 #8E3B5E  tint #F4DDE6  on-tint #642740   (plum)
accent-2 #C76B86  tint #F8E2E8  on-tint #8E3F56   (rose)
link     #8E3B5E   dock #271520  panel #3C2230  dock-title #EBA8BE  dock-text #E0CBD4
```

## Neutral

### Mono — graphite only · restrained, institutional, text-first
```
canvas   #F7F7F8     ink #18181B     sub #52525B
accent   #27272A  tint #E7E7EA  on-tint #18181B   (graphite — the only "color")
link     #3F3F46   dock #18181B  panel #27272A  dock-title #E4E4E7  dock-text #A1A1AA
chip     fill #EFEFF1 border #D4D4D8 text #27272A
```
Carry hierarchy with weight, scale, and one graphite block-vs-panel role-swap — no second hue.

---
**Usage in the generator:** pass these hexes straight into `board.py` calls — `fill=` for blocks,
`key_fill / key_stroke / key_tx` for highlighted chips, the `dock`/`panel`/`dock-*` colors for a base
band. Keep **dark text on light tints, light text on saturated blocks**, and never put sub-16px text
directly on a saturated canvas (put it in a panel). When a board needs an alert/pain note, the shared
red accent above reads on every palette.
