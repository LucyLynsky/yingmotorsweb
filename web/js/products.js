var YM_IMAGES_BASE = "https://webimages.yingmotors.com/web/images/";

function ymDir(sku, slug) {
  return sku + "_" + slug;
}

function ymStock(sku, slug, count, thumbNo) {
  var folder = ymDir(sku, slug);
  var images = [];
  var i;
  var thumb = thumbNo || 1;
  function fileName(i) {
    var n = (i < 10 ? "0" : "") + i;
    return sku + "_" + n + ".jpg";
  }
  for (i = 1; i <= count; i++) {
    images.push(YM_IMAGES_BASE + "stock/" + folder + "/" + fileName(i));
  }
  return {
    images: images,
    thumb: YM_IMAGES_BASE + "stock/" + folder + "/thumbs/" + fileName(thumb)
  };
}

function ymVid(sku, slug, names) {
  var folder = ymDir(sku, slug);
  return names.map(function (name) {
    var file = name.indexOf(sku + "_") !== 0 ? sku + "_" + name : name;
    return YM_IMAGES_BASE + "stock/" + folder + "/" + file;
  });
}

var _ut = ymStock("YM-UTK-001", "used-howo-tractor", 5);
var _sc9 = ymStock("YM-UTK-002", "used-sitrak-c9h", 1);
var _sg7 = ymStock("YM-UTK-003", "used-sitrak-g7s", 1);
var _us = ymStock("YM-UTK-004", "used-shacman-f3000", 12);
var _sx3 = ymStock("YM-UTK-005", "used-shacman-x3000", 3);
var _ud = ymStock("YM-UTK-006", "used-howo-dump", 4);
var _hyd = ymStock("YM-UTK-007", "used-howo-dump-yellow", 1);
var _hwg = ymStock("YM-UTK-008", "used-howo-dump-white-grey", 2);
var _hr430 = ymStock("YM-UTK-010", "used-howo-dump-red", 3);
var _h371 = ymStock("YM-UTK-011", "used-howo-371", 1);
var _wt = ymStock("YM-UTK-013", "used-weichai-wt110", 3);
var _uv = ymStock("YM-USP-001", "used-howo-vacuum", 5);
var _nhk = ymStock("YM-NTK-001", "new-howo-stake", 1);
var _n1 = ymStock("YM-NTL-001", "new-special-box", 2);
var _n2 = ymStock("YM-NTL-002", "new-dump-hyva", 2);
var _nsun = ymStock("YM-NTL-003", "new-dump-sunhunk", 4);
var _ngn = ymStock("YM-NTL-004", "new-dump-green", 1);
var _nvr = ymStock("YM-NTL-005", "new-van-red", 1);
var _nds = ymStock("YM-NTL-006", "new-dropside-red", 2);
var _nwr = ymStock("YM-NTL-007", "new-dump-white-red", 1);
var _nfb = ymStock("YM-NTL-008", "new-flatbed-blue", 1);
var _t1 = ymStock("YM-NTC-001", "new-tricycle-1", 6);
var _t2 = ymStock("YM-NTC-002", "new-tricycle-2", 5);
var _t3 = ymStock("YM-NTC-003", "new-tricycle-3", 1);
var _t4 = ymStock("YM-NTC-004", "new-tricycle-4", 1);
var _t5 = ymStock("YM-NTC-005", "new-tricycle-5", 1);
var _t6 = ymStock("YM-NTC-006", "new-tricycle-6", 3);
var _t7 = ymStock("YM-NTC-007", "new-tricycle-7", 3);
var _f1 = ymStock("YM-NFW-001", "new-utv-6wheel", 1);
var _f2 = ymStock("YM-NFW-002", "new-4wd-dumper", 3);
var _uk1 = ymStock("YM-UEX-001", "used-komatsu-pc200", 6);
var _uk2 = ymStock("YM-UEX-002", "used-komatsu-pc200-b", 1);
var _uk3 = ymStock("YM-UEX-003", "used-komatsu-pc130", 1);
var _uk4 = ymStock("YM-UEX-004", "used-komatsu-pc70", 1);
var _uk5 = ymStock("YM-UEX-005", "used-komatsu-pc56", 1);
var _sdl = ymStock("YM-ULD-001", "used-sdlg-loader", 4);
var _um = ymStock("YM-UMX-001", "used-mixer-cimc", 1);
var _smx = ymStock("YM-UMX-002", "used-shacman-mixer", 1);
var _ub = ymStock("YM-UBS-001", "used-bus", 7, 5);
var _ug = ymStock("YM-UBS-002", "used-bus-yutong", 8);

/* Stock number: YM-{N|U}{TYPE}-{NNN}
   Folder: {YM_IMAGES_BASE}stock/{sku}_{id}/   e.g. YM-UTK-001_used-howo-tractor/
   Files: {sku}_01.jpg, {sku}_v01.mp4, thumbs/{sku}_01.jpg, {sku}_description.md
   N=new U=used
   TK=truck TL=trailer TC=tricycle FW=fourwheel
   BS=bus EX=excavator LD=loader MX=mixer SP=special
   Sequence is unique within that group and is never reused.
   Retired (do not reuse): YM-UTK-009 merged into YM-UTK-010 (not searchable);
   YM-UTK-012 chassis photos belong to YM-UTK-001 (not sold separately, not searchable);
   YM-UEX-006 and YM-UEX-007 are extra angles of YM-UEX-001 (not separate units). */
window.YM_PRODUCTS = [
  {
    id: "used-howo-tractor",
    sku: "YM-UTK-001",
    category: "used",
    type: "truck",
    brand: "HOWO",
    images: _ut.images,
    thumb: _ut.thumb,
    videos: ymVid("YM-UTK-001", "used-howo-tractor", ["v01.mp4", "v02.mp4", "v04.mp4", "v05.mp4"]),
    en: {
      name: "Used HOWO / SINOTRUK Tractor",
      subtitle: "CNHTC tractor unit · in stock",
      summary: "White HOWO tractor with CNHTC grille. Photos and yard videos available. Extra photos are chassis / rear-frame detail shots of this unit — not a separate chassis for sale. Typical choice for Africa and Middle East haulage.",
      highlights: ["HOWO / SINOTRUK tractor", "White cab, CNHTC badge", "Chassis / frame detail photos", "Yard videos on this page", "FOB / CIF quotation"],
      specs: [["Brand", "HOWO / SINOTRUK"], ["Type", "Tractor / prime mover"], ["Color", "White"], ["Condition", "Used"], ["Documents", "Export documents on request"]]
    },
    zh: {
      name: "二手豪沃 / 中国重汽牵引车",
      subtitle: "中国重汽牵引车头 · 现车",
      summary: "白色豪沃牵引车，前脸 CNHTC 标识。本页含场地视频。另含本车底盘 / 后车架特写，仅作说明图，不单独出售底盘。适合非洲、中东货运。",
      highlights: ["豪沃 / 中国重汽牵引车", "白色驾驶室", "含底盘说明图", "本页含视频", "支持 FOB / CIF"],
      specs: [["品牌", "豪沃 / 中国重汽"], ["类型", "牵引车"], ["颜色", "白色"], ["状态", "二手"], ["单证", "询盘提供"]]
    }
  },
  {
    id: "used-sitrak-c9h",
    sku: "YM-UTK-002",
    category: "used",
    type: "truck",
    brand: "SITRAK",
    images: _sc9.images,
    thumb: _sc9.thumb,
    en: {
      name: "Used SITRAK Tractor (Orange)",
      subtitle: "SINOTRUK SITRAK · export unit",
      summary: "Orange SITRAK tractor with chrome grille badge and 出口 windshield mark. Photographed in a SINOTRUK yard lineup.",
      highlights: ["SITRAK / SINOTRUK tractor", "Orange cab", "Export-marked unit", "FOB / CIF quotation"],
      specs: [["Brand", "SITRAK / SINOTRUK"], ["Type", "Tractor / prime mover"], ["Color", "Orange"], ["Condition", "Used"], ["Documents", "Export documents on request"]]
    },
    zh: {
      name: "二手汕德卡牵引车（橙色）",
      subtitle: "中国重汽汕德卡 · 出口现车",
      summary: "橙色汕德卡牵引车，前脸 SITRAK 标识，风挡贴有「出口」。场地实拍。",
      highlights: ["汕德卡 / 中国重汽牵引车", "橙色驾驶室", "出口标识", "支持 FOB / CIF"],
      specs: [["品牌", "汕德卡 / 中国重汽"], ["类型", "牵引车"], ["颜色", "橙色"], ["状态", "二手"], ["单证", "询盘提供"]]
    }
  },
  {
    id: "used-sitrak-g7s",
    sku: "YM-UTK-003",
    category: "used",
    type: "truck",
    brand: "SITRAK",
    images: _sg7.images,
    thumb: _sg7.thumb,
    en: {
      name: "Used SITRAK G7S Tractor",
      subtitle: "G7S · orange cab · China VI",
      summary: "Orange SITRAK G7S tractor, high-roof cab, chrome grille. Several identical units in the same yard row.",
      highlights: ["SITRAK G7S", "Orange high-roof cab", "Yard lineup", "FOB / CIF quotation"],
      specs: [["Brand", "SITRAK / SINOTRUK"], ["Model", "G7S"], ["Type", "Tractor / prime mover"], ["Color", "Orange"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手汕德卡 G7S 牵引车",
      subtitle: "G7S · 橙色 · 国六",
      summary: "橙色汕德卡 G7S 牵引车，高顶驾驶室。同排多台现车。",
      highlights: ["汕德卡 G7S", "橙色高顶", "场地成排现车", "支持 FOB / CIF"],
      specs: [["品牌", "汕德卡 / 中国重汽"], ["型号", "G7S"], ["类型", "牵引车"], ["颜色", "橙色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-shacman-f3000",
    sku: "YM-UTK-004",
    category: "used",
    type: "truck",
    brand: "SHACMAN",
    images: _us.images,
    thumb: _us.thumb,
    videos: ymVid("YM-UTK-004", "used-shacman-f3000", ["v01.mp4", "v02.mp4"]),
    en: {
      name: "Used SHACMAN Delong F3000",
      subtitle: "德龙 F3000 tractor · white",
      summary: "SHACMAN Delong F3000 with chrome grille badge. Multiple exterior photos and videos from the yard.",
      highlights: ["SHACMAN Delong F3000", "White cab", "Photo set + videos", "Inspect before loading"],
      specs: [["Brand", "SHACMAN"], ["Model", "Delong F3000"], ["Type", "Tractor / heavy truck"], ["Color", "White"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手陕汽德龙 F3000",
      subtitle: "德龙 F3000 · 白色",
      summary: "陕汽德龙 F3000，前脸 SHACMAN 标识。场地多角度照片与视频。",
      highlights: ["陕汽德龙 F3000", "白色驾驶室", "多图 + 视频", "装柜前可验"],
      specs: [["品牌", "陕汽 SHACMAN"], ["型号", "德龙 F3000"], ["类型", "牵引 / 重卡"], ["颜色", "白色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-shacman-x3000",
    sku: "YM-UTK-005",
    category: "used",
    type: "truck",
    brand: "SHACMAN",
    images: _sx3.images,
    thumb: _sx3.thumb,
    en: {
      name: "Used SHACMAN X3000 Tractor",
      subtitle: "X3000 · 430 hp class · white",
      summary: "White SHACMAN X3000 6×4 tractor. Front, three-quarter and fifth-wheel photos from the yard. Door marked 430.",
      highlights: ["SHACMAN X3000", "6×4 tractor, 430 class", "White cab, black grille", "Inspect before loading"],
      specs: [["Brand", "SHACMAN"], ["Model", "X3000"], ["Type", "Tractor / prime mover"], ["Drive", "6×4"], ["Color", "White"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手陕汽德龙 X3000 牵引车",
      subtitle: "X3000 · 430 马力级 · 白色",
      summary: "白色陕汽 X3000 牵引车，6×4，车门 430 标识。含正面、侧面和鞍座实拍。",
      highlights: ["陕汽德龙 X3000", "6×4 牵引，430 级", "白色驾驶室", "装柜前可验"],
      specs: [["品牌", "陕汽 SHACMAN"], ["型号", "X3000"], ["类型", "牵引车"], ["驱动", "6×4"], ["颜色", "白色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-howo-dump",
    sku: "YM-UTK-006",
    category: "used",
    type: "truck",
    brand: "SINOTRUK",
    images: _ud.images,
    thumb: _ud.thumb,
    en: {
      name: "Used SINOTRUK Dump Truck",
      subtitle: "CNHTC tipper · white",
      summary: "White SINOTRUK dump truck with CNHTC front badge. Suitable for construction and quarry haulage.",
      highlights: ["SINOTRUK dump / tipper", "White cab and body", "Multi-axle heavy duty", "Used export unit"],
      specs: [["Brand", "SINOTRUK / CNHTC"], ["Type", "Dump truck"], ["Color", "White"], ["Condition", "Used"], ["Use", "Construction / quarry"]]
    },
    zh: {
      name: "二手中国重汽自卸车",
      subtitle: "中国重汽自卸 · 白色",
      summary: "白色中国重汽自卸车，前脸 CNHTC。适合工地和料场运输。",
      highlights: ["中国重汽自卸", "白色驾驶室与货箱", "多轴重载", "二手出口现车"],
      specs: [["品牌", "中国重汽"], ["类型", "自卸车"], ["颜色", "白色"], ["状态", "二手"], ["用途", "工地 / 料场"]]
    }
  },
  {
    id: "used-howo-dump-yellow",
    sku: "YM-UTK-007",
    category: "used",
    type: "truck",
    brand: "HOWO",
    images: _hyd.images,
    thumb: _hyd.thumb,
    en: {
      name: "Used HOWO Dump Truck (Yellow)",
      subtitle: "CNHTC tipper · yellow",
      summary: "Yellow HOWO dump trucks with CNHTC grille, headlight guards and visor still in film. Yard pair photographed together.",
      highlights: ["HOWO / SINOTRUK dump", "Yellow cab", "Headlight mesh guards", "Used export unit"],
      specs: [["Brand", "HOWO / SINOTRUK"], ["Type", "Dump truck"], ["Color", "Yellow"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手豪沃自卸车（黄色）",
      subtitle: "中国重汽自卸 · 黄色",
      summary: "黄色豪沃自卸，前脸 CNHTC，大灯铁网护罩，遮阳罩带保护膜。场地成对实拍。",
      highlights: ["豪沃自卸", "黄色驾驶室", "大灯护网", "二手出口现车"],
      specs: [["品牌", "豪沃 / 中国重汽"], ["类型", "自卸车"], ["颜色", "黄色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-howo-dump-white-grey",
    sku: "YM-UTK-008",
    category: "used",
    type: "truck",
    brand: "HOWO",
    images: _hwg.images,
    thumb: _hwg.thumb,
    en: {
      name: "Used HOWO Dump Truck (White / Grey)",
      subtitle: "8×4 tipper · grey body",
      summary: "White HOWO cab with dark-grey dump body. Four-axle layout, side underrun guard and roof beacon. Hood-open service photo included.",
      highlights: ["HOWO dump / tipper", "White cab, grey body", "8×4 style chassis", "Service-bay photo"],
      specs: [["Brand", "HOWO / SINOTRUK"], ["Type", "Dump truck"], ["Drive", "8×4 class"], ["Color", "White cab / grey body"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手豪沃自卸车（白驾灰箱）",
      subtitle: "8×4 自卸 · 灰货箱",
      summary: "白色豪沃驾驶室、深灰货箱。四轴，侧护栏和顶警示灯。含翻盖检修实拍。",
      highlights: ["豪沃自卸", "白驾灰箱", "四轴", "含检修仓照片"],
      specs: [["品牌", "豪沃 / 中国重汽"], ["类型", "自卸车"], ["驱动", "8×4 级"], ["颜色", "白驾 / 灰箱"], ["状态", "二手"]]
    }
  },
  {
    id: "used-howo-dump-red",
    sku: "YM-UTK-010",
    aliases: ["used-howo-dump-orange"],
    category: "used",
    type: "truck",
    brand: "HOWO",
    images: _hr430.images,
    thumb: _hr430.thumb,
    en: {
      name: "Used HOWO 430 Dump Truck (Red)",
      subtitle: "SINOTRUK 430 · red tipper",
      summary: "Red HOWO 430 dump, cab and body matched. Yard photos from several angles: SINOTRUK 430 badge, CNHTC grille, headlight guards; mirror arm still in film on one shot.",
      highlights: ["HOWO 430 dump", "Red cab and body", "Several yard angles", "Used export"],
      specs: [["Brand", "HOWO / SINOTRUK"], ["Model", "430 class"], ["Type", "Dump truck"], ["Color", "Red"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手豪沃 430 自卸（红色）",
      subtitle: "中国重汽 430 · 红色自卸",
      summary: "红色豪沃 430 自卸，驾驶室与货箱同色。多角度场地实拍：前脸 SINOTRUK 430 与 CNHTC，大灯护网，后视镜有保护膜。",
      highlights: ["豪沃 430 自卸", "红色驾驶室与货箱", "多角度实拍", "二手出口"],
      specs: [["品牌", "豪沃 / 中国重汽"], ["型号", "430 级"], ["类型", "自卸车"], ["颜色", "红色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-howo-371",
    sku: "YM-UTK-011",
    category: "used",
    type: "truck",
    brand: "HOWO",
    images: _h371.images,
    thumb: _h371.thumb,
    en: {
      name: "Used HOWO 371 (Red)",
      subtitle: "SINOTRUK 371 · red cab",
      summary: "Red HOWO cab with 371 front badge, CNHTC grille and headlight mesh guards. Photographed in the yard lineup.",
      highlights: ["HOWO 371", "Red cab", "CNHTC grille", "Used"],
      specs: [["Brand", "HOWO / SINOTRUK"], ["Model", "371 class"], ["Type", "Heavy truck cab"], ["Color", "Red"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手豪沃 371（红色）",
      subtitle: "中国重汽 371 · 红色驾驶室",
      summary: "红色豪沃驾驶室，前脸 371 与 CNHTC，大灯铁网护罩。场地实拍。",
      highlights: ["豪沃 371", "红色驾驶室", "CNHTC 前脸", "二手"],
      specs: [["品牌", "豪沃 / 中国重汽"], ["型号", "371 级"], ["类型", "重卡驾驶室"], ["颜色", "红色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-weichai-wt110",
    sku: "YM-UTK-013",
    category: "used",
    type: "truck",
    brand: "Weichai",
    images: _wt.images,
    thumb: _wt.thumb,
    videos: ymVid("YM-UTK-013", "used-weichai-wt110", ["v01.mp4"]),
    en: {
      name: "Used Weichai WT110 Mining Dump",
      subtitle: "Off-highway mining truck · yellow",
      summary: "Yellow Weichai WT110 wide-body mining dump. Yard video plus stills. Heavy-duty off-road tyres, black grille.",
      highlights: ["Weichai WT110", "Mining / off-highway dump", "Yellow body", "Yard video on this page"],
      specs: [["Brand", "Weichai"], ["Model", "WT110"], ["Type", "Mining dump truck"], ["Color", "Yellow"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手潍柴 WT110 矿用自卸",
      subtitle: "宽体矿卡 · 黄色",
      summary: "黄色潍柴 WT110 宽体矿用自卸。含场地视频和截帧。越野胎、黑色前脸。",
      highlights: ["潍柴 WT110", "矿用宽体自卸", "黄色", "本页含视频"],
      specs: [["品牌", "潍柴 Weichai"], ["型号", "WT110"], ["类型", "矿用自卸"], ["颜色", "黄色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-howo-vacuum",
    sku: "YM-USP-001",
    category: "used",
    type: "special",
    brand: "HOWO",
    images: [_uv.images[0], _uv.images[2], _uv.images[3], _uv.images[4]],
    thumb: _uv.thumb,
    en: {
      name: "HOWO Jetting & Vacuum Truck",
      subtitle: "Blue-plate sanitation · sludge 4.1 m³ / water 2 m³",
      summary: "HOWO chassis combination sewer cleaner. High-pressure washing plus vacuum suction. China VI, 150 hp, GVW 4,495 kg — blue-plate class in China.",
      highlights: ["HOWO chassis, 150 hp China VI", "Sludge 4.1 m³, fresh water 2 m³", "24 MPa jetting, 170 L/min", "8 m suction, Φ100 mm particle"],
      specs: [
        ["Product name", "Jetting & vacuum truck"],
        ["Effective volume", "Sludge 4.1 m³ / fresh water 2 m³"],
        ["Dimensions", "5995 × 2350 × 2650 mm"],
        ["Cab seats", "2"],
        ["Engine maker", "Weichai Power / Kunming Yunnei"],
        ["Engine model", "WP2.5NQ150E61 / D25TCIF1"],
        ["Engine power", "110 kW / 150 hp"],
        ["Emission", "China VI"],
        ["GVW / curb / payload", "4,495 / 2,870 / 1,495 kg"],
        ["Wheelbase", "3280 mm"],
        ["Max speed", "95 km/h"],
        ["Tyres", "7.00R16 × 6"],
        ["Water / sludge tank", "2 m³ / 4.1 m³"],
        ["Jetting pressure", "24 MPa"],
        ["Pump flow", "170 L/min"],
        ["Vertical suction", "8 m"],
        ["Max particle", "Φ100 mm"]
      ]
    },
    zh: {
      name: "重汽豪沃蓝牌清洗吸污车",
      subtitle: "清洗 + 吸污 · 污罐 4.1 立方 / 清水 2 立方",
      summary: "豪沃底盘清洗吸污两用车。国六 150 马力，总质量 4495kg 蓝牌。高压清洗 + 真空吸污。",
      highlights: ["豪沃底盘，150 马力国 VI", "污罐 4.1 立方，清水 2 立方", "清洗压力 24 MPa，流量 170 L/min", "垂直吸程 8 m，最大颗粒 Φ100 mm"],
      specs: [
        ["产品名称", "清洗吸污车"],
        ["有效容积", "污罐 4.1 m³ / 清水 2 m³"],
        ["外形尺寸", "5995 × 2350 × 2650 mm"],
        ["驾驶室准乘", "2 人"],
        ["发动机厂家", "潍柴动力 / 昆明云内动力"],
        ["发动机型号", "WP2.5NQ150E61 / D25TCIF1"],
        ["发动机功率", "110 kW / 150 马力"],
        ["排放标准", "国 VI"],
        ["总质量 / 整备 / 额定载质量", "4495 / 2870 / 1495 kg"],
        ["轴距", "3280 mm"],
        ["最高车速", "95 km/h"],
        ["轮胎", "7.00R16 × 6"],
        ["清水箱 / 污水箱", "2 m³ / 4.1 m³"],
        ["清洗压力", "24 MPa"],
        ["水泵流量", "170 L/min"],
        ["垂直吸程", "8 m"],
        ["最大吸入颗粒", "Φ100 mm"]
      ]
    }
  },
  {
    id: "new-howo-stake",
    sku: "YM-NTK-001",
    category: "new",
    type: "truck",
    brand: "HOWO",
    images: _nhk.images,
    thumb: _nhk.thumb,
    en: {
      name: "HOWO High-side Cargo Truck",
      subtitle: "Stake / fence cargo · new",
      summary: "White HOWO cargo truck with matching high-side stake body. 6×4 style chassis for general cargo and livestock-fence haulage.",
      highlights: ["HOWO cargo truck", "High-side stake body", "White cab and body", "New stock"],
      specs: [["Brand", "HOWO"], ["Type", "Cargo / stake truck"], ["Color", "White"], ["Condition", "New"]]
    },
    zh: {
      name: "豪沃高栏载货车",
      subtitle: "高栏货车 · 新车",
      summary: "白色豪沃载货车，配套高栏货箱，适合普货运输。",
      highlights: ["豪沃载货车", "高栏货箱", "白色", "新车现货"],
      specs: [["品牌", "豪沃"], ["类型", "高栏载货车"], ["颜色", "白色"], ["状态", "新车"]]
    }
  },
  {
    id: "new-special-box",
    sku: "YM-NTL-001",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _n1.images,
    thumb: _n1.thumb,
    en: {
      name: "Special Ventilated Box Trailer",
      subtitle: "Custom box · hatch, door, ladder",
      summary: "Dark-grey special box trailer with side ventilation, rear door, roof hatch and access ladder. Suitable for livestock, service or special cargo.",
      highlights: ["Ventilated / special box", "Rear door and hatch", "Side ladder to roof", "Custom graphics"],
      specs: [["Type", "Special box trailer"], ["Access", "Door, hatch, ladder"], ["Color", "Dark grey"], ["Condition", "New"]]
    },
    zh: {
      name: "特种通风厢式挂车",
      subtitle: "定制厢体 · 舱门爬梯",
      summary: "深灰特种厢式挂车，侧通风、后门、顶舱和爬梯，适合活畜、维修或特种货物。",
      highlights: ["特种通风厢", "后门 + 顶舱", "后爬梯", "可喷绘"],
      specs: [["类型", "特种厢式挂车"], ["通道", "门、舱盖、爬梯"], ["颜色", "深灰"], ["状态", "新车"]]
    }
  },
  {
    id: "new-dump-hyva",
    sku: "YM-NTL-002",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _n2.images,
    thumb: _n2.thumb,
    en: {
      name: "U-shape Dump Semi-Trailer (HYVA)",
      subtitle: "Tri-axle tipper · HYVA cylinder",
      summary: "Grey U-shape rear-dump semi-trailer with HYVA (海沃) front lift cylinder. Carry / 冠荣 mechanical body, three axles.",
      highlights: ["U-shape dump body", "HYVA hydraulic cylinder", "Tri-axle chassis", "Bulk materials"],
      specs: [["Type", "Dump semi-trailer"], ["Body", "U-shape"], ["Lift", "HYVA front cylinder"], ["Axles", "3"], ["Condition", "New"]]
    },
    zh: {
      name: "U型自卸半挂（海沃油缸）",
      subtitle: "三轴后翻 · 海沃举升",
      summary: "灰色 U 型后翻自卸半挂，前举升为海沃 HYVA 油缸，冠荣货箱，三轴。",
      highlights: ["U型货箱", "海沃油缸", "三轴", "散货运输"],
      specs: [["类型", "自卸半挂"], ["货箱", "U型"], ["举升", "海沃前顶"], ["轴数", "3"], ["状态", "新车"]]
    }
  },
  {
    id: "new-dump-sunhunk",
    sku: "YM-NTL-003",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _nsun.images,
    thumb: _nsun.thumb,
    en: {
      name: "U-shape Dump Semi-Trailer (SUNHUNK)",
      subtitle: "Front-lift tipper · SUNHUNK cylinder",
      summary: "Grey dump semi-trailer with red SUNHUNK front-lift cylinder, spare tyre on the headboard and landing gear down. Fleet photos from the yard.",
      highlights: ["U-shape / ribbed dump body", "SUNHUNK hydraulic cylinder", "Spare tyre on headboard", "New stock"],
      specs: [["Type", "Dump semi-trailer"], ["Lift", "SUNHUNK front cylinder"], ["Color", "Grey / red cylinder"], ["Condition", "New"]]
    },
    zh: {
      name: "U型自卸半挂（SUNHUNK 油缸）",
      subtitle: "前顶自卸 · 宏大油缸",
      summary: "灰色自卸半挂，前顶红色 SUNHUNK 油缸，前墙备胎，支腿落地。含场地成排实拍。",
      highlights: ["U型 / 加强货箱", "SUNHUNK 举升油缸", "前墙备胎", "新车现货"],
      specs: [["类型", "自卸半挂"], ["举升", "SUNHUNK 前顶"], ["颜色", "灰箱红油缸"], ["状态", "新车"]]
    }
  },
  {
    id: "new-dump-green",
    sku: "YM-NTL-004",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _ngn.images,
    thumb: _ngn.thumb,
    en: {
      name: "Green U-shape Dump Semi-Trailer",
      subtitle: "Front-lift tipper · Changyuan HYVA",
      summary: "Gloss green U-shape dump trailer on red chassis, Changyuan HYVA lift cylinder and front access ladder.",
      highlights: ["Green U-body", "Red chassis", "HYVA-type lift", "New"],
      specs: [["Type", "Dump semi-trailer"], ["Color", "Green / red chassis"], ["Condition", "New"]]
    },
    zh: {
      name: "绿色 U 型自卸半挂",
      subtitle: "前顶自卸 · 长远海沃",
      summary: "绿色 U 型自卸，红色底盘，长远海沃举升油缸，带前爬梯。",
      highlights: ["绿色 U 箱", "红底盘", "海沃举升", "新车"],
      specs: [["类型", "自卸半挂"], ["颜色", "绿箱红架"], ["状态", "新车"]]
    }
  },
  {
    id: "new-van-red",
    sku: "YM-NTL-005",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _nvr.images,
    thumb: _nvr.thumb,
    en: {
      name: "Red Van Semi-Trailer",
      subtitle: "Enclosed dry-cargo box",
      summary: "Corrugated red van semi-trailer with rear doors for weather-protected cargo.",
      highlights: ["Enclosed van body", "Rear cargo doors", "Red finish", "New"],
      specs: [["Type", "Van / box semi-trailer"], ["Color", "Red"], ["Condition", "New"]]
    },
    zh: {
      name: "红色厢式半挂车",
      subtitle: "封闭干货厢",
      summary: "红色瓦楞厢式半挂，后门开启，适合怕雨货物。",
      highlights: ["封闭厢体", "后双开门", "红色", "新车"],
      specs: [["类型", "厢式半挂"], ["颜色", "红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-dropside-red",
    sku: "YM-NTL-006",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _nds.images,
    thumb: _nds.thumb,
    en: {
      name: "Red Dropside / Fence Semi-Trailer",
      subtitle: "Tri-axle side panels",
      summary: "Red dropside semi-trailer with folding side panels, headboard and tri-axle chassis for general cargo.",
      highlights: ["Dropside / fence body", "Tri-axle", "Red paint", "New"],
      specs: [["Type", "Dropside semi-trailer"], ["Axles", "3"], ["Color", "Red"], ["Condition", "New"]]
    },
    zh: {
      name: "红色栏板 / 侧翻半挂",
      subtitle: "三轴侧板",
      summary: "红色栏板半挂，侧板可放，三轴，适合普货。",
      highlights: ["栏板货箱", "三轴", "红色", "新车"],
      specs: [["类型", "栏板半挂"], ["轴数", "3"], ["颜色", "红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-dump-white-red",
    sku: "YM-NTL-007",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _nwr.images,
    thumb: _nwr.thumb,
    en: {
      name: "White / Red U-shape Dump Trailer",
      subtitle: "Front hydraulic lift",
      summary: "Cream U-shape tipper on red chassis with front hydraulic cylinder and inspection platform.",
      highlights: ["U-shape body", "Red chassis", "Front lift", "New"],
      specs: [["Type", "Dump semi-trailer"], ["Body", "U-shape"], ["Color", "White / red"], ["Condition", "New"]]
    },
    zh: {
      name: "米白 / 红 U 型自卸半挂",
      subtitle: "前举升",
      summary: "米色 U 型货箱、红色底盘，前举升油缸和检修平台。",
      highlights: ["U型箱", "红底盘", "前顶", "新车"],
      specs: [["类型", "自卸半挂"], ["货箱", "U型"], ["颜色", "米白 / 红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-flatbed-blue",
    sku: "YM-NTL-008",
    category: "new",
    type: "trailer",
    brand: "Yingmotors",
    images: _nfb.images,
    thumb: _nfb.thumb,
    en: {
      name: "Blue Flatbed Semi-Trailer",
      subtitle: "Open deck · headboard",
      summary: "Blue flatbed trailer with diamond-plate deck, front headboard and side tool box.",
      highlights: ["Flat deck", "Headboard", "Blue chassis", "New"],
      specs: [["Type", "Flatbed semi-trailer"], ["Color", "Blue"], ["Condition", "New"]]
    },
    zh: {
      name: "蓝色平板半挂车",
      subtitle: "平板 + 前挡",
      summary: "蓝色平板半挂，花纹板台面、前挡和侧工具箱。",
      highlights: ["平板", "前挡", "蓝色", "新车"],
      specs: [["类型", "平板半挂"], ["颜色", "蓝"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-1",
    sku: "YM-NTC-001",
    category: "new",
    type: "tricycle",
    brand: "Yingmotors",
    images: _t1.images,
    thumb: _t1.thumb,
    videos: ymVid("YM-NTC-001", "new-tricycle-1", ["v01.mp4", "v02.mp4"]),
    en: {
      name: "Blue Cabin Dump Tricycle",
      subtitle: "7-speed heavy-duty · thickened hopper",
      summary: "Blue three-wheel dump tricycle with enclosed cab, thickened hopper and 7-speed heavy-duty drive. Videos included.",
      highlights: ["Enclosed cab", "Dump hopper", "7-speed heavy duty", "Videos on this page"],
      specs: [["Type", "Cargo dump tricycle"], ["Color", "Blue"], ["Drive", "7-speed heavy"], ["Condition", "New"]]
    },
    zh: {
      name: "蓝色封闭自卸三轮车",
      subtitle: "七速加重 · 加厚料斗",
      summary: "蓝色三轮自卸，封闭驾驶室、加厚料斗、七速加重。本页含视频。",
      highlights: ["封闭驾驶室", "自卸料斗", "七速加重", "含视频"],
      specs: [["类型", "自卸三轮"], ["颜色", "蓝"], ["驱动", "七速加重"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-2",
    sku: "YM-NTC-002",
    category: "new",
    type: "tricycle",
    brand: "Yingmotors",
    images: _t2.images,
    thumb: _t2.thumb,
    en: {
      name: "Red Hydraulic Dump Tricycle",
      subtitle: "Open cab · twin ram tipper",
      summary: "Red three-wheel dump tricycle with hydraulic rams shown in tipping position. For farm and site short-haul.",
      highlights: ["Hydraulic dump bed", "Open operator station", "Off-road tyres", "New"],
      specs: [["Type", "Dump tricycle"], ["Color", "Red"], ["Condition", "New"]]
    },
    zh: {
      name: "红色液压自卸三轮车",
      subtitle: "开放驾驶 · 双油缸",
      summary: "红色三轮自卸，液压举升料斗，适合农场和工地短途。",
      highlights: ["液压自卸", "开放驾驶", "越野胎", "新车"],
      specs: [["类型", "自卸三轮"], ["颜色", "红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-3",
    sku: "YM-NTC-003",
    category: "new",
    type: "tricycle",
    brand: "Yingmotors",
    images: _t3.images,
    thumb: _t3.thumb,
    en: {
      name: "Blue Luxury Cargo Tricycle",
      subtitle: "Windshield cab · cargo bed",
      summary: "Blue cargo tricycle with windshield, round lamps and deep cargo bed. Marked as latest luxury model.",
      highlights: ["Windshield cab", "Cargo bed", "Blue", "New"],
      specs: [["Type", "Cargo tricycle"], ["Color", "Blue"], ["Condition", "New"]]
    },
    zh: {
      name: "蓝色豪华载货三轮",
      subtitle: "挡风驾驶室 · 货箱",
      summary: "蓝色载货三轮，带挡风玻璃和深货箱，标「最新豪华型」。",
      highlights: ["挡风驾驶室", "货箱", "蓝色", "新车"],
      specs: [["类型", "载货三轮"], ["颜色", "蓝"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-4",
    sku: "YM-NTC-004",
    category: "new",
    type: "tricycle",
    brand: "Liba",
    images: _t4.images,
    thumb: _t4.thumb,
    en: {
      name: "Liba Xiaokang Star Cargo Tricycle",
      subtitle: "力霸 小康之星",
      summary: "Blue Liba Xiaokang Star cargo tricycle, open station, drop-side cargo bed.",
      highlights: ["Liba Xiaokang Star", "Cargo bed", "Blue", "New"],
      specs: [["Brand", "Liba 力霸"], ["Model", "Xiaokang Star"], ["Type", "Cargo tricycle"], ["Condition", "New"]]
    },
    zh: {
      name: "力霸小康之星载货三轮",
      subtitle: "力霸 · 小康之星",
      summary: "蓝色力霸小康之星载货三轮，开放驾驶，栏板货箱。",
      highlights: ["力霸小康之星", "货箱", "蓝色", "新车"],
      specs: [["品牌", "力霸"], ["型号", "小康之星"], ["类型", "载货三轮"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-5",
    sku: "YM-NTC-005",
    category: "new",
    type: "tricycle",
    brand: "Liba",
    images: _t5.images,
    thumb: _t5.thumb,
    en: {
      name: "Liba Xiaokang Star Cabin Tricycle",
      subtitle: "Enclosed screen · cargo",
      summary: "Blue Liba Xiaokang Star with windshield, dual mirrors and cargo body. Factory-floor photo.",
      highlights: ["Cabin windshield", "Cargo body", "Liba badge", "New"],
      specs: [["Brand", "Liba 力霸"], ["Model", "Xiaokang Star"], ["Type", "Cargo tricycle"], ["Condition", "New"]]
    },
    zh: {
      name: "力霸小康之星封闭三轮",
      subtitle: "挡风 · 货箱",
      summary: "蓝色力霸小康之星，带挡风和货箱，厂房实拍。",
      highlights: ["挡风", "货箱", "力霸", "新车"],
      specs: [["品牌", "力霸"], ["型号", "小康之星"], ["类型", "载货三轮"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-6",
    sku: "YM-NTC-006",
    category: "new",
    type: "tricycle",
    brand: "Yingmotors",
    images: _t6.images,
    thumb: _t6.thumb,
    en: {
      name: "Red Passenger Tricycle (Tuk-tuk)",
      subtitle: "Canopy · multi-seat",
      summary: "Red passenger three-wheeler with grey canopy and plastic-wrapped seats. For passenger / last-mile transport.",
      highlights: ["Passenger layout", "Canopy roof", "Red body", "New"],
      specs: [["Type", "Passenger tricycle"], ["Color", "Red"], ["Condition", "New"]]
    },
    zh: {
      name: "红色载客三轮（篷车）",
      subtitle: "篷顶 · 多座",
      summary: "红色载客三轮，灰篷、座椅带保护膜，适合载人短途。",
      highlights: ["载客布局", "篷顶", "红色", "新车"],
      specs: [["类型", "载客三轮"], ["颜色", "红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-tricycle-7",
    sku: "YM-NTC-007",
    category: "new",
    type: "tricycle",
    brand: "Yingmotors",
    images: _t7.images,
    thumb: _t7.thumb,
    en: {
      name: "Red Cargo Tricycle",
      subtitle: "High cargo bed · automobile-quality badge",
      summary: "Red cargo tricycle with ribbed cargo box and front rack. Marked 汽车品质 (automobile quality).",
      highlights: ["Cargo box", "Front rack", "Red", "New"],
      specs: [["Type", "Cargo tricycle"], ["Color", "Red"], ["Condition", "New"]]
    },
    zh: {
      name: "红色载货三轮",
      subtitle: "高货箱 · 汽车品质",
      summary: "红色载货三轮，加强货箱和前护架，标「汽车品质」。",
      highlights: ["货箱", "前护架", "红色", "新车"],
      specs: [["类型", "载货三轮"], ["颜色", "红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-utv-6wheel",
    sku: "YM-NFW-001",
    category: "new",
    type: "fourwheel",
    brand: "Yingmotors",
    images: _f1.images,
    thumb: _f1.thumb,
    en: {
      name: "Red 6-Wheel Off-road UTV",
      subtitle: "Cargo bed · all-terrain",
      summary: "Red six-wheel utility vehicle with cargo bed, roll cage and knobby tyres for farm and site work.",
      highlights: ["6-wheel chassis", "Cargo bed", "Off-road tyres", "New"],
      specs: [["Type", "6-wheel UTV / cargo"], ["Color", "Red"], ["Condition", "New"]]
    },
    zh: {
      name: "红色六轮山地货运车",
      subtitle: "货箱 · 全地形",
      summary: "红色六轮货运 UTV，货箱、防滚架、越野胎，适合农场和工地。",
      highlights: ["六轮", "货箱", "越野胎", "新车"],
      specs: [["类型", "六轮货运"], ["颜色", "红"], ["状态", "新车"]]
    }
  },
  {
    id: "new-4wd-dumper",
    sku: "YM-NFW-002",
    category: "new",
    type: "fourwheel",
    brand: "Yingmotors",
    images: _f2.images,
    thumb: _f2.thumb,
    en: {
      name: "Ace Small 4WD Mini Dumper",
      subtitle: "王牌小四驱",
      summary: "Blue compact 4WD dump truck for quarry, farm and site short-haul. Open cab, tipping cargo bed.",
      highlights: ["4WD mini dumper", "Open cab", "Tipping bed", "New"],
      specs: [["Model", "Ace Small 4WD / 王牌小四驱"], ["Type", "Mini dump truck"], ["Color", "Blue"], ["Condition", "New"]]
    },
    zh: {
      name: "王牌小四驱自卸车",
      subtitle: "四驱小翻斗",
      summary: "蓝色小型四驱自卸，开放驾驶室，适合矿山、农场短途。",
      highlights: ["四驱小翻斗", "开放驾驶室", "自卸货箱", "新车"],
      specs: [["型号", "王牌小四驱"], ["类型", "小型自卸"], ["颜色", "蓝"], ["状态", "新车"]]
    }
  },
  {
    id: "used-komatsu-pc200",
    sku: "YM-UEX-001",
    aliases: ["used-komatsu-pc200-c", "YM-UEX-006", "used-komatsu-pc200-d", "YM-UEX-007"],
    category: "used",
    type: "excavator",
    brand: "Komatsu",
    images: _uk1.images,
    thumb: _uk1.thumb,
    videos: ymVid("YM-UEX-001", "used-komatsu-pc200", ["v01.mp4", "v02.mp4", "v03.mp4"]),
    en: {
      name: "Used Komatsu PC200 Excavator",
      subtitle: "Unit 1 · 20-ton class",
      summary: "First of two PC200 units in stock — same model as unit 2, different machine. Front, side, rear and workshop photos of this unit, plus walk-around videos. Yellow crawler with PC 200 side panel; engine cover open in the workshop shots.",
      highlights: ["Komatsu PC200 · unit 1", "Approx. 20 ton", "Multi-angle photos + videos", "Used, in stock"],
      specs: [["Brand", "Komatsu"], ["Model", "PC200"], ["Unit", "1 of 2 in stock"], ["Class", "Approx. 20 ton"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手小松 PC200 挖掘机",
      subtitle: "1 号车 · 20 吨级",
      summary: "现车两台 PC200 中的第一台，与 2 号车同型号、不是同一台。含本车正面、侧面、后面及车间实拍，以及绕车视频。侧板 PC 200 标识，车间照片可见发动机舱打开。",
      highlights: ["小松 PC200 · 1 号车", "约 20 吨", "多角度实拍 + 视频", "二手现车"],
      specs: [["品牌", "小松"], ["型号", "PC200"], ["车号", "现车 1 号"], ["吨位", "约 20 吨"], ["状态", "二手"]]
    }
  },
  {
    id: "used-komatsu-pc200-b",
    sku: "YM-UEX-002",
    category: "used",
    type: "excavator",
    brand: "Komatsu",
    images: _uk2.images,
    thumb: _uk2.thumb,
    en: {
      name: "Used Komatsu PC200 Excavator",
      subtitle: "Unit 2 · 20-ton class",
      summary: "Second PC200 in stock — same model as unit 1, different machine. Yard photo with SOKUTO markings and other machines in the background.",
      highlights: ["Komatsu PC200 · unit 2", "Approx. 20 ton", "Separate machine from unit 1", "Used, in stock"],
      specs: [["Brand", "Komatsu"], ["Model", "PC200"], ["Unit", "2 of 2 in stock"], ["Class", "Approx. 20 ton"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手小松 PC200 挖掘机",
      subtitle: "2 号车 · 20 吨级",
      summary: "现车两台 PC200 中的第二台，与 1 号车同型号、不是同一台。场地实拍，侧有 SOKUTO 标识。",
      highlights: ["小松 PC200 · 2 号车", "约 20 吨", "与 1 号车不是同一台", "二手现车"],
      specs: [["品牌", "小松"], ["型号", "PC200"], ["车号", "现车 2 号"], ["吨位", "约 20 吨"], ["状态", "二手"]]
    }
  },
  {
    id: "used-komatsu-pc130",
    sku: "YM-UEX-003",
    category: "used",
    type: "excavator",
    brand: "Komatsu",
    images: _uk3.images,
    thumb: _uk3.thumb,
    en: {
      name: "Used Komatsu PC130 Excavator",
      subtitle: "13-ton class",
      summary: "Used Komatsu PC130 hydraulic excavator for urban and road work.",
      highlights: ["Komatsu PC130", "Mid-size", "Crawler", "Used"],
      specs: [["Brand", "Komatsu"], ["Model", "PC130"], ["Class", "Approx. 13 ton"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手小松 PC130 挖掘机",
      subtitle: "13 吨级",
      summary: "二手小松 PC130，适合市政和道路工程。",
      highlights: ["小松 PC130", "中型", "履带", "二手"],
      specs: [["品牌", "小松"], ["型号", "PC130"], ["吨位", "约 13 吨"], ["状态", "二手"]]
    }
  },
  {
    id: "used-komatsu-pc70",
    sku: "YM-UEX-004",
    category: "used",
    type: "excavator",
    brand: "Komatsu",
    images: _uk4.images,
    thumb: _uk4.thumb,
    en: {
      name: "Used Komatsu PC70 Excavator",
      subtitle: "7-ton class",
      summary: "Used Komatsu PC70 compact crawler excavator.",
      highlights: ["Komatsu PC70", "Compact class", "Used export"],
      specs: [["Brand", "Komatsu"], ["Model", "PC70"], ["Class", "Approx. 7 ton"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手小松 PC70 挖掘机",
      subtitle: "7 吨级",
      summary: "二手小松 PC70 小型履带挖掘机。",
      highlights: ["小松 PC70", "小型", "二手出口"],
      specs: [["品牌", "小松"], ["型号", "PC70"], ["吨位", "约 7 吨"], ["状态", "二手"]]
    }
  },
  {
    id: "used-komatsu-pc56",
    sku: "YM-UEX-005",
    category: "used",
    type: "excavator",
    brand: "Komatsu",
    images: _uk5.images,
    thumb: _uk5.thumb,
    en: {
      name: "Used Komatsu PC56 Excavator",
      subtitle: "Small excavator",
      summary: "Used Komatsu PC56, container-friendly size for light construction.",
      highlights: ["Komatsu PC56", "Small class", "Used"],
      specs: [["Brand", "Komatsu"], ["Model", "PC56"], ["Class", "Small"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手小松 PC56 挖掘机",
      subtitle: "小型挖掘机",
      summary: "二手小松 PC56，便于装箱发运。",
      highlights: ["小松 PC56", "小型", "二手"],
      specs: [["品牌", "小松"], ["型号", "PC56"], ["吨位", "小型"], ["状态", "二手"]]
    }
  },
  {
    id: "used-sdlg-loader",
    sku: "YM-ULD-001",
    category: "used",
    type: "loader",
    brand: "SDLG",
    images: _sdl.images,
    thumb: _sdl.thumb,
    en: {
      name: "Used SDLG Wheel Loader",
      subtitle: "Yellow front-end loader · factory photos",
      summary: "SDLG wheel loader photographed at the plant: full machine, outdoor lineup, engine bay and dual ADKAI batteries.",
      highlights: ["SDLG wheel loader", "Yellow bucket and arms", "Engine and battery photos", "Used / plant stock"],
      specs: [["Brand", "SDLG 临工"], ["Type", "Wheel loader"], ["Color", "Yellow"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手临工 SDLG 装载机",
      subtitle: "黄色轮式装载机 · 厂房实拍",
      summary: "临工轮式装载机。含整机、成排现车、发动机舱和双电瓶实拍。",
      highlights: ["临工 SDLG 装载机", "黄色料斗", "含发动机 / 电瓶照片", "二手现车"],
      specs: [["品牌", "临工 SDLG"], ["类型", "轮式装载机"], ["颜色", "黄色"], ["状态", "二手"]]
    }
  },
  {
    id: "used-mixer-cimc",
    sku: "YM-UMX-001",
    category: "used",
    type: "mixer",
    brand: "CIMC",
    images: _um.images,
    thumb: _um.thumb,
    en: {
      name: "Used CIMC Concrete Mixer",
      subtitle: "White mixer drum · CIMC 中集",
      summary: "White concrete mixer with CIMC (中集) branded drum and chute. Used construction mixer.",
      highlights: ["CIMC mixer drum", "White unit", "Used"],
      specs: [["Brand", "CIMC 中集"], ["Type", "Concrete mixer truck"], ["Color", "White"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手中集混凝土搅拌车",
      subtitle: "白色搅拌罐 · 中集",
      summary: "白色搅拌车，罐体中集 CIMC 标识。",
      highlights: ["中集搅拌罐", "白色", "二手"],
      specs: [["品牌", "中集 CIMC"], ["类型", "搅拌车"], ["颜色", "白"], ["状态", "二手"]]
    }
  },
  {
    id: "used-shacman-mixer",
    sku: "YM-UMX-002",
    category: "used",
    type: "mixer",
    brand: "SHACMAN",
    images: _smx.images,
    thumb: _smx.thumb,
    en: {
      name: "Used SHACMAN Mixer (M3000S)",
      subtitle: "350 hp · China VI · white",
      summary: "White SHACMAN M3000S mixer, door badge 350 hp China VI. Four-axle chassis, white drum. Photographed on the export lot.",
      highlights: ["SHACMAN M3000S mixer", "350 hp China VI", "White cab and drum", "Used export"],
      specs: [["Brand", "SHACMAN"], ["Model", "M3000S"], ["Engine", "350 hp class"], ["Emission", "China VI"], ["Type", "Concrete mixer truck"], ["Color", "White"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手陕汽搅拌车（M3000S）",
      subtitle: "350 马力 · 国六 · 白色",
      summary: "白色陕汽 M3000S 搅拌车，车门 350 国六。四轴，白色罐体。出口车场实拍。",
      highlights: ["陕汽 M3000S 搅拌车", "350 马力国六", "白色驾驶室与罐体", "二手出口"],
      specs: [["品牌", "陕汽 SHACMAN"], ["型号", "M3000S"], ["发动机", "350 马力级"], ["排放", "国 VI"], ["类型", "搅拌车"], ["颜色", "白"], ["状态", "二手"]]
    }
  },
  {
    id: "used-bus",
    sku: "YM-UBS-001",
    category: "used",
    type: "bus",
    brand: "Yingmotors",
    images: [
      _ub.images[4],
      _ub.images[0],
      _ub.images[1],
      _ub.images[2],
      _ub.images[3],
      _ub.images[5],
      _ub.images[6]
    ],
    thumb: _ub.thumb,
    videos: ymVid("YM-UBS-001", "used-bus", ["v01.mp4"]),
    en: {
      name: "Used Coach Bus (Blue / White)",
      subtitle: "Coach interior · Senegal-ready seats",
      summary: "Blue-and-white coach with 2+2 seats still in plastic. Headrests marked Senegal voyages. Exterior and cabin photos plus video.",
      highlights: ["Coach / tour bus", "2+2 seats, overhead racks", "Custom headrest option", "Video available"],
      specs: [["Type", "Coach bus"], ["Color", "Blue / white"], ["Seats", "2+2, high-back"], ["Condition", "Used / refurbished look"]]
    },
    zh: {
      name: "二手大巴（蓝白）",
      subtitle: "客车内饰 · 可出口座椅",
      summary: "蓝白客车，2+2 座椅仍带保护膜，头枕有 Senegal voyages 标识。含外观、驾驶室和视频。",
      highlights: ["长途客车", "2+2 高背座", "可定制头枕", "含视频"],
      specs: [["类型", "客车 / 大巴"], ["颜色", "蓝白"], ["座位", "2+2 高背"], ["状态", "二手"]]
    }
  },
  {
    id: "used-bus-yutong",
    sku: "YM-UBS-002",
    category: "used",
    type: "bus",
    brand: "Yutong",
    images: _ug.images,
    thumb: _ug.thumb,
    en: {
      name: "Used Yutong Coach (Green)",
      subtitle: "Yutong · Essamaye FC / Valdeu Express livery",
      summary: "Yutong high-deck coach, dark green over bright green bumper. Interior seats wrapped; headrests Essamaye FC Ziguinchor.",
      highlights: ["Yutong coach", "Green two-tone body", "Wrapped interior seats", "Export livery"],
      specs: [["Brand", "Yutong"], ["Type", "High-deck coach"], ["Color", "Green"], ["Condition", "Used"]]
    },
    zh: {
      name: "二手宇通客车（绿色）",
      subtitle: "宇通 · Essamaye FC 涂装",
      summary: "宇通高一级客车，深绿车身、亮绿保险杠。座椅带膜，头枕 Essamaye FC Ziguinchor。",
      highlights: ["宇通客车", "绿色双色", "座椅带保护膜", "出口涂装"],
      specs: [["品牌", "宇通"], ["类型", "高一级客车"], ["颜色", "绿"], ["状态", "二手"]]
    }
  }
];

window.YM_FEATURED_IDS = [
  "used-sitrak-g7s",
  "used-shacman-x3000",
  "used-howo-dump-red",
  "used-sdlg-loader",
  "used-komatsu-pc200",
  "used-shacman-mixer"
];

window.YM = window.YM || {};

YM.getLang = function () {
  return localStorage.getItem("ym-lang") === "zh" ? "zh" : "en";
};

YM.setLang = function (lang) {
  localStorage.setItem("ym-lang", lang === "zh" ? "zh" : "en");
};

YM.productById = function (id) {
  if (!id) return undefined;
  var raw = String(id).trim();
  var key = raw.toUpperCase();
  return YM_PRODUCTS.find(function (p) {
    if (p.id === raw || (p.sku && p.sku.toUpperCase() === key)) return true;
    var aliases = p.aliases || [];
    for (var i = 0; i < aliases.length; i++) {
      if (aliases[i] === raw || String(aliases[i]).toUpperCase() === key) return true;
    }
    return false;
  });
};

YM.tProduct = function (product) {
  return product[YM.getLang()] || product.en;
};

YM.productRef = function (product) {
  if (!product) return "";
  var name = YM.tProduct(product).name;
  return product.sku ? product.sku + " " + name : name;
};

YM.pageProduct = function () {
  var id = new URLSearchParams(location.search).get("id");
  return YM.productById(id || "");
};

YM.skuOf = function (product, fallback) {
  if (product && product.sku) return product.sku;
  var text = String(fallback || "").trim();
  var match = text.match(/\bYM-[A-Z0-9]+-\d+\b/i);
  return match ? match[0].toUpperCase() : "";
};

YM.contactGreeting = function (product) {
  if (product === undefined) product = YM.pageProduct();
  var lang = YM.getLang();
  var sku = YM.skuOf(product);
  if (lang === "zh") {
    return sku
      ? "您好，我来自 Yingmotors 网站，关注现车编号 " + sku + "。"
      : "您好，我来自 Yingmotors 网站。";
  }
  return sku
    ? "Hello, I found you from the Yingmotors website. I am interested in STOCK NO " + sku + "."
    : "Hello, I found you from the Yingmotors website.";
};

YM.whatsappLink = function (product) {
  return "https://wa.me/8618053729906?text=" + encodeURIComponent(YM.contactGreeting(product));
};

YM.mailtoLink = function (product) {
  if (product === undefined) product = YM.pageProduct();
  var sku = YM.skuOf(product);
  var subject = sku ? "STOCK NO " + sku + " — Yingmotors" : "Inquiry — Yingmotors";
  return "mailto:yingmotorsinfo@gmail.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(YM.contactGreeting(product));
};

YM.matchesFilter = function (p, filter) {
  if (!filter || filter === "all") return true;
  if (filter === "new" || filter === "used") return p.category === filter;
  if (filter === "light") return p.type === "tricycle" || p.type === "fourwheel";
  if (filter === "machinery") return p.type === "excavator" || p.type === "loader" || p.type === "mixer" || p.type === "special";
  return p.type === filter;
};

YM.matchesQuery = function (p, q) {
  var t = String(q || "").trim().toLowerCase();
  if (!t) return true;
  var hay = [
    p.sku, p.id, p.brand, p.type, p.category,
    p.en && p.en.name, p.en && p.en.subtitle,
    p.zh && p.zh.name, p.zh && p.zh.subtitle
  ].concat(p.aliases || []).join(" ").toLowerCase();
  return hay.indexOf(t) !== -1;
};

YM.renderCards = function (target, products, options) {
  var el = typeof target === "string" ? document.querySelector(target) : target;
  if (!el) return;
  var lang = YM.getLang();
  var opts = options || {};
  el.innerHTML = products.map(function (p) {
    var t = p[lang];
    var badge = p.category === "used"
      ? (lang === "zh" ? "二手" : "Used")
      : (lang === "zh" ? "新车" : "New");
    return (
      '<a class="card" href="product.html?id=' + p.id + '">' +
        '<div class="card-media">' +
          '<img src="' + p.thumb + '" alt="' + t.name + '" loading="lazy">' +
          '<span class="badge">' + badge + "</span>" +
        "</div>" +
        '<div class="card-body">' +
          (p.sku ? '<p class="card-sku">' + p.sku + "</p>" : "") +
          '<p class="card-brand">' + p.brand + "</p>" +
          "<h3>" + t.name + "</h3>" +
          '<p class="card-sub">' + t.subtitle + "</p>" +
          (opts.compact ? "" : '<span class="card-link">' + (lang === "zh" ? "查看详情" : "View details") + "</span>") +
        "</div>" +
      "</a>"
    );
  }).join("");
};
