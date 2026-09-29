# kakudio.dev

Static single-page site served by GitHub Pages from the root of `main`. **Anything merged to `main` goes live** at https://kakudio.dev/.

- Run locally: `python3 -m http.server 8000` from the repo root, open http://localhost:8000/ (and `/404.html`).
- No build step, framework or dependencies. Keep it that way.
- Randomizer details and all external links live in `config.js`; brand copy, headings and metadata live in `index.html` and must work without JavaScript.
- Unknown links stay `"PLACEHOLDER"` — never invent a Discord or spelunky.fyi URL.
- Before merging, check: page renders at ~375px and desktop widths with no horizontal scroll; no `<a>` points at a placeholder; every action is reachable by keyboard with a visible focus ring; the browser console has no errors; asset paths are root-relative and HTTPS.
