# -*- coding: utf-8 -*-
"""Write sitemap.xml and sitemap.html from js/products.js. Run after adding or removing stock."""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(r"E:\codePrj\web")
JS = (ROOT / "js" / "products.js").read_text(encoding="utf-8")
SITE = "https://yingmotors.com"
TODAY = date.today().isoformat()

TYPE_ORDER = [
    ("truck", "Trucks", "重卡"),
    ("trailer", "Trailers", "挂车"),
    ("tricycle", "Tricycles", "三轮车"),
    ("fourwheel", "UTV / 4WD", "四轮"),
    ("bus", "Buses", "客车"),
    ("excavator", "Excavators", "挖掘机"),
    ("loader", "Loaders", "装载机"),
    ("mixer", "Mixers", "搅拌车"),
    ("special", "Sanitation", "环卫车"),
]


def field(block: str, name: str) -> str:
    m = re.search(rf'\b{name}:\s*"([^"]*)"', block)
    return m.group(1) if m else ""


def lang_name(block: str, lang: str) -> str:
    m = re.search(rf"{lang}:\s*\{{(.*?)\n    \}}", block, re.S)
    if not m:
        return ""
    n = re.search(r'name:\s*"([^"]*)"', m.group(1))
    return n.group(1) if n else ""


def parse_products(src: str) -> list[dict]:
    body = src.split("window.YM_PRODUCTS = [", 1)[1].split("];", 1)[0]
    products = []
    for chunk in re.split(r"\n  \{\n", body):
        if "id:" not in chunk:
            continue
        block = "  {\n" + chunk
        pid = field(block, "id")
        if not pid:
            continue
        products.append(
            {
                "id": pid,
                "sku": field(block, "sku"),
                "type": field(block, "type"),
                "name_en": lang_name(block, "en"),
                "name_zh": lang_name(block, "zh"),
            }
        )
    return products


def xml_url(loc: str, priority: str) -> str:
    return (
        "  <url>\n"
        f"    <loc>{html.escape(loc, quote=True)}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def write_xml(products: list[dict]) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n',
        xml_url(SITE + "/", "1.0"),
        xml_url(SITE + "/products.html", "0.9"),
        xml_url(SITE + "/custom.html", "0.8"),
        xml_url(SITE + "/about.html", "0.7"),
        xml_url(SITE + "/contact.html", "0.8"),
        xml_url(SITE + "/sitemap.html", "0.4"),
    ]
    for p in products:
        parts.append(xml_url(f"{SITE}/product.html?id={p['id']}", "0.7"))
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("".join(parts), encoding="utf-8")


def write_html(products: list[dict]) -> None:
    by_type: dict[str, list[dict]] = {}
    for p in products:
        by_type.setdefault(p["type"], []).append(p)

    groups = []
    for key, en, zh in TYPE_ORDER:
        items = by_type.get(key) or []
        if not items:
            continue
        links = []
        for p in items:
            label = p["sku"] + " · " + (p["name_en"] or p["id"])
            links.append(
                f'          <li><a href="product.html?id={html.escape(p["id"], quote=True)}">{html.escape(label)}</a></li>'
            )
        groups.append(
            "        <section>\n"
            f"          <h2>{html.escape(en)} / {html.escape(zh)}</h2>\n"
            "          <ul>\n"
            + "\n".join(links)
            + "\n          </ul>\n"
            "        </section>"
        )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sitemap · YING MOTORS</title>
  <meta name="description" content="Sitemap of Shandong Yingmotors: stock list, trucks, trailers, excavators, contact Kate.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/sitemap.html">
  <link rel="sitemap" type="application/xml" title="Sitemap" href="{SITE}/sitemap.xml">
  <link rel="icon" href="assets/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#210E06">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE}/sitemap.html">
  <meta property="og:title" content="Sitemap · YING MOTORS">
  <meta property="og:description" content="All public pages and stock units from Shandong Yingmotors.">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg">
  <link rel="preconnect" href="https://webimages.yingmotors.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Oswald:wght@400;500;600&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body data-title="sitemap_title">
  <header class="site-header" id="site-header"></header>
  <section class="page-hero">
    <div class="wrap">
      <p class="kicker">YING MOTORS</p>
      <h1 data-i18n="sitemap_title">Sitemap</h1>
      <p class="lead" data-i18n="sitemap_lead">All public pages and stock units.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap sitemap-cols">
      <section>
        <h2 data-i18n="sitemap_pages">Pages</h2>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="products.html">Stock</a></li>
          <li><a href="custom.html">Customize</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </section>
{chr(10).join(groups)}
    </div>
  </section>
  <footer class="site-footer" id="site-footer"></footer>
  <script src="js/i18n.js"></script>
  <script src="js/products.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
"""
    (ROOT / "sitemap.html").write_text(page, encoding="utf-8")


def main() -> None:
    products = parse_products(JS)
    write_xml(products)
    write_html(products)
    print(f"Wrote sitemap.xml and sitemap.html ({len(products)} products)")


if __name__ == "__main__":
    main()
