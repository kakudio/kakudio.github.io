# kakudio.dev

Static site served by GitHub Pages from the root of `main`. **Anything merged to `main` goes live** at https://kakudio.dev/.

- Run locally: `python3 -m http.server 8000` from the repo root, open http://localhost:8000/ (and `/shell-game/`, `/bug-report/`, `/404.html`).
- No build step, framework or dependencies. Keep it that way.
- The report form on `/bug-report/` is the one piece of JavaScript on the site (`bug-report/report-form.js`, loaded only by that page); every other page ships none. Every link and piece of content — randomizer details (on `/shell-game/`), brand copy, headings, metadata, and the form's labels and messages — lives in the HTML of the page that shows it.
- The bug-reporting page, `bug-report/index.html` at `/bug-report/`, holds the report service's URLs and the list of covered mods. A mod added to the service's list (`GET /api/mods`) means a new entry on that page.
- A link with no real URL yet is left out of the HTML — never invent a Discord or spelunky.fyi URL.
- Before merging, check: page renders at ~375px and desktop widths with no horizontal scroll; every `<a>` has a real `href`; every action is reachable by keyboard with a visible focus ring; the browser console has no errors; asset paths are root-relative and HTTPS.
