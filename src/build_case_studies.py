#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path

from portable_links import portable_html

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.relogiclabs.com"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def navigation() -> str:
    links = [
        ("Home", "/"),
        ("About", "/#about"),
        ("Services", "/services"),
        ("Digital Product", "/projects"),
        ("Case Studies", "/case-studies"),
        ("Our People", "/people"),
        ("News / Blogs", "/news"),
    ]
    desktop = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    mobile = desktop + '<a href="/#project-intake">Contact</a>'
    return f'''<div class="nav-shell" id="navShell">
  <nav class="nav" aria-label="Primary navigation">
    <a href="/" class="brand" aria-label="Relogic home"><span class="brand-mark"><img src="/images/team/relogic-logo-transparent.png" alt="Relogic Labs"></span></a>
    <div class="nav-links">{desktop}</div>
    <div class="nav-actions">
      <a class="nav-cta" href="/#project-intake">Start a project</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false"><span class="hamburger" aria-hidden="true"><b></b><b></b><b></b></span></button>
    </div>
  </nav>
  <div class="mobile-menu" id="mobileMenu">{mobile}</div>
</div>'''


def footer() -> str:
    return '''<footer class="rl-footer"><div class="cs-wrap"><div class="footer-grid">
  <div><a href="/" class="brand" aria-label="Relogic home"><span class="brand-mark"><img src="/images/team/relogic-logo-transparent.png" alt="Relogic Labs"></span></a>
    <p class="footer-copy">Research, AI, data intelligence and digital products for decisions that need a visible path from evidence to action.</p></div>
  <div class="footer-links"><a href="/#about">About</a><a href="/services">Services</a><a href="/research">Research</a><a href="/projects">Digital Product</a><a href="/case-studies">Case Studies</a><a href="/people">Our People</a><a href="/news">News / Blogs</a><a href="/#project-intake">Contact</a></div>
</div><div class="copyright">© 2026 Relogic Solutions. Built around evidence, data and useful intelligence.</div></div></footer>
<script src="/assets/js/site.js" defer></script>'''


def section_markup(section: dict) -> str:
    paragraphs = "\n".join(f"<p>{esc(p)}</p>" for p in section.get("paragraphs", []))
    bullets = ""
    if section.get("bullets"):
        items = "\n".join(f"<li>{esc(item)}</li>" for item in section["bullets"])
        bullets = f"<ul class=\"cs-detail-list\">{items}</ul>"
    return f'''<section class="cs-detail-section" id="{esc(section['id'])}">
  <h2>{esc(section['title'])}</h2>
  {paragraphs}
  {bullets}
</section>'''


def page(project: dict, projects: list[dict]) -> str:
    slug = esc(project["slug"])
    title = esc(project["title"])
    description = esc(project["summary"])
    canonical = f"{SITE}/case-studies/{slug}"
    image = esc(project["og_image"])
    status = esc(project["status"])
    pipeline = "".join(
        f'<li><span class="cs-pipeline-number">{index:02d}</span><strong>{esc(step["title"])}</strong><p>{esc(step["detail"])}</p></li>'
        for index, step in enumerate(project["pipeline"], 1)
    )
    sections = "\n".join(section_markup(section) for section in project["sections"])
    toc = "".join(
        f'<a href="#{esc(section["id"])}">{esc(section["title"])}</a>'
        for section in project["sections"]
    )
    related = "".join(
        f'''<a class="cs-related-card" href="/case-studies/{esc(other['slug'])}">
  <span>{esc(other['track'])}</span><strong>{esc(other['title'])}</strong><em>Read technical case study →</em>
</a>'''
        for other in projects if other["slug"] != project["slug"]
    )
    photo_alt = esc(project["image_alt"])
    photo_credit = esc(project["photo_credit"])
    photo_credit_url = esc(project["photo_credit_url"])
    schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": project["title"],
        "description": project["summary"],
        "image": project["og_image"],
        "mainEntityOfPage": canonical,
        "author": {"@type": "Organization", "name": "Relogic Labs"},
        "publisher": {
            "@type": "Organization",
            "name": "Relogic Labs",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/brand/relogic-labs-organization-logo.png"},
        },
    }
    schema_json = json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#050816">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="/favicon.ico" type="image/x-icon" sizes="16x16 32x32 48x48 64x64 96x96 128x128 192x192">
  <link rel="apple-touch-icon" href="/assets/brand/relogic-labs-apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Relogic Labs">
  <meta property="og:title" content="{title} · Technical Case Study · Relogic Labs">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{photo_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} · Technical Case Study · Relogic Labs">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/chrome.css">
  <link rel="stylesheet" href="/assets/css/readability.css">
  <link rel="stylesheet" href="/assets/css/case-study-page.css">
  <link rel="stylesheet" href="/assets/css/case-study-detail.css">
  <script type="application/ld+json">{schema_json}</script>
  <title>{title} · Technical Case Study · Relogic Labs</title>
</head>
<body class="cs-page cs-detail-page">
<a class="rl-skip" href="#main">Skip to content</a>
{navigation()}
<main id="main">
  <section class="cs-detail-hero">
    <div class="cs-wrap">
      <a class="cs-detail-back" href="/case-studies">← All case studies</a>
      <div class="cs-detail-hero-grid">
        <div class="cs-detail-intro">
          <div class="cs-kicker">{esc(project['kicker'])}</div>
          <h1>{title}</h1>
          <p class="cs-detail-lede">{description}</p>
          <div class="cs-detail-status"><span></span>{status}</div>
          <a class="cs-detail-primary" href="/#project-intake">Discuss a similar system <span aria-hidden="true">↗</span></a>
        </div>
        <figure class="cs-detail-image">
          <img src="{esc(project['image'])}" alt="{photo_alt}" fetchpriority="high" width="1400" height="1000">
          <figcaption>Photo by <a href="{photo_credit_url}" target="_blank" rel="noopener noreferrer">{photo_credit}</a></figcaption>
        </figure>
      </div>
    </div>
  </section>
  <section class="cs-detail-body cs-wrap">
    <aside class="cs-detail-aside">
      <div class="cs-aside-fact"><small>BUILD STAGE</small><strong>{status}</strong></div>
      <div class="cs-aside-fact"><small>PRODUCT TRACK</small><strong>{esc(project['track'])}</strong></div>
      <div class="cs-aside-fact"><small>PRIMARY USERS</small><strong>{esc(project['audience'])}</strong></div>
      <nav class="cs-detail-toc" aria-label="On this page"><span>IN THIS WRITE-UP</span>{toc}</nav>
    </aside>
    <article class="cs-technical-writeup">
      <div class="cs-build-note"><strong>Technical direction · in development</strong><p>This write-up describes the system intent and engineering approach for an active build. It does not claim shipped functionality, measured performance, regulatory approval or customer outcomes that have not been published.</p></div>
      <p class="cs-outcome-line"><span>Design objective</span>{esc(project['design_goal'])}</p>
      <section class="cs-pipeline-section" aria-labelledby="cs-pipeline-title">
        <div class="cs-kicker">System outline</div><h2 id="cs-pipeline-title">A traceable path from input to outcome.</h2>
        <ol class="cs-pipeline">{pipeline}</ol>
      </section>
      {sections}
    </article>
  </section>
  <section class="cs-related-section cs-wrap" aria-labelledby="cs-related-title">
    <div class="cs-kicker">More model builds</div>
    <h2 id="cs-related-title">Related case studies</h2>
    <div class="cs-related-grid">{related}</div>
    <a class="cs-all-cases" href="/case-studies">View all case studies ↑</a>
  </section>
</main>
{footer()}
</body>
</html>
'''


def main() -> None:
    projects = json.loads((ROOT / "data" / "case-studies.json").read_text(encoding="utf-8"))
    for project in projects:
        destination = ROOT / "case-studies" / project["slug"] / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(portable_html(ROOT, destination.relative_to(ROOT), page(project, projects)), encoding="utf-8")
        print(f"Built {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
