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
| Colours, type and layout | `assets/css/site.css` |

**Placeholders.** A link set to `"PLACEHOLDER"` in `config.js` — or to anything that isn't an `https://` URL — renders as a disabled "coming soon" label instead of a link. Replace it with the real URL and it becomes a working link; nothing else needs editing. The Discord invite and the spelunky.fyi listing ship as placeholders.

**Media.** Add up to three entries to `media`, e.g. `{ src: "/assets/media/run.gif", alt: "What happens in the clip" }`. They fill the slots in order (the first is the wide one); empty slots show as "coming soon".

**The randomizer repository must be public.** View on GitHub and Download Beta point at [kakudio/spelunky2-key-item-randomizer](https://github.com/kakudio/spelunky2-key-item-randomizer) and its `/releases/latest`. Both 404 for visitors while that repository is private. `/releases/latest` always resolves to the newest release, so new betas need no link change.

## Deployment

GitHub Pages serves the root of `main` as-is (`.nojekyll` turns off Jekyll processing). Anything merged to `main` goes live at <https://kakudio.dev/> within a minute or two.

The `CNAME` file is the repository's half of the custom domain. The other half is outside this repository: DNS records for `kakudio.dev`, and Pages enabled in **Settings → Pages** with source *Deploy from a branch*, `main`, `/ (root)`, and *Enforce HTTPS* on. See GitHub's guide to [configuring a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

## Favicon and social preview

`assets/img/favicon.svg` is the source for the icons. `assets/img/social-preview.png` (1200×630) is a screenshot of `tools/social-preview.html` served from the repository root; the PNG icons are screenshots of the SVG at 32×32 and 180×180. Re-take them with any browser screenshot tool if the wordmark or colours change. The metadata points at `https://kakudio.dev/assets/img/social-preview.png`, so social previews only work once the site is live.
