# Relogic project structure

This static site preserves the original studio design and existing media while connecting its pages through shared navigation and styles.

```
relogic-site/
├── index.html                 Home and studio
├── services/index.html        Services
├── research/index.html        Research consultancy
├── projects/index.html        Digital products
├── case-studies/index.html    Image-led case studies
├── people/index.html          Team directory
├── people/                    Individual profile pages
├── news/index.html            Field Notes and studio updates
├── news/blogs/                Project-led articles
├── news/updates/              Studio updates
├── assets/
│   ├── brand/                 Favicons, logo and home social preview
│   ├── css/                   Shared and page-specific styles
│   └── js/site.js             Shared navigation and interaction behavior
├── data/                      Site, team, project and editorial records
├── src/build_editorial.py     Build Field Notes pages from blogs.json
├── images/                    Original media plus generated social cards
├── tools/serve.py             Local preview, intake API and protected inbox
├── robots.txt / sitemap.xml
├── _headers / _redirects / .htaccess / vercel.json
└── .well-known/security.txt
```

The `/case-studies/` page presents DEN Agentic AI, Agent Relogic, FounderCMD and ClinTx Engine with sourced photography. Field Note articles link to the public GitHub projects that inspired them and publish absolute social metadata with a title-bearing local PNG.

Keep the original image and research asset paths intact when replacing media. Local secrets belong outside the public site directory; use server environment variables for private credentials.
