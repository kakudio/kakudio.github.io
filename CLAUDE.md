# kakudio.dev

Static single-page site served by GitHub Pages from the root of `main`. **Anything merged to `main` goes live** at https://kakudio.dev/.

- Run locally: `python3 -m http.server 8000` from the repo root, open http://localhost:8000/ (and `/404.html`).
- No build step, framework or dependencies. Keep it that way.
- The site ships no JavaScript. Every link and piece of content — randomizer details, brand copy, headings, metadata — lives in the HTML of the page that shows it.
- A link with no real URL yet is left out of the HTML — never invent a Discord or spelunky.fyi URL.
- Before merging, check: page renders at ~375px and desktop widths with no horizontal scroll; every `<a>` has a real `href`; every action is reachable by keyboard with a visible focus ring; the browser console has no errors; asset paths are root-relative and HTTPS.
