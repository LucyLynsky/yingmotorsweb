---
name: yingmotors-web
description: >-
  Develop and maintain the YING MOTORS static export site (Shandong Yingmotors /
  英驰汽车). Use when editing this repo, adding or removing stock, writing product
  copy, changing i18n, CSS, inquiry forms, WhatsApp, or Cloudflare R2 image URLs
  (webimages.yingmotors.com, hero.jpg, products.js, YM_IMAGES_BASE).
---

# YING MOTORS 站点开发

面向海外买家的**纯静态外贸站**：看现车、询价。无构建、无后台、无在线支付。默认英文，中文为对照。

改任何 UI / 现车 / 文案前先读本 Skill；加车、换图、写参数的逐步说明见 [reference.md](reference.md)。

## 硬约束

- 保持 HTML + CSS + 原生 JS。不要引入框架、打包器或后端。
- 产品图必须是我司实拍。禁止网图顶替现车；禁止把 `.heic` 或中文路径写进网页。
- 价格、小时数、配置不写死。询盘确认。参数是图上能看清的信息或型号常规值。
- 产品文案**看图手写**进 `js/products.js` 的 `en` / `zh`。没有 OCR、没有自动生成。
- 网页用图走 R2，不要再写相对路径 `images/...`（`assets/`、`contact/` 除外）。
- WhatsApp 号码必须是 `8618053729906`（国家码、无 `+`、无空格）。
- 已退役 SKU 禁止复用：`YM-UTK-009`、`YM-UTK-012`、`YM-UEX-006`、`YM-UEX-007`。
- 改 UI 后必须用本地 `http.server` 打开页面核对（不要用 `file://`）。

## 品牌与联系人

| 项 | 值 |
| --- | --- |
| 公司 | Shandong Yingmotors Co.,Ltd |
| 品牌 | YING MOTORS |
| 地址 | Liangshan County, Jining City, Shandong Province |
| 销售 | Kate |
| WhatsApp | +86 180 5372 9906 |
| 微信 | k18053729906 |
| 邮箱 | yingmotorsinfo@gmail.com |
| 主色 | `#E49402` / `#210E06` / 纸色 `#F6F1EA` |

改电话、邮箱、微信时同步：`js/app.js` 头尾与 WhatsApp 链接、`contact.html` 展示、`js/i18n.js` 里写死的号码/邮箱文案。

## 目录与职责

```text
index.html          首页
products.html       现车目录（?cat= ?q=）
product.html        兼容跳转（?id= → product/{id}.html，noindex）
product/{id}.html   预渲染详情（build_sitemap.py 从 products.js 生成）
custom.html         定制说明
about.html / contact.html
css/styles.css
js/i18n.js          全站中英文案（不含产品名）
js/products.js      现车数据、SKU、卡片、YM_IMAGES_BASE
js/app.js           顶栏页脚、语言、筛选、详情、询盘
js/countries.js     仅 contact.html 国家列表
assets/             Logo / Favicon / OG（本地相对路径）
contact/            微信 / WhatsApp 二维码（本地）
images/stock/       本地制图源：{sku}_{id}/ JPG、thumbs、mp4、description.md
images/products/    原片存档（中文路径、HEIC 可留在这里）
docs/               水印脚本、产品资料 Excel 生成
```

脚本顺序（contact 在 `app.js` 前多加载 `countries.js`）：

```html
<script src="js/i18n.js"></script>
<script src="js/products.js"></script>
<script src="js/app.js"></script>
```

新 HTML：`data-page` 高亮导航，`data-title` 双语标题；`<head>` 加

`<link rel="preconnect" href="https://webimages.yingmotors.com">`

顶栏/页脚/悬浮聊天由 `YM.mountChrome()` 注入，不要在五个页面各写一份。

## 图片：本地制图，R2 上线

CDN 根：`https://webimages.yingmotors.com/web/images/`

对应 bucket 对象键：`web/images/{相对路径}`，例如本地 `images/hero.jpg` →

`https://webimages.yingmotors.com/web/images/hero.jpg`

| 用途 | 写法 |
| --- | --- |
| 现车全图 / 缩略图 / 视频 | `js/products.js` 的 `YM_IMAGES_BASE` + `ymStock` / `ymVid` |
| 首页主图 | `index.html` hero `background-image` |
| 内页横幅 / 关于页图 | `css/styles.css` `.page-hero`、`about.html` `<img>` |
| Logo、favicon、二维码 | 继续相对路径 `assets/`、`contact/` |

流程：原片 → `images/stock/{sku}_{id}/`（JPG 长边约 1600px，thumb 约 960×600、16:10）→ `docs/watermark_stock.py` 打水印 → **上传到 R2 同一相对路径** → 改 `ymStock` 张数（若有增删）。

换同一文件名的图：覆盖本地 + 覆盖 R2 即可，不用改 JS。浏览器 Ctrl+F5。

## 中英文

1. 全站句子：`js/i18n.js` 的 `YM_I18N.en` / `YM_I18N.zh` 成对加键；HTML 用 `data-i18n`。
2. 产品名、导语、要点、参数：只写在该产品的 `en` / `zh`。
3. 语言键 `localStorage ym-lang`。非 `zh` 一律当 `en`。切语言会 `location.reload()`。
4. 缺键时 `YM.t` 回退英文。新增文案必须中英都有。

## 现车数据

`YM_PRODUCTS` 一条最少：`id`、`sku`、`category`（`new`|`used`）、`type`、`brand`、`images`、`thumb`；可选 `videos`、`aliases`。

`type`：`truck` / `trailer` / `tricycle` / `fourwheel` / `bus` / `excavator` / `loader` / `mixer` / `special`

筛选（`YM.matchesFilter`）：`?cat=new|used|truck|...`；`light` = 三轮+四轮；`machinery` = 挖机+装载+搅拌+环卫。搜索 `?q=` 匹配 sku / id / brand / 中英文名。

SKU：`YM-{N|U}{TYPE}-{NNN}`。同类序号永不复用。文件夹名 `{sku}_{id}`。

首页推荐：`YM_FEATURED_IDS`（建议 ≤6）。删车时必须同时从这里去掉。

加 / 删 / 换图 / 看图写文案：按 [reference.md](reference.md) 做完检查清单。

改完现车后刷新台账和预渲染详情：

```powershell
python docs/build_product_datasheet.py
python docs/build_sitemap.py
```

`build_sitemap.py` 会写 `sitemap.xml`、`sitemap.html` 和 `product/{id}.html`（每台车独立静态页，供 Google 抓取）。上线时把 `product/` 一并上传。

脚本读本地 `images/stock/`，不读 R2。本地缺文件时 Excel 会标未引用/缺失。

## 询盘

- 联系表：`YM.sendInquiryByEmail()` → Web3Forms → `yingmotorsinfo@gmail.com`。Key 在 `js/app.js` 的 `YM.WEB3FORMS_ACCESS_KEY`。换收件箱必须用新邮箱重新申请 key。
- 卡片/详情 Email 是 `mailto:`，与 Web3Forms 不是一条路径。
- WhatsApp 预填：`YM.whatsappLink(product)`，带当前语言和车型。

## 视觉

Oswald 标题 + Source Sans 3 / Noto Sans SC。断点约 980px 手机菜单、640px 单列卡片。深色顶栏 Logo 用 `assets/logo-mark-dark.svg`。

## 预览

```powershell
cd E:\codePrj\web
python -m http.server 8080
```

打开 http://127.0.0.1:8080/ 。上线只传站点文件（含 `product/`）；`images/products/` 与 HEIC 原片不必上生产。网页图以 R2 为准。
