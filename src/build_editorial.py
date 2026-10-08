#!/usr/bin/env python3
"""Build the Relogic News / Blogs index and share-ready project notes."""

from __future__ import annotations

import html
import json
import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.relogiclabs.com"

UPDATES = [
    {
        "href": "/news/updates/research-pathways/index.html",
        "date": "In development",
        "title": "Research starts with the shape of the evidence",
        "copy": "The research desks are being organized around medical, startup and enterprise questions, with source context kept close to each finding.",
        "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=400&q=70",
        "alt": "Researchers reviewing medical evidence",
    },
    {
        "href": "/news/updates/selected-work/index.html",
        "date": "In development",
        "title": "Four models, four different jobs",
        "copy": "DEN Agentic AI, Agent Relogic, FounderCMD and ClinTx Engine each start from a different user need and a different kind of evidence.",
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=400&q=70",
        "alt": "A team planning work around a table",
    },
    {
        "href": "/news/updates/media-slot/index.html",
        "date": "Product note",
        "title": "A useful model makes its reasoning inspectable",
        "copy": "The product notes focus on visible sources, clear limits and a next step a person can review.",
        "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=400&q=70",
        "alt": "A speaker presenting research to an audience",
    },
    {
        "href": "/news/updates/intake-open/index.html",
        "date": "Studio",
        "title": "Bring the difficult brief",
        "copy": "Research and product briefs can start with the question, the evidence already available and the people who need to act.",
        "image": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=400&q=70",
        "alt": "Colleagues working together in a studio",
    },
]


def local_href(page_dir: Path, target: str) -> str:
    """Return a site-root target relative to the current page directory."""
    path, separator, suffix = target.lstrip("/").partition("#")
    if not path:
        path = "index.html"
    relative = posixpath.relpath(path, page_dir.as_posix() or ".")
    return relative + (separator + suffix if separator else "")


def nav(page_dir: Path) -> str:
    links = [
        ("Home", "/index.html"),
        ("About", "/index.html#about"),
        ("Services", "/services/index.html"),
        ("Digital Product", "/projects/index.html"),
        ("Case Studies", "/case-studies/index.html"),
        ("Our People", "/people/index.html"),
        ("News / Blogs", "/news/index.html"),
    ]
    desktop = "".join(
        f'<a href="{html.escape(local_href(page_dir, href), quote=True)}">{label}</a>'
        for label, href in links
    )
    mobile = desktop + (
        f'<a href="{html.escape(local_href(page_dir, "/index.html#project-intake"), quote=True)}">Contact</a>'
    )
    home = html.escape(local_href(page_dir, "/index.html"), quote=True)
    logo = html.escape(local_href(page_dir, "/images/team/relogic-logo-transparent.png"), quote=True)
    contact = html.escape(local_href(page_dir, "/index.html#project-intake"), quote=True)
    return f'''<div class="nav-shell" id="navShell">
    <nav class="nav" aria-label="Primary navigation">
      <a href="{home}" class="brand" aria-label="Relogic home"><span class="brand-mark"><img src="{logo}" alt="Relogic Labs"></span></a>

      <div class="nav-links">{desktop}</div>

      <div class="nav-actions">
        <a class="nav-cta" href="{contact}">Start a project</a>
        <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false"><span class="hamburger" aria-hidden="true"><b></b><b></b><b></b></span></button>
      </div>
    </nav>

    <div class="mobile-menu" id="mobileMenu">{mobile}</div>
  </div>'''


def footer(page_dir: Path) -> str:
    home = html.escape(local_href(page_dir, "/index.html"), quote=True)
    logo = html.escape(local_href(page_dir, "/images/team/relogic-logo-transparent.png"), quote=True)
    links = [
        ("About", "/index.html#about"),
        ("Services", "/services/index.html"),
        ("Research", "/research/index.html"),
        ("Digital Product", "/projects/index.html"),
        ("Case Studies", "/case-studies/index.html"),
        ("Our People", "/people/index.html"),
        ("News / Blogs", "/news/index.html"),
        ("Contact", "/index.html#project-intake"),
    ]
    rendered_links = "".join(
        f'<a href="{html.escape(local_href(page_dir, href), quote=True)}">{label}</a>'
        for label, href in links
    )
    script = html.escape(local_href(page_dir, "/assets/js/site.js"), quote=True)
    return f'''<footer class="rl-footer">
  <div class="container"><div class="footer-grid">
    <div><a href="{home}" class="brand" aria-label="Relogic home"><span class="brand-mark"><img src="{logo}" alt="Relogic Labs"></span></a>
      <p class="footer-copy">Research, AI, data intelligence and digital products for decisions that need a visible path from evidence to action.</p></div>
    <div class="footer-links">{rendered_links}</div>
  </div><div class="copyright">© 2026 Relogic Solutions. Built around evidence, data and useful intelligence.</div></div>
</footer><script src="{script}" defer></script>'''


def card(post: dict, featured: bool = False) -> str:
    page_dir = Path("news")
    slug = html.escape(post["slug"], quote=True)
    title = html.escape(post["title"])
    excerpt = html.escape(post["excerpt"])
    category = html.escape(post["category"])
    image = html.escape(post["index_image"], quote=True)
    alt = html.escape(post["index_image_alt"], quote=True)
    target = html.escape(local_href(page_dir, f"/news/blogs/{slug}/index.html"), quote=True)
    featured_class = " featured" if featured else ""
    return f'''<a class="blog-card{featured_class}" href="{target}">
        <figure><img src="{image}" alt="{alt}" loading="lazy" width="1200" height="630"></figure>
        <div class="copy"><div class="meta">{category}</div><h3>{title}</h3><p>{excerpt}</p><span class="read">Read article →</span></div>
      </a>'''


def update_card(item: dict) -> str:
    return f'''<a class="news-item" href="{html.escape(local_href(Path("news"), item["href"]), quote=True)}">
        <figure><img src="{html.escape(item["image"], quote=True)}" alt="{html.escape(item["alt"], quote=True)}" loading="lazy" width="400" height="300"></figure>
        <div><div class="when">{html.escape(item["date"])}</div><h3>{html.escape(item["title"])}</h3><p>{html.escape(item["copy"])}</p><span class="chip">Studio note</span></div>
      </a>'''


def write_index(posts: list[dict]) -> None:
    page_dir = Path("news")
    blog_cards = "\n".join(card(post, i == 0) for i, post in enumerate(posts))
    updates = "\n".join(update_card(item) for item in UPDATES)
    nav_markup = nav(page_dir)
    footer_markup = footer(page_dir)
    css = html.escape(local_href(page_dir, "/assets/css/editorial.css"), quote=True)
    meta_image = f"{SITE}/images/social/blog-hub.png"
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{SITE}/news">
  <link rel="icon" href="/assets/brand/relogic-labs-favicon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="/assets/brand/relogic-labs-apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="{html.escape(local_href(page_dir, "/site.webmanifest"), quote=True)}">
  <meta name="theme-color" content="#050816">
  <title>News &amp; Blogs · Relogic Labs</title>
  <meta name="description" content="Project notes and studio updates on research, applied AI, business planning and useful decisions.">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Relogic Labs">
  <meta property="og:title" content="News &amp; Blogs · Relogic Labs">
  <meta property="og:description" content="Project notes and studio updates on research, applied AI, business planning and useful decisions.">
  <meta property="og:url" content="{SITE}/news">
  <meta property="og:image" content="{meta_image}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Relogic project notes and studio updates">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="News &amp; Blogs · Relogic Labs">
  <meta name="twitter:description" content="Project notes and studio updates on research, applied AI, business planning and useful decisions.">
  <meta name="twitter:image" content="{meta_image}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{html.escape(local_href(page_dir, "/assets/css/tokens.css"), quote=True)}">
  <link rel="stylesheet" href="{html.escape(local_href(page_dir, "/assets/css/chrome.css"), quote=True)}">
  <link rel="stylesheet" href="{html.escape(local_href(page_dir, "/assets/css/readability.css"), quote=True)}">
  <link rel="stylesheet" href="{css}">
</head>
<body class="desk-page">
<a class="rl-skip" href="#main">Skip to content</a>
{nav_markup}
<main id="main">
  <section class="desk-hero">
    <div class="container">
      <div class="kicker">Desk · Notes and signal</div>
      <h1>Research begins with a signal.<br><span>Better questions come next.</span></h1>
      <p>Project notes turn public work into practical questions about product research, model evaluation, business planning and the decisions that follow.</p>
    </div>
  </section>

  <section class="desk" aria-label="Blogs and studio news">
    <div class="col">
      <div class="col-head"><div><small>01 / Studio desk</small><h2>Blogs</h2></div><em>Method, product, research</em></div>
      {blog_cards}
    </div>
    <div class="col">
      <div class="col-head"><div><small>02 / Studio updates</small><h2>News &amp; media</h2></div><em>Products, research, studio</em></div>
      {updates}
      <a class="news-cta" href="{html.escape(local_href(page_dir, "/case-studies/index.html"), quote=True)}">Explore the case studies →</a>
      <a class="news-cta" href="{html.escape(local_href(page_dir, "/index.html#project-intake"), quote=True)}">Start a research or product brief →</a>
    </div>
  </section>
</main>
{footer_markup}
</body>
</html>
'''
    (ROOT / "news" / "index.html").write_text(page, encoding="utf-8")


def article_page(post: dict) -> str:
    slug = html.escape(post["slug"], quote=True)
    page_dir = Path("news") / "blogs" / post["slug"]
    title = html.escape(post["title"])
    excerpt = html.escape(post["excerpt"])
    category = html.escape(post["category"])
    repo = html.escape(post["repo"])
    repo_url = html.escape(post["repo_url"], quote=True)
    share_image = html.escape(post["image"], quote=True)
    article_image = html.escape(post["index_image"], quote=True)
    article_alt = html.escape(post["index_image_alt"], quote=True)
    canonical = f"{SITE}/news/blogs/{slug}"
    body = []
    for section in post["sections"]:
        heading = html.escape(section["heading"])
        paragraphs = "\n".join(f"<p>{html.escape(text)}</p>" for text in section["paragraphs"])
        body.append(f"<h2>{heading}</h2>{paragraphs}")
    article_body = "\n".join(body)
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["excerpt"],
        "datePublished": "2026-10-08",
        "author": {"@type": "Organization", "name": "Relogic Labs"},
        "publisher": {"@type": "Organization", "name": "Relogic Labs", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/brand/relogic-labs-organization-logo.png"}},
        "image": f"{SITE}/images/social/{share_image}",
        "mainEntityOfPage": canonical,
    }
    schema_json = json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")
    local = lambda target: html.escape(local_href(page_dir, target), quote=True)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="/assets/brand/relogic-labs-favicon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="/assets/brand/relogic-labs-apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="{local("/site.webmanifest")}">
  <meta name="theme-color" content="#050816">
  <title>{title} · Relogic Labs</title>
  <meta name="description" content="{html.escape(post["excerpt"], quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Relogic Labs">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{html.escape(post["excerpt"], quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/images/social/{share_image}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Relogic Field Note: {title}">
  <meta property="article:published_time" content="2026-10-08">
  <meta property="article:author" content="Relogic Labs">
  <meta property="article:section" content="{category}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{html.escape(post["excerpt"], quote=True)}">
  <meta name="twitter:image" content="{SITE}/images/social/{share_image}">
  <meta name="twitter:image:alt" content="Relogic Field Note: {title}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{local("/assets/css/tokens.css")}">
  <link rel="stylesheet" href="{local("/assets/css/chrome.css")}">
  <link rel="stylesheet" href="{local("/assets/css/readability.css")}">
  <link rel="stylesheet" href="{local("/assets/css/editorial.css")}">
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="desk-page">
<a class="rl-skip" href="#main">Skip to content</a>
{nav(page_dir)}
<main id="main">
  <article class="article">
    <div class="crumb"><a href="{local("/news/index.html")}">News / Blogs</a> · Project note</div>
    <h1>{title}</h1>
    <p class="lede">{excerpt}</p>
    <figure class="hero-pic"><img src="{article_image}" alt="{article_alt}" width="1200" height="630" fetchpriority="high"></figure>
    <div class="body">{article_body}
      <p class="project-source"><a href="{repo_url}" target="_blank" rel="noopener noreferrer">Explore the project repository · {repo} ↗</a></p>
    </div>
    <a class="back" href="{local("/news/index.html")}">← Back to News / Blogs</a>
  </article>
</main>
{footer(page_dir)}
</body>
</html>
'''


def main() -> None:
    posts = json.loads((ROOT / "data" / "blogs.json").read_text(encoding="utf-8"))
    for post in posts:
        destination = ROOT / "news" / "blogs" / post["slug"] / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(article_page(post), encoding="utf-8")
    write_index(posts)
    print(f"Built {len(posts)} project notes and the News / Blogs index.")


if __name__ == "__main__":
    main()
