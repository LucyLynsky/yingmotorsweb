# YING MOTORS 外贸网站

山东英驰汽车（Shandong Yingmotors Co.,Ltd）面向海外买家的静态外贸站点：展示现车、支持中英文切换、通过 WhatsApp / 邮箱询盘。

本地预览：

```powershell
cd E:\codePrj\web
python -m http.server 8080
```

浏览器打开 http://127.0.0.1:8080/

---

## 1. 网站开发需求关键点

### 1.1 业务目标

- 做给海外客户看的外贸站，不是维修占位页。
- 核心动作是看现车、询价，不需要在线支付或后台登录。
- 销售对接人固定为 Kate，询盘走 WhatsApp 和邮箱。

### 1.2 语言

- 必须支持中英文切换。
- 外贸站默认英文；中文用于国内同事核对和部分中文买家。
- 导航、首页、产品名、参数、关于我们、联系页、页脚都要双语。
- 语言选择需要记住，刷新或换页后保持。

### 1.3 品牌与联系方式（必须与资料一致）

| 项 | 内容 |
| --- | --- |
| 公司 | Shandong Yingmotors Co.,Ltd |
| 品牌 | YING MOTORS |
| 地址 | Liangshan County, Jining City, Shandong Province |
| 联系人 | Kate |
| 电话 / WhatsApp | +86 180 5372 9906 |
| 邮箱 | yingmotorsinfo@gmail.com |

品牌视觉以现有 Logo 为准：金色 `#E49402`、深棕 `#210E06`、深色顶栏、金色按钮。

### 1.4 素材来源

| 资料 | 路径 | 用途 |
| --- | --- | --- |
| 产品目录原片 | `images/products/NEW`、`images/products/USED` | 按车型分夹的实拍（含 HEIC / 视频） |
| 网页用图 | `images/stock/{sku}_{id}/` | 按现车编号分夹：JPG、视频、描述 md |
| 品牌 Logo | `bandlogo/`、`assets/` | 顶栏、页脚、Favicon、联系标签 |

约束：

- 产品图只用我司实拍，不使用网图顶替现车。
- `new` 目录原图多为 HEIC，浏览器不能直接显示，必须转成 JPG 后再上线。
- 新车、二手要分开展示。

### 1.5 页面与功能

| 页面 | 要求 |
| --- | --- |
| 首页 | 公司定位、主营分类、现车入口、WhatsApp |
| 现车目录 | 全部现车；可按新车 / 二手 / 车型筛选 |
| 产品详情 | 实拍、要点、参数、询这一台 |
| 关于我们 | 梁山货源、出口说明、对接人 Kate |
| 联系我们 | 完整联系方式 + 询盘表单（Send → Gmail） |

其它要求：

- 手机端可用（菜单、按钮、图片不挤在一起）。
- 价格不公开填死，一律询盘确认（FOB / CIF、小时数、配置以实车为准）。
- 询盘要带上车型，方便 Kate 回复。

### 1.6 现车范围（按 `images/products` 目录）

**新车 `NEW/`**

- `1` 特种通风厢式挂车
- `2` U 型自卸半挂（海沃油缸）
- 根目录散图：豪沃高栏、绿/米白自卸、红厢式、红栏板、蓝平板
- `三轮车/1–7` 载货、自卸、载客三轮
- `四轮车/1–2` 六轮 UTV、王牌小四驱

**二手 `USED/`**

- `Howo/Truck Tractor` 豪沃牵引车（含视频）
- `Howo/Dump Truck` 中国重汽自卸
- `SHACMAN` 陕汽德龙 F3000
- `Komatsu挖掘机` PC200 / PC130 / PC70 / PC56
- `大巴`、`大巴绿` 客车（含宇通）
- `搅拌罐` 中集搅拌车
- `重汽豪沃蓝牌清洗吸污车` 含介绍文档参数

网页不直接引用中文路径和 HEIC，统一转到 `images/stock/{sku}_{id}/`。同一 Stock No. 的图片、视频、产品描述放在同一个文件夹。

---

## 2. 网站开发实现关键点

### 2.1 技术选型

- 纯静态站：HTML + CSS + 原生 JS，无构建工具、无后端。
- 原因：可直接放到任意空间 / 对象存储。联系表单通过 Web3Forms 把询盘发到 Gmail，不需要自建收表服务器。
- 预览用 Python 自带 `http.server` 即可，不要用 `file://` 打开（部分路径和脚本在本地文件协议下不稳定）。

### 2.2 目录约定

```text
E:\codePrj\web\
  index.html              首页
  products.html           现车目录
  product.html            详情（?id=产品ID）
  about.html / contact.html
  css/styles.css          全站样式
  js/i18n.js              中英文文案
  js/products.js          产品数据 + 卡片渲染
  js/app.js               顶栏页脚、语言、筛选、详情、表单
  assets/                 网页用 Logo / Favicon / OG 图
  images/products/        按车型分夹的原始目录（NEW / USED）
  images/stock/           网页用 JPG / 视频，文件夹名为 {sku}_{product_id}
  images/hero.jpg         首页主图
  bandlogo/               品牌 Logo 源文件
```

源图目录保留不动；网站只引用 `images/` 和 `assets/`。

### 2.3 中英文切换（实现要点）

1. 文案集中在 `js/i18n.js` 的 `YM_I18N.en` / `YM_I18N.zh`。
2. HTML 里用 `data-i18n="键名"`，`YM.applyI18n()` 写入文本。
3. 产品名称、简介、参数放在 `js/products.js` 每条产品的 `en` / `zh`，不进 i18n 总表。
4. 当前语言存在 `localStorage` 键 `ym-lang`（`en` 或 `zh`）。
5. 点击顶栏 EN / 中文后 `location.reload()`，保证所有页面和产品卡一起切换。
6. 缺省为英文：`localStorage` 不是 `zh` 时按 `en` 处理。

新增一句文案：先在 `i18n.js` 两边都加键，再在 HTML 写 `data-i18n`。

### 2.4 产品数据（实现要点）

一条产品最少包含：

- `id`：URL 用，如 `product.html?id=komatsu-pc200`
- `category`：`new` 或 `used`（筛选「新车 / 二手」）
- `type`：`truck` / `trailer` / `tricycle` / `fourwheel` / `bus` / `excavator` / `mixer` / `special`
- `brand`、`images[]`、`thumb`，可选 `videos[]`

筛选逻辑在 `js/app.js` 的 `YM.mountProductList()`：`?cat=used`、`?cat=truck`、`?cat=light`（三轮+四轮）、`?cat=machinery`（挖机+搅拌+环卫）。

WhatsApp 预填文案由 `YM.whatsappLink(product)` 生成，会带上当前语言和车型名。

**加一台车：** 原片放进 `images/products/NEW` 或 `USED` 对应文件夹 → 转成 `images/stock/{sku}_{id}/` → 在 `js/products.js` 追加一条。

详情页文案（名称、简介、要点、参数）**不是**从图片自动生成的，也没有 OCR 或后台。全部是看实拍后写进 `products.js` 的 `en` / `zh`。写法与字段对照见 **4.5**。

### 2.5 图片处理（实现要点）

- HEIC 用 Python（Pillow + pillow-heif）转 JPG，再压到长边约 1600px，输出到 `images/stock/{sku}_{id}/`（避免中文路径和 HEIC）。
- 列表用 `thumbs/`（约 16:10 裁切），详情用全图。
- 视频复制为 `{sku}_v01.mp4` 等，详情页 `<video>` 播放。
- 首页 `images/hero.jpg` 从车队实拍裁成 16:9。
- 竖图按车身位置做 `focus_y` 裁切，避免卡片只看到天空或地面。

以后换图：先转格式、出 thumb，再改 `products.js` 路径。不要把 `.heic` 写进 HTML。

### 2.6 公共头尾与询盘

- 顶栏、页脚、悬浮 WhatsApp 由 `YM.mountChrome()` 注入，避免五个 HTML 各写一份。
- 页面用 `data-page` 高亮当前导航；`data-title` 用于双语 `<title>`。
- 联系页左侧仍展示 WhatsApp / 微信 / 邮箱；表单上只保留 **Send**，不再用 WhatsApp 提交。
- 号码写成 `8618053729906`（国家码、无 `+`、无空格），否则 WhatsApp 链接会失效。
- 产品卡片、详情页上的 Email 链接仍是 `mailto:yingmotorsinfo@gmail.com`（打开访客自己的邮箱软件），与联系表单的 Web3Forms 发送不是同一条路径。

联系表单发信流程：

1. 访客在 `contact.html` 填表，点 **Send**。发送成功后按钮变为 **Finished**。
2. `js/app.js` 的 `YM.sendInquiryByEmail()` 在浏览器里 `POST` 到 `https://api.web3forms.com/submit`（免费版要求走前端，不能从服务器代发）。
3. Web3Forms 把询盘转发到申请 Access Key 时绑定的邮箱：**`yingmotorsinfo@gmail.com`**。
4. 邮件主题为 `Inquiry - {车型}`；正文为表单字段（姓名、公司、国家、联系方式、目的港、留言）。访客填了邮箱时，`Reply-To` 是对方邮箱，Kate 在 Gmail 里直接回复即可。
5. 发件人是 Web3Forms 的通知地址（不是 `yingmotors@outlook.com`，也不是访客自己的邮箱）。

配置 Access Key：

1. 打开 [https://web3forms.com](https://web3forms.com)，用 **`yingmotorsinfo@gmail.com`** 申请 key（key 会发到该 Gmail）。
2. 把 key 填进 `js/app.js` 顶部的 `YM.WEB3FORMS_ACCESS_KEY`。key 本来就要写在前端，可公开；换 key 或泄漏后到 Web3Forms 后台作废再申请即可。
3. 未填写 key 时，点发送会提示「邮箱发送尚未配置」，不会发出去。
4. 站点上线后，建议在 Web3Forms 后台把允许域名限制成正式域名，减少被盗用刷信。

换收件邮箱：必须用新邮箱重新申请 key，再改 `YM.WEB3FORMS_ACCESS_KEY`；只改网页上展示的 Gmail 地址不会改变 Web3Forms 的投递目标。

### 2.7 视觉实现

- 字体：Oswald（标题）+ Source Sans 3 / Noto Sans SC（正文），Google Fonts 外链。
- 主色跟 Logo：`--gold: #e49402`，`--ink: #210e06`，纸色背景 `--paper: #f6f1ea`。
- 深色顶栏用 `assets/logo-mark-dark.svg`（MOTORS 为浅色）。
- 断点：约 980px 收成手机菜单；640px 单列卡片。

### 2.8 页面与脚本加载顺序

每个 HTML 底部固定：

```html
<script src="js/i18n.js"></script>
<script src="js/products.js"></script>
<script src="js/app.js"></script>
```

`app.js` 在 `DOMContentLoaded` 里按顺序：挂头尾 → 应用 i18n → 首页卡片 / 目录筛选 / 详情 / 表单。详情页是 JS 生成 DOM，生成后再跑一次 `applyI18n()`。

### 2.9 上线注意

- 上传整个站点目录，保证 `css/`、`js/`、`assets/`、`images/` 相对路径不变。
- `motorspicture/` 原图体积大且含 HEIC，生产环境可不传，只保留 `images/`。
- 若以后有独立域名，把 `index.html` 里的 `og:image` 改成绝对 URL。
- 参数表是实拍上看清的信息或该型号常规数据（见 **4.5**）。详情页另有全站免责声明：典型参考值，最终以合同 / 技术协议为准。

---

## 3. 常用修改入口

| 要改什么 | 改哪里 |
| --- | --- |
| 导航 / 首页句子 | `js/i18n.js` |
| 增减现车 | `js/i18n.js` 不用动；改 `js/products.js` |
| 产品名称 / 简介 / 参数 | `js/products.js` 的 `en` / `zh`（写法见 **4.5**） |
| 电话、邮箱、WhatsApp | `js/app.js`、`js/products.js` 的链接函数，以及 `contact.html` 展示文本 |
| 询盘表发到哪个邮箱 | `js/app.js` 顶部 `YM.WEB3FORMS_ACCESS_KEY`（见 **2.6**）；收件箱由申请 key 的邮箱决定 |
| 颜色、间距、手机菜单 | `css/styles.css` |
| Logo / 浏览器图标 | `assets/` |

---

## 4. 日常维护（改图 / 加车 / 删车）

网站没有后台。现车全部写在 `js/products.js`，网页只引用 `images/stock/{sku}_{id}/` 下的 **英文路径 JPG / MP4**。原片放在 `images/products/`，不要把中文文件夹或 `.heic` 写进网页。同一 Stock No. 的图、视频、描述（`{sku}_description.md`）必须在同一文件夹。

改完后用 `python -m http.server 8080` 打开对应页面核对；再运行：

```powershell
python E:\codePrj\web\docs\build_product_datasheet.py
```

刷新 `docs/Yingmotors-产品媒体资料.xlsx`，作为库存台账。

先在 Excel 里查 `product_id`（即详情地址 `product.html?id=...`）。

### 4.1 有产品图片（或视频）要修改

1. 在资料表 **01_产品主表** 找到该车的 `product_id`、封面路径、图片/视频路径。
2. **换同一张图：** 用新 JPG 覆盖 `images/stock/{sku}_{id}/{sku}_01.jpg`（或对应编号）。文件名保持 `{sku}_01.jpg`、`{sku}_02.jpg`… 不要改名，就不用改 JS。
3. **同时更新缩略图：** 覆盖 `images/stock/{sku}_{id}/thumbs/{sku}_01.jpg`（列表和首页卡片用这张）。建议约 960×600、16:10。
4. **多拍了几张：** 按顺序加 `{sku}_03.jpg`、`{sku}_04.jpg`…，并各做一张 `thumbs/{sku}_0x.jpg`。然后改 `products.js` 顶部对应的 `ymStock("sku", "id", 张数)`，把张数改成新数量。
5. **换视频：** 覆盖 `{sku}_v01.mp4` 等；新增则加 `{sku}_v03.mp4`，并在该产品的 `videos: ymVid("sku", "id", ["v01.mp4", ...])` 里补文件名。建议无声、H.264。
6. 浏览器强制刷新（Ctrl+F5）看 `product.html?id=该id` 和 `products.html`。

原片可另存一份到 `images/products/NEW` 或 `USED` 对应夹，便于存档。网页仍只读 `images/stock/`。

HEIC 需先转 JPG 再覆盖 stock，例如：

```powershell
python -c "from PIL import Image; from pillow_heif import register_heif_opener; register_heif_opener(); im=Image.open(r'原图.heic').convert('RGB'); im.save(r'E:\codePrj\web\images\stock\YM-NTK-002_new-howo-cargo\YM-NTK-002_01.jpg','JPEG',quality=88)"
```

### 4.2 有产品车型要增加

1. 定一个 **英文 id / 文件夹名**，只含小写字母、数字、连字符，例如 `new-howo-cargo`。这就是 `product_id`。
2. 原片放入 `images/products/NEW/...` 或 `USED/...`。
3. 建立网页目录（文件夹名 = Stock No. + `_` + product_id）：
   - `images/stock/YM-NTK-002_new-howo-cargo/YM-NTK-002_01.jpg`、`YM-NTK-002_02.jpg`…
   - `images/stock/YM-NTK-002_new-howo-cargo/thumbs/YM-NTK-002_01.jpg`…
   - 有视频则 `YM-NTK-002_v01.mp4`…
   - 产品描述 `YM-NTK-002_description.md`（与图、视频同夹）
4. 打开 `js/products.js`：
   - 顶部增加：`var _xx = ymStock("YM-NTK-002", "new-howo-cargo", 4);`（张数与文件一致）
   - 在 `YM_PRODUCTS` 数组里 **复制一条相近车型**，改这些字段：

| 字段 | 填什么 |
| --- | --- |
| `id` | 与文件夹名一致，如 `new-howo-cargo` |
| `category` | `new` 或 `used` |
| `type` | `truck` 重卡 / `trailer` 挂车 / `tricycle` 三轮 / `fourwheel` 四轮 / `bus` 客车 / `excavator` 挖机 / `mixer` 搅拌 / `special` 环卫 |
| `brand` | 品牌英文，如 HOWO |
| `images` / `thumb` | `_xx.images`、`_xx.thumb` |
| `videos` | 可选，`ymVid("YM-NTK-002", "new-howo-cargo", ["v01.mp4"])` |
| `en` / `zh` | `name`、`subtitle`、`summary`、`highlights`、`specs` 中英都写（**怎么从图片写，见 4.5**） |

5. 若要出现在首页「现车实拍」，把 id 加进文件末尾的 `YM_FEATURED_IDS`（建议不超过 6 条）。
6. 打开 `products.html` 用对应筛选确认能出来；再打开 `product.html?id=新id`。
7. 重新生成 Excel 资料表。

`type` 决定筛选：三轮+四轮走「三轮/四轮」；挖机+搅拌+环卫走「工程机械」。

### 4.3 有产品车型要删除

1. 在 `js/products.js` 的 `YM_PRODUCTS` 里删掉整条对象（从 `{` 到 `},`）。
2. 若该 id 在 `YM_FEATURED_IDS` 里，一并删掉，否则首页会少一张卡或空白。
3. 顶部若有仅这一台使用的 `var _xx = ymStock(...)`，可以删掉，避免遗留。
4. `images/stock/{sku}_{id}/` 文件夹可删除（网页不再引用）。`images/products/` 原片是否保留自己决定，建议先移到备份夹而不是直接扔掉。
5. 重新生成 Excel。资料表 **10_未引用** 里会列出磁盘上还有、网站已不挂的文件，便于清理。

不要只删图片不删 JS：详情链接还会在，会变成裂图。不要只删 JS 不删首页推荐 id。

### 4.4 改完必查

- [ ] `products.html` 列表图正常
- [ ] `product.html?id=...` 大图、缩略图、视频
- [ ] 中英文切换后名称和参数都对
- [ ] 首页推荐位（若动过 `YM_FEATURED_IDS`）
- [ ] 已刷新 `docs/Yingmotors-产品媒体资料.xlsx`

### 4.5 产品描述怎么从图片写进 `products.js`

网站**不会**根据新图片自动写出描述。没有识别脚本、没有接口。流程是：打开实拍 → 把图上能看清的信息填进 `js/products.js` → 详情页只负责读出来展示。换一张图如果不改 JS，页面文案不会变。

#### 写的时候看什么

打开 `images/stock/{sku}_{id}/` 里的 JPG（必要时对照原片），从图上读：

- 前脸 / 中网字母：品牌（HOWO、SITRAK、SHACMAN、Komatsu…）
- 前脸型号标、车门侧标、罐体 / 货箱上的字：型号、马力、排放、搅拌容量等
- 油漆颜色、车身形式（牵引 / 自卸 / 搅拌罐 / 挖机履带）
- 轴数（数轮子）、驾驶室高低顶、是否贴「出口」
- 拍摄环境（出口车场、成排现车）只写进简介，不当成品参数

图上看不清的数字**不要编**。罐体写了「搅拌容量」但立方米看不清，就不要填容量。只看到「350 马力」门标、没有发动机型号时，写成「350 马力**级**」。有厂家介绍文档时（例如豪沃清洗吸污车），参数可以按文档抄，并注明以合同为准。

#### 字段从哪来（结构 vs 看图）

| 字段 | 详情页位置 | 从哪来 |
| --- | --- | --- |
| `id` | 网址 `product.html?id=...` | 自己定的英文文件夹名，图上没有 |
| `sku` | 现车编号，如 `YM-UMX-002` | 按规则编：`YM-` + N/U + 类型缩写 + 序号。图上没有 |
| `category` | 徽章「新车 / 二手」 | 原图在 `NEW/` 还是 `USED/`（或 `used/`） |
| `type` | 筛选分类 | 车型（罐=mixer，牵引/自卸=truck…） |
| `brand` | 品牌一行 | **图上读**：中网或车身品牌字 |
| `images` / `thumb` | 大图、缩略图 | `ymStock("YM-NTK-002", "new-howo-cargo", 张数)`，不是文案 |
| `en.name` / `zh.name` | `<h1>` 标题 | 拼：新旧 + 品牌 + 车型 + 图上型号 |
| `subtitle` | 标题下导语 | 门标 / 颜色等最醒目的几项，用 `·` 隔开 |
| `summary` | 简介段落 | 把图上能确认的事写成 1～2 句 |
| `highlights` | 要点列表 | 从 name / summary 抽 3～4 条短句 |
| `specs` | 参数表 | 同样信息改成「项目 / 值」行；中英各写一遍 |

`sku` 规则见 `js/products.js` 顶部注释：`YM-{N|U}{TYPE}-{NNN}`。N=新车 U=二手；TK 重卡 / TL 挂车 / TC 三轮 / FW 四轮 / BS 客车 / EX 挖机 / LD 装载机 / MX 搅拌 / SP 环卫。同类序号不复用。

详情页底部那句「参数为典型参考值，最终以合同 / 技术协议为准」来自 `js/i18n.js` 的 `detail_note`，全站共用，不要写进某一台车的 `summary`。

`product.html` 是空壳。`js/app.js` 的 `YM.mountProductDetail()` 用 `?id=` 找到产品，按当前语言取 `en` 或 `zh`，再填进标题、导语、简介、要点和参数表。

#### 实例：陕汽搅拌车 `used-shacman-mixer`

原片：`images/product pictures20260830/used/Mixing tank/` 一辆白色搅拌车。转入 `images/stock/YM-UMX-002_used-shacman-mixer/YM-UMX-002_01.jpg` 后看图填写（详情 `product.html?id=used-shacman-mixer`）：

| 图上看到的 | 写成的文案 |
| --- | --- |
| 中网镀铬 `SHACMAN` | `brand: "SHACMAN"`；名称里的陕汽 / SHACMAN |
| 前脸型号标 `M3000S` | 名称括号、参数「型号」 |
| 车门标「350 马力 / 国六」 | 导语 `350 hp · China VI`；参数发动机 / 排放 |
| 白驾驶室 + 白搅拌罐 | 名称里的搅拌车；要点「白色驾驶室与罐体」 |
| 两前桥 + 两后桥 | 简介「四轴」 |
| 背景国旗、成排货车 | 简介「出口车场实拍」（不是铭牌） |
| 罐体「搅拌容量」字看不清 | **不写**立方米 |
| 文件夹在 `used/` | `category: "used"`，徽章「二手」 |

对应 `products.js` 片段：

```javascript
id: "used-shacman-mixer",
sku: "YM-UMX-002",
category: "used",
type: "mixer",
brand: "SHACMAN",
en: {
  name: "Used SHACMAN Mixer (M3000S)",
  subtitle: "350 hp · China VI · white",
  summary: "White SHACMAN M3000S mixer, door badge 350 hp China VI. Four-axle chassis, white drum. Photographed on the export lot.",
  highlights: ["SHACMAN M3000S mixer", "350 hp China VI", "White cab and drum", "Used export"],
  specs: [["Brand", "SHACMAN"], ["Model", "M3000S"], ["Engine", "350 hp class"], ["Emission", "China VI"], ["Type", "Concrete mixer truck"], ["Color", "White"], ["Condition", "Used"]]
}
```

以后加新图：转 JPG → 看图填上表 → 写入 `en` / `zh`。不要指望上传图片后页面自己长出一段文字。
