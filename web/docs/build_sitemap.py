# -*- coding: utf-8 -*-
"""Write sitemap.xml, sitemap.html and prerendered product/*.html from js/products.js.

Run after adding or removing stock. Generated product pages must be uploaded with the site.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(r"E:\codePrj\web")
JS_PATH = ROOT / "js" / "products.js"
JS = JS_PATH.read_text(encoding="utf-8")
SITE = "https://yingmotors.com"
TODAY = date.today().isoformat()
IMAGES_BASE = (
    re.search(r'YM_IMAGES_BASE\s*=\s*"([^"]+)"', JS).group(1)
    if re.search(r'YM_IMAGES_BASE\s*=\s*"([^"]+)"', JS)
    else "https://webimages.yingmotors.com/web/images/"
)
WA = "https://wa.me/8618053729906"
MAIL = "yingmotorsinfo@gmail.com"
DETAIL_NOTE = (
    "Parameters shown in the product description are typical reference values. "
    "Final specifications are subject to the contract / technical agreement confirmed by both parties. "
    "Customization is available; please contact our sales team for details."
)

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

TYPE_FILTER = {
    "truck": "truck",
    "trailer": "trailer",
    "tricycle": "light",
    "fourwheel": "light",
    "bus": "bus",
    "excavator": "excavator",
    "loader": "loader",
    "mixer": "mixer",
    "special": "special",
}

TYPE_LABEL = {key: en for key, en, _zh in TYPE_ORDER}


def field(block: str, name: str) -> str:
    m = re.search(rf'\b{name}:\s*"([^"]*)"', block)
    return m.group(1) if m else ""


def lang_fields(block: str, lang: str) -> dict:
    m = re.search(rf"{lang}:\s*\{{(.*?)\n    \}}", block, re.S)
    src = m.group(1) if m else ""

    def s(name: str) -> str:
        mm = re.search(rf'\b{name}:\s*"([^"]*)"', src)
        return mm.group(1) if mm else ""

    hm = re.search(r"highlights:\s*\[(.*?)\]", src, re.S)
    highlights = re.findall(r'"([^"]*)"', hm.group(1)) if hm else []
    specs = re.findall(r'\["([^"]*)",\s*"([^"]*)"\]', src)
    return {
        "name": s("name"),
        "subtitle": s("subtitle"),
        "summary": s("summary"),
        "highlights": highlights,
        "specs": specs,
    }


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
        sku = field(block, "sku")
        en = lang_fields(block, "en")
        zh = lang_fields(block, "zh")
        products.append(
            {
                "id": pid,
                "sku": sku,
                "type": field(block, "type"),
                "category": field(block, "category"),
                "brand": field(block, "brand"),
                "en": en,
                "zh": zh,
                "name_en": en["name"],
                "name_zh": zh["name"],
                "image": f"{IMAGES_BASE}stock/{sku}_{pid}/{sku}_01.jpg",
            }
        )
    return products


def product_href(pid: str) -> str:
    return f"product/{pid}.html"


def product_url(pid: str) -> str:
    return f"{SITE}/{product_href(pid)}"


def seo_title(name: str) -> str:
    n = (name or "").strip().rstrip(".")
    if re.search(r"\bfor export\b", n, re.I):
        return f"{n} | YING MOTORS"
    return f"{n} for Export | YING MOTORS"


def seo_desc(summary: str) -> str:
    text = (summary or "").strip()
    if not text:
        return (
            "Export stock from Shandong Yingmotors in Liangshan, China. "
            "WhatsApp Kate for photos and FOB / CIF quotation."
        )
    return text


def xml_url(loc: str, priority: str, image: str | None = None, image_title: str | None = None) -> str:
    extra = ""
    if image:
        extra = (
            "    <image:image>\n"
            f"      <image:loc>{html.escape(image, quote=True)}</image:loc>\n"
            f"      <image:title>{html.escape(image_title or '', quote=True)}</image:title>\n"
            "    </image:image>\n"
        )
    return (
        "  <url>\n"
        f"    <loc>{html.escape(loc, quote=True)}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        f"    <priority>{priority}</priority>\n"
        f"{extra}"
        "  </url>\n"
    )


def write_xml(products: list[dict]) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n',
        xml_url(SITE + "/", "1.0"),
        xml_url(SITE + "/products.html", "0.9"),
        xml_url(SITE + "/custom.html", "0.8"),
        xml_url(SITE + "/about.html", "0.7"),
        xml_url(SITE + "/contact.html", "0.8"),
        xml_url(SITE + "/sitemap.html", "0.3"),
    ]
    for p in products:
        parts.append(xml_url(product_url(p["id"]), "0.8", p["image"], p["name_en"]))
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("".join(parts), encoding="utf-8")


def write_html_sitemap(products: list[dict]) -> None:
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
            href = html.escape(product_href(p["id"]), quote=True)
            links.append(f"          <li><a href=\"{href}\">{html.escape(label)}</a></li>")
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
  <meta property="og:site_name" content="YING MOTORS">
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


def stock_list_html(products: list[dict]) -> str:
    items = []
    for p in products:
        label = (p["sku"] + " · " if p["sku"] else "") + (p["name_en"] or p["id"])
        href = html.escape(product_href(p["id"]), quote=True)
        items.append(f'          <li><a href="{href}">{html.escape(label)}</a></li>')
    return "\n".join(items)


def patch_products_noscript(products: list[dict]) -> None:
    path = ROOT / "products.html"
    text = path.read_text(encoding="utf-8")
    start = "<!-- YM-STOCK-LIST -->"
    end = "<!-- /YM-STOCK-LIST -->"
    if start not in text or end not in text:
        raise SystemExit("products.html is missing YM-STOCK-LIST markers")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    path.write_text(before + start + "\n" + stock_list_html(products) + "\n          " + end + after, encoding="utf-8")


def greeting(sku: str) -> str:
    if sku:
        return f"Hello, I found you from the Yingmotors website. I am interested in STOCK NO {sku}."
    return "Hello, I found you from the Yingmotors website."


def write_product_page(p: dict) -> None:
    en = p["en"]
    name = en["name"] or p["id"]
    title = seo_title(name)
    desc = seo_desc(en["summary"] or en["subtitle"] or name)
    page_url = product_url(p["id"])
    image = p["image"]
    sku = p["sku"]
    badge = "Used" if p["category"] == "used" else "New"
    type_label = TYPE_LABEL.get(p["type"], "Stock")
    cat = TYPE_FILTER.get(p["type"], "all")
    cat_href = f"products.html?cat={cat}"
    greet = greeting(sku)
    wa = f"{WA}?text={quote(greet)}"
    mail_href = (
        f"mailto:{MAIL}?subject={quote(('STOCK NO ' + sku + ' — Yingmotors') if sku else 'Inquiry — Yingmotors')}"
        f"&body={quote(greet)}"
    )
    spec_rows = ([("Stock No.", sku)] if sku else []) + list(en["specs"])
    highlights = "".join(f"<li>{html.escape(h)}</li>" for h in en["highlights"])
    spec_html = "".join(
        f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>" for k, v in spec_rows
    )
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Stock", "item": SITE + "/products.html"},
                    {"@type": "ListItem", "position": 3, "name": type_label, "item": SITE + "/" + cat_href},
                    {"@type": "ListItem", "position": 4, "name": name, "item": page_url},
                ],
            },
            {
                "@type": "Vehicle",
                "name": name,
                "sku": sku or p["id"],
                "brand": {"@type": "Brand", "name": p["brand"] or "YING MOTORS"},
                "description": en["summary"] or desc,
                "image": image,
                "url": page_url,
                "mileageFromOdometer": None,
                "offers": {
                    "@type": "Offer",
                    "availability": "https://schema.org/InStock",
                    "url": page_url,
                    "seller": {
                        "@type": "Organization",
                        "name": "Shandong Yingmotors Co.,Ltd",
                        "url": SITE + "/",
                    },
                },
            },
        ],
    }
    jsonld["@graph"][1].pop("mileageFromOdometer")
    json_text = json.dumps(jsonld, ensure_ascii=False, indent=2)

    e = html.escape
    eq = lambda s: html.escape(s, quote=True)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{eq(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{eq(page_url)}">
  <link rel="sitemap" type="application/xml" title="Sitemap" href="{SITE}/sitemap.xml">
  <base href="../">
  <link rel="icon" href="assets/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#210E06">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="YING MOTORS">
  <meta property="og:url" content="{eq(page_url)}">
  <meta property="og:title" content="{eq(title)}">
  <meta property="og:description" content="{eq(desc)}">
  <meta property="og:image" content="{eq(image)}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{json_text}
  </script>
  <link rel="preconnect" href="https://webimages.yingmotors.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Oswald:wght@400;500;600&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body data-page="products" data-product-id="{eq(p['id'])}">
  <header class="site-header" id="site-header"></header>
  <section class="section">
    <div class="wrap" id="product-detail">
      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="index.html">Home</a>
        <span aria-hidden="true">/</span>
        <a href="products.html">Stock</a>
        <span aria-hidden="true">/</span>
        <a href="{eq(cat_href)}">{e(type_label)}</a>
        <span aria-hidden="true">/</span>
        <span>{e(name)}</span>
      </nav>
      <a class="back-link" href="products.html">Back to stock</a>
      <div class="detail-grid">
        <div class="detail-gallery">
          <img src="{eq(image)}" alt="{eq(name)}">
        </div>
        <div class="detail-info">
          <span class="badge">{e(badge)}</span>
          {f'<p class="detail-sku"><span>Stock No.</span> {e(sku)}</p>' if sku else ''}
          <p class="card-brand">{e(p['brand'])}</p>
          <h1>{e(name)}</h1>
          <p class="lead">{e(en['subtitle'])}</p>
          <p>{e(en['summary'])}</p>
          <p class="spec-disclaimer">{e(DETAIL_NOTE)}</p>
          <ul class="highlights">{highlights}</ul>
          <div class="detail-actions">
            <a class="btn btn-gold" href="{eq(wa)}" target="_blank" rel="noopener">Ask for this unit</a>
            <a class="btn btn-ghost" href="{eq(mail_href)}">Email</a>
          </div>
        </div>
      </div>
      <section class="specs-block">
        <h2>Specifications</h2>
        <table class="spec-table">{spec_html}</table>
        <p class="spec-disclaimer">{e(DETAIL_NOTE)}</p>
      </section>
    </div>
  </section>
  <footer class="site-footer" id="site-footer"></footer>
  <script src="js/i18n.js"></script>
  <script src="js/products.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
"""
    out = ROOT / "product" / f"{p['id']}.html"
    out.write_text(page, encoding="utf-8")


def write_product_pages(products: list[dict]) -> None:
    folder = ROOT / "product"
    folder.mkdir(exist_ok=True)
    keep = {f"{p['id']}.html" for p in products}
    for old in folder.glob("*.html"):
        if old.name not in keep:
            old.unlink()
    for p in products:
        write_product_page(p)


def main() -> None:
    products = parse_products(JS)
    if not products:
        raise SystemExit("No products parsed from js/products.js")
    missing = [p["id"] for p in products if not p["name_en"]]
    if missing:
        raise SystemExit("Missing English name: " + ", ".join(missing))
    write_xml(products)
    write_html_sitemap(products)
    write_product_pages(products)
    patch_products_noscript(products)
    sample = next(p for p in products if p["id"] == "used-howo-dump-red") if any(
        p["id"] == "used-howo-dump-red" for p in products
    ) else products[0]
    print(f"Wrote sitemap + {len(products)} product pages")
    print("Example title:", seo_title(sample["name_en"]))


if __name__ == "__main__":
    main()
