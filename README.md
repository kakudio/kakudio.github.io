# kakudio.github.io

Source for [kakudio.dev](https://kakudio.dev), the Kakudio website: a static homepage that introduces Kakudio and sends people to the beta of Shell Game, a key item randomizer for Spelunky 2, and a page that tells players how to report bugs in Kakudio's mods. Plain HTML and CSS, plus one small script for the bug-report form — no framework, no build step.

## Run it locally

From the repository root, start any static file server:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. The bug-reporting page is at <http://localhost:8000/bug-report/> and the 404 page at <http://localhost:8000/404.html>. Asset paths are root-relative (`/assets/...`), so serve from the repository root rather than opening the files directly.

## Where things live

The report form on `/bug-report/` is the one piece of JavaScript on the site; every other page ships none. Every link and every piece of content — the form's labels and messages included — is written into the HTML of the page that shows it, so it appears exactly as served.

| What | Where |
| --- | --- |
| Homepage: brand copy, headings (including each game), Shell Game's name, Beta badge, descriptor, pitch and requirements line, beta-tester and About text, footer | `index.html` |
| Homepage links (Download Beta, View on GitHub, Join Discord, Report bugs that you find, About's closing line, Kakudio on GitHub) | `href`s in `index.html` |
| Bug-reporting page: where run logs live, the report form and all its copy, the report service's URLs and rules, and the instructions for sending a report from a script or agent, with the mods it covers | `bug-report/index.html`, served at `/bug-report/` |
| The report form's behaviour: choosing a run, checking it, sending it, and the copy buttons | `bug-report/report-form.js`, loaded only by `bug-report/index.html` |
| 404 page copy and its link home | `404.html` |
| Search, Open Graph and social-card metadata | `<head>` of each page |
| Layout, spacing, focus rings, reduced motion, and the knobs a theme sets | `assets/css/base.css` |
| Colours, type, textures, decoration and the wordmark lettering | the active theme, `assets/themes/<game>/` (today `spelunky`) |
| Which theme a page wears | the theme `<link>` in the `<head>` of `index.html`, `bug-report/index.html`, `404.html` and `tools/social-preview.html` |

**Links not yet known.** A link with no real URL yet is left out of the HTML entirely — never added with a made-up or placeholder URL. Today that is the spelunky.fyi listing. When it exists, add it to `index.html` below Shell Game's buttons:

```html
<p class="also-on"><a class="text-link" href="https://spelunky.fyi/...">Listing on spelunky.fyi</a></p>
```

**Links that repeat.** The Discord invite appears three times in `index.html` (Shell Game's buttons, *Come play with us* and About's closing line). Change all of them together.

**Media.** To show screenshots or gameplay GIFs beside Shell Game, put the files in `assets/media/` and add a media group as the last child of its `<article class="project-card">`, one `<figure class="slot">` per item; the first is shown wide, and the card switches to two columns on wide screens:

```html
<div class="media" role="group" aria-label="Screenshots and gameplay">
  <figure class="slot"><img src="/assets/media/run.gif" alt="What happens in the clip" loading="lazy" decoding="async"></figure>
</div>
```

Leave the group out while there is nothing to show.

**Bug reports.** `/bug-report/` is the public face of the Kakudio report service (`https://bug-reports.kakudio.workers.dev`); its address is linked from the service and from Shell Game, so it doesn't move. Everything it says about the service restates kakudio/bug-reports `service/README.md` and `service/src/submit.ts`, and where they disagree the service wins. Sending a report without the form is described once, in *From a script or agent* (`#service`): numbered steps written for a person — where the run logs are, picking the one for the run, the request with a `curl` example, and the answers. Its copy button copies those same visible steps as plain text, so they are what a player hands an agent; keep them complete enough to stand alone when pasted, with nothing that depends on the rest of the page. The steps list the covered mods by hand, copied from the service's `GET /api/mods`: when a mod is added to the service's list, add one row for it to the covered-mods table in step 1, with its name, `mod_id`, run-log folder, file names and first line.

**The report form.** `bug-report/report-form.js` is a hand-written script with no dependencies. It enhances the form already in `bug-report/index.html`: it reads the covered mods from the service's `GET /api/mods` (the URL in the form's `data-mods`) each time the page loads, so a new mod's run logs are recognised without changing the script, and posts to the form's `action`. It shows and hides the messages written in the HTML rather than writing its own. Its checks on a run log's name, first line, encoding and size mirror kakudio/bug-reports `service/src/mods.ts` and `service/src/submit.ts`, and only spare the player a pointless upload; the service decides. The service answers cross-origin requests only from the origins it lists in kakudio/bug-reports `service/src/cors.ts`, so the form can't send from `python3 -m http.server` unless the service is also run locally (`wrangler dev` in kakudio/bug-reports).

**Projects.** Projects are grouped by game: each game is a `<section class="game">` in `index.html` headed by the game's name, holding one `<article class="project-card">` per mod. Add a mod as another article inside its game; add a game as another section.

**The randomizer repository must be public.** View on GitHub and Download Beta point at [kakudio/spelunky2-key-item-randomizer](https://github.com/kakudio/spelunky2-key-item-randomizer) and its `/releases/latest`. Both 404 for visitors while that repository is private. `/releases/latest` always resolves to the newest release, so new betas need no link change.

## Themes

The look is split in two. `assets/css/base.css` is game-neutral: it owns layout, spacing, accessibility and behaviour, and declares the custom properties (knobs) in its `:root` with plain defaults — palette, fonts, wordmark lettering, button, code-block and focus-ring styling, and the height of the hero's ground. A theme dresses the page for one game on top of that.

**What a theme contains.** One folder under `assets/themes/`, holding everything the look needs:

```
assets/themes/spelunky/
  theme.css      knob values and decoration
  fonts/         self-hosted, openly licensed type, with its licence (OFL.txt)
  img/           original pixel-art textures and motifs (SVG)
```

`theme.css` sets knobs on `:root` and may add decoration — backgrounds, borders, shadows, `@font-face`, and `::before`/`::after` pseudo-elements. The page's sections (`.hero`, `.lost`, `.project`, `.testers`, `.about`, `.guide`, `.site-footer`) are positioned and isolated by the base, so decoration can be placed inside them and layered behind the content with a negative `z-index`; `.ground` is an empty strip along the bottom of the hero and the 404 page, as tall as `--ground-height`. It never changes display, size, margin, padding or grid placement of page content; the base owns those. Animations need no reduced-motion handling of their own: the base stops every animation under `prefers-reduced-motion`. Reference the bundle's files with root-relative paths (`/assets/themes/<game>/...`), and never load anything from a third-party server.

**Adding a theme.** Copy `assets/themes/spelunky/` to `assets/themes/<game>/`, replace its fonts and images, and change the knob values and decoration in its `theme.css`. An empty `theme.css` is valid and shows the base defaults, which is a quick way to check that a theme only changes the look.

**Making a theme active.** Each page names its theme in exactly one place, the second stylesheet link in its `<head>`:

```html
<link rel="stylesheet" href="/assets/css/base.css">
<link rel="stylesheet" href="/assets/themes/spelunky/theme.css">
```

Point that link at the new theme in `index.html`, `bug-report/index.html`, `404.html` and `tools/social-preview.html`. It is plain CSS loaded in the `<head>`, so it applies without JavaScript and without a flash of another look. Also set `<meta name="theme-color">` in the three pages to the theme's `--bg`: it is page metadata that follows the active theme, not a second selector. Then re-take the favicon and social preview (below) so they match.

## Deployment

GitHub Pages serves the root of `main` as-is (`.nojekyll` turns off Jekyll processing). Anything merged to `main` goes live at <https://kakudio.dev/> within a minute or two.

The `CNAME` file is the repository's half of the custom domain. The other half is outside this repository: DNS records for `kakudio.dev`, and Pages enabled in **Settings → Pages** with source *Deploy from a branch*, `main`, `/ (root)`, and *Enforce HTTPS* on. See GitHub's guide to [configuring a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

## Favicon and social preview

`assets/img/favicon.svg` is the source for the icons. `assets/img/social-preview.png` (1200×630) is a screenshot of `tools/social-preview.html` served from the repository root; the PNG icons are screenshots of the SVG at 32×32 and 180×180. Re-take them with any browser screenshot tool if the wordmark, colours or active theme change. The metadata points at `https://kakudio.dev/assets/img/social-preview.png`, so social previews only work once the site is live.
