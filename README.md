# Relogic Labs site

The site keeps its dark studio identity, home-page carousel, research and product pages, team portraits, diagrams and project media. Shared navigation and readable type connect the existing pages. The four model case studies have their own image-led page.

## Public routes

| Route | Page |
|---|---|
| `/` | Studio home |
| `/services/` | Services |
| `/research/` | Research consultancy |
| `/research/medical/`, `/research/startups/`, `/research/enterprise/` | Research desks |
| `/projects/` | Digital products |
| `/case-studies/` | Image-led case studies for four models in build |
| `/people/`, `/people/<slug>/` | Team directory and profiles |
| `/news/` or `/news` | Field Notes and studio updates |
| `/news/blogs/<slug>/` | Project-led articles |

The four case-study tracks are DEN Agentic AI, Agent Relogic, FounderCMD and ClinTx Engine. Article inspiration and source repositories are linked on each Field Note page.

## Editorial updates

Edit `data/blogs.json` and rebuild the Field Notes pages and index with:

```bash
python3 src/build_editorial.py
```

Each article has absolute Open Graph and Twitter metadata plus a local 1200 x 630 PNG with the article title. The same metadata provides preview cards in Facebook, LinkedIn and WhatsApp. Social platforms cache previews, so use their URL inspection tools to refresh a card after publishing a change.

`src/build_site.py` is a legacy migration utility for a separate set of source pages. It is not part of the current site build.

## Local development

```bash
python3 tools/serve.py
```

Open `http://127.0.0.1:4173/`. The included server resolves directory routes such as both `/news` and `/news/` to their `index.html` pages. Project intake posts to `/api/intake`; local submissions are stored in `data/leads/`.

To open the local inbox, configure a server-only key before starting the server:

```powershell
$env:RELOGIC_ADMIN_KEY = "a-long-private-value"
python tools/serve.py
```

Then open `http://127.0.0.1:4173/admin`. The server has no default key, never prints the key, sends the form by POST, and blocks direct requests for private lead and credential files.

## Credential handling

Google OAuth client secrets, service-account keys and API credentials do not belong in this static website or its browser JavaScript. Keep them in a server-only environment variable or a secret manager. `.gitignore`, `.vercelignore`, host rules and the local server block common credential filenames. No Google authentication credential was included in the supplied archive or added to this project.

## Design and assets

Shared color and readability tokens live in `assets/css/tokens.css` and `assets/css/readability.css`. Shared navigation lives in `assets/css/chrome.css` and `assets/js/site.js`. Original photos, research graphs, partner logos, favicons and brand files remain in their original paths; the new social cards live in `images/social/`.
