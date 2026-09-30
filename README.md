# kakudio.github.io

Source for [kakudio.dev](https://kakudio.dev), the Kakudio website: one static page that introduces Kakudio and sends people to the beta of Shell Game, a key item randomizer for Spelunky 2. Plain HTML, CSS and a little JavaScript — no framework, no build step.

## Run it locally

From the repository root, start any static file server:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. The 404 page is at <http://localhost:8000/404.html>. Asset paths are root-relative (`/assets/...`), so serve from the repository root rather than opening the files directly.

## Where things are configured

| What | Where |
| --- | --- |
| Randomizer name, descriptor (the line under the name), description, beta status, requirements line | `config.js` → `randomizer` |
| Every external link (Download Beta, View on GitHub, Join Discord, spelunky.fyi, GitHub org) | `config.js` → `links` |
| Screenshots and gameplay GIFs | `config.js` → `media`, files in `assets/media/` |
| Brand copy, headings, beta-tester and About text, footer | `index.html` |
| Search, Open Graph and social-card metadata | `<head>` of `index.html` |
| Layout, spacing, focus rings, reduced motion, and the knobs a theme sets | `assets/css/base.css` |
| Colours, type, textures, decoration and the wordmark lettering | the active theme, `assets/themes/<game>/` (today `spelunky`) |
| Which theme a page wears | the theme `<link>` in the `<head>` of `index.html`, `404.html` and `tools/social-preview.html` |

**Placeholders.** A link set to `"PLACEHOLDER"` in `config.js` — or to anything that isn't an `https://` URL — renders as a disabled "coming soon" label instead of a link. Replace it with the real URL and it becomes a working link; nothing else needs editing. The Discord invite and the spelunky.fyi listing ship as placeholders.

**Media.** Add up to three entries to `media`, e.g. `{ src: "/assets/media/run.gif", alt: "What happens in the clip" }`. They fill the slots in order (the first is the wide one); empty slots show as "coming soon".

**The randomizer repository must be public.** View on GitHub and Download Beta point at [kakudio/spelunky2-key-item-randomizer](https://github.com/kakudio/spelunky2-key-item-randomizer) and its `/releases/latest`. Both 404 for visitors while that repository is private. `/releases/latest` always resolves to the newest release, so new betas need no link change.

## Themes

The look is split in two. `assets/css/base.css` is game-neutral: it owns layout, spacing, accessibility and behaviour, and declares the custom properties (knobs) in its `:root` with plain defaults — palette, fonts, wordmark lettering, button and focus-ring styling, and the height of the hero's ground. A theme dresses the page for one game on top of that.

**What a theme contains.** One folder under `assets/themes/`, holding everything the look needs:

```
assets/themes/spelunky/
  theme.css      knob values and decoration
  fonts/         self-hosted, openly licensed type, with its licence (OFL.txt)
  img/           original pixel-art textures and motifs (SVG)
```

`theme.css` sets knobs on `:root` and may add decoration — backgrounds, borders, shadows, `@font-face`, and `::before`/`::after` pseudo-elements. The page's sections (`.hero`, `.lost`, `.brand-line`, `.testers`, `.about`, `.site-footer`) are positioned and isolated by the base, so decoration can be placed inside them and layered behind the content with a negative `z-index`; `.ground` is an empty strip along the bottom of the hero and the 404 page, as tall as `--ground-height`. It never changes display, size, margin, padding or grid placement of page content; the base owns those. Animations need no reduced-motion handling of their own: the base stops every animation under `prefers-reduced-motion`. Reference the bundle's files with root-relative paths (`/assets/themes/<game>/...`), and never load anything from a third-party server.

**Adding a theme.** Copy `assets/themes/spelunky/` to `assets/themes/<game>/`, replace its fonts and images, and change the knob values and decoration in its `theme.css`. An empty `theme.css` is valid and shows the base defaults, which is a quick way to check that a theme only changes the look.

**Making a theme active.** Each page names its theme in exactly one place, the second stylesheet link in its `<head>`:

```html
<link rel="stylesheet" href="/assets/css/base.css">
<link rel="stylesheet" href="/assets/themes/spelunky/theme.css">
```

Point that link at the new theme in `index.html`, `404.html` and `tools/social-preview.html`. It is plain CSS loaded in the `<head>`, so it applies without JavaScript and without a flash of another look. Also set `<meta name="theme-color">` in both pages to the theme's `--bg`: it is page metadata that follows the active theme, not a second selector. Then re-take the favicon and social preview (below) so they match.

## Deployment

GitHub Pages serves the root of `main` as-is (`.nojekyll` turns off Jekyll processing). Anything merged to `main` goes live at <https://kakudio.dev/> within a minute or two.

The `CNAME` file is the repository's half of the custom domain. The other half is outside this repository: DNS records for `kakudio.dev`, and Pages enabled in **Settings → Pages** with source *Deploy from a branch*, `main`, `/ (root)`, and *Enforce HTTPS* on. See GitHub's guide to [configuring a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

## Favicon and social preview

`assets/img/favicon.svg` is the source for the icons. `assets/img/social-preview.png` (1200×630) is a screenshot of `tools/social-preview.html` served from the repository root; the PNG icons are screenshots of the SVG at 32×32 and 180×180. Re-take them with any browser screenshot tool if the wordmark, colours or active theme change. The metadata points at `https://kakudio.dev/assets/img/social-preview.png`, so social previews only work once the site is live.
