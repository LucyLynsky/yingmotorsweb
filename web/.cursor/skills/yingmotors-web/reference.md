# YING MOTORS 维护细则

Agent 做加车、换图、删车、写参数时按本节逐步执行。原则见 [SKILL.md](SKILL.md)。

## 1. 换图 / 换视频（已有车型）

1. 用 `product_id` 或 SKU 在 `js/products.js` 找到该条。详情地址：`product/{id}.html`（旧链 `product.html?id={id}` 会跳转过去）。
2. **换同一张：** 覆盖本地 `images/stock/{sku}_{id}/{sku}_01.jpg`（或对应序号）。文件名不要改。
3. **同步缩略图：** 覆盖 `thumbs/{sku}_0x.jpg`（列表和首页卡片用）。约 960×600、16:10。
4. **多拍了几张：** 按序加 `{sku}_03.jpg`… 及对应 thumbs。把顶部 `ymStock("sku", "id", 张数)` 改成新数量。
5. **视频：** 覆盖 `{sku}_v01.mp4`；新增则加 `{sku}_v03.mp4`，并改该产品 `videos: ymVid("sku", "id", ["v01.mp4", ...])`。建议无声 H.264。
6. 需要水印时跑 `docs/watermark_stock.py`（源图在文件夹内 `_orig/`）。
7. **上传 R2**，对象键与本地相对路径一致：`web/images/stock/{sku}_{id}/...`
8. HEIC 先转 JPG 再进 stock，例如：

```powershell
python -c "from PIL import Image; from pillow_heif import register_heif_opener; register_heif_opener(); im=Image.open(r'原图.heic').convert('RGB'); im.save(r'E:\codePrj\web\images\stock\YM-NTK-002_new-howo-cargo\YM-NTK-002_01.jpg','JPEG',quality=88)"
```

9. Ctrl+F5 打开 `product/{id}.html` 和 `products.html`。原片可另存 `images/products/NEW` 或 `USED`。
10. 运行 `python docs/build_sitemap.py`，把新的 `product/{id}.html` 和 sitemap 一并上传。

## 2. 增加一台车

1. 英文 `id`：小写字母、数字、连字符，如 `new-howo-cargo`。
2. 按规则编新 SKU（同类下一个未用序号）。退役号禁止用。
3. 原片放入 `images/products/NEW/...` 或 `USED/...`。
4. 建网页目录 `images/stock/{sku}_{id}/`：
   - `{sku}_01.jpg`、`{sku}_02.jpg`…
   - `thumbs/{sku}_01.jpg`…
   - 视频 `{sku}_v01.mp4`…
   - 描述 `{sku}_description.md`（与图同夹）
5. 打水印，上传 R2。
6. `js/products.js`：
   - 顶部 `var _xx = ymStock("YM-NTK-002", "new-howo-cargo", 4);`
   - 复制一条相近车型，改字段：

| 字段 | 填什么 |
| --- | --- |
| `id` | 与文件夹 slug 一致 |
| `sku` | `YM-NTK-002` |
| `category` | `new` 或 `used` |
| `type` | 见 SKILL `type` 列表 |
| `brand` | 图上品牌英文 |
| `images` / `thumb` | `_xx.images`、`_xx.thumb` |
| `videos` | 可选 `ymVid("YM-NTK-002", "new-howo-cargo", ["v01.mp4"])` |
| `en` / `zh` | 看图填写，见第 5 节 |

7. 首页推荐则把 `id` 写入 `YM_FEATURED_IDS`（建议不超过 6）。
8. 核对 `products.html` 筛选、`product/{新id}.html`、中英文。
9. `python docs/build_sitemap.py` 和 `python docs/build_product_datasheet.py`

## 3. 删除一台车

1. 从 `YM_PRODUCTS` 删整条对象。
2. 从 `YM_FEATURED_IDS` 去掉该 `id`。
3. 删除仅该车使用的 `var _xx = ymStock(...)`。
4. 本地 `images/stock/{sku}_{id}/` 可删；R2 上对应前缀一并删，避免脏文件。原片建议先备份。
5. 重跑 `python docs/build_sitemap.py` 和资料表。脚本会删掉已下架的 `product/{id}.html`。不要只删图不删 JS（裂图）；不要只删 JS 不删推荐 id。

## 4. 改完必查

- [ ] `products.html` 列表图来自 R2 且正常
- [ ] `product/{id}.html` 大图、缩略图、视频；无 JS 时 HTML 里仍有品名和参数
- [ ] 已运行 `python docs/build_sitemap.py`，新的 `product/*.html` 与 sitemap 已上传
- [ ] 中英文名称和参数都对
- [ ] 动过 `YM_FEATURED_IDS` 则查首页
- [ ] R2 路径与 `YM_IMAGES_BASE` + `stock/{sku}_{id}/` 一致
- [ ] 已刷新 `docs/Yingmotors-product-media-datasheet.xlsx`（若脚本输出名不同，以 `docs/` 实际文件为准）

## 5. 产品描述怎么从图片写进 `products.js`

网站不会根据新图自动写描述。打开 stock 里的 JPG（必要时对照原片）：

- 前脸 / 中网字母 → 品牌
- 型号标、车门侧标、罐体字 → 型号、马力、排放、容量
- 颜色、车身形式、轴数、高低顶、是否贴「出口」
- 拍摄环境只写进简介，不当成品参数

图上看不清的数字不要编。只看到「350 马力」写成「350 马力**级**」。有厂家文档可抄，并依赖全站 `detail_note` 免责声明（写在 `i18n.js`，不要复制进某一台的 `summary`）。

| 字段 | 从哪来 |
| --- | --- |
| `id` | 自己定的英文 slug |
| `sku` | `YM-{N\|U}{TYPE}-{NNN}`，图上没有 |
| `category` | 原图在 NEW 还是 USED |
| `type` | 车型 |
| `brand` | **图上读** |
| `en.name` / `zh.name` | 新旧 + 品牌 + 车型 + 图上型号 |
| `subtitle` | 门标 / 颜色等，用 `·` 隔开 |
| `summary` | 能确认的事写成 1～2 句 |
| `highlights` | 3～4 条短句 |
| `specs` | 同样信息改成「项目 / 值」，中英各一遍 |

实例（陕汽搅拌 `used-shacman-mixer` / `YM-UMX-002`）：中网 SHACMAN、前脸 M3000S、门标 350 马力国六、白驾驶室白罐、四轴 → 写进 name/subtitle/specs；罐体立方米看不清则不写。

## 6. SKU 类型缩写

N=新车 U=二手。TK 重卡 / TL 挂车 / TC 三轮 / FW 四轮 / BS 客车 / EX 挖机 / LD 装载机 / MX 搅拌 / SP 环卫。

退役（勿复用）：YM-UTK-009 并入 YM-UTK-010；YM-UTK-012 是 YM-UTK-001 底盘说明图；YM-UEX-006、YM-UEX-007 是 YM-UEX-001 的其它角度。
