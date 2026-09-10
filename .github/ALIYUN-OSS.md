# 阿里云 OSS 部署说明

YING MOTORS 静态站通过 GitHub Actions 发布到新加坡 OSS。产品图仍走 Cloudflare R2（`webimages.yingmotors.com`），不要把 `images/` 传到 OSS。

线上站点：

- `http://www.yingmotors.net/`
- GitHub 仓库：`LucyLynsky/yingmotorsweb`
- Workflow：`.github/workflows/deploy.yml`
- 图片同步：`.github/workflows/sync-r2.yml`

---

## 1. 架构

```text
push main
 ├─ web/** 或 deploy.yml 变化  →  Deploy to Aliyun OSS  →  桶 aliyingmotorsweb
 └─ resource/images/**        →  Sync images to R2   →  Cloudflare R2
```

GitHub 仓库里站点在 `web/` 目录。上线只传 HTML / CSS / JS / `assets/` / `contact/` / `product/` 等，排除 `.cursor/`、`docs/`、`images/`、原片目录。

---

## 2. GitHub Secrets

仓库 **Settings → Secrets and variables → Actions**：

| Secret | 正确值 | 不要填 |
| --- | --- | --- |
| `ALI_OSS_BUCKET` | `aliyingmotorsweb` | `oss://...` |
| `ALI_OSS_ENDPOINT` | `oss-ap-southeast-1.aliyuncs.com` | 内网 `-internal`、带 `https://`、Bucket 域名 |
| `ALI_ACCESS_KEY_ID` | RAM AccessKey，`LTAI` 开头 | 登录名 `xxx@....onaliyun.com`、ARN、用户 ID |
| `ALI_ACCESS_KEY_SECRET` | 创建 AccessKey 时的密钥 | — |

Endpoint 在 OSS 桶 **概览 → 访问端口 → 外网访问 → 地域节点**。新加坡就是上面这一条。

---

## 3. RAM 用户

1. 访问控制 RAM → 用户，使用 `aliyingmotors`（须与 OSS 同一账号）。
2. **认证管理** 里创建 AccessKey，填进上面两个 Secret。
3. **添加权限**，勾选 **`AliyunOSSFullAccess`**，点确定。  
   权限授给用户，不是单独授给 Key。没这步会 403：`The bucket you access does not belong to you`。
4. 不要勾 `AdministratorAccess`。

---

## 4. OSS 桶设置

桶：`aliyingmotorsweb`，地域 **新加坡**。

| 项 | 设置 |
| --- | --- |
| 权限控制 → 阻止公共访问 | **关闭** |
| 权限控制 → 读写权限 | **公共读**，点「设置」保存 |
| 数据管理 → 静态页面 | 开启；默认首页 `index.html`；404 可填 `index.html` |
| 域名管理 | 绑定 `www.yingmotors.net`（根域名 `yingmotors.net` 在 Cloudflare 上不易检验 CNAME） |

访客打开 `/` 必须靠静态页面，否则只有 `.../index.html` 能开、根路径会 XML 报错。

---

## 5. Cloudflare DNS（`yingmotors.net`）

必须改 **`yingmotors.net`**（有 s），不是 `yingmotor.net`。

验证所有权（绑域名时阿里云会给值，过期后以控制台为准）：

| 类型 | 名称 | 内容 | 代理 |
| --- | --- | --- | --- |
| TXT | `_dnsauth` | 控制台给的哈希 | 仅 DNS（灰云） |

网站解析：

| 类型 | 名称 | 目标 | 代理 |
| --- | --- | --- | --- |
| CNAME | `www` | `aliyingmotorsweb.ap-southeast-1.thepacificmax.com` | 仅 DNS |

名称只填 `_dnsauth` / `www`，不要写成 `xxx.yingmotors.net`。  
根域名 `@` 在 Cloudflare 会被压成 A 记录，阿里云检验 CNAME 常显示「未生效」，所以站点用 **www**。

可选：用 Cloudflare 把 `yingmotors.net` 跳转到 `www.yingmotors.net`。  
先不要开「已代理」，否则检验更容易失败。

---

## 6. 日常发布

改完 `web/` 推到 `main`，Actions 里 **Deploy to Aliyun OSS** 变绿即已上传。  
也可手动 **Run workflow**。

本地 `E:\codePrj\web` 若不是这个 Git 仓库，改 workflow 后要同步到 `LucyLynsky/yingmotorsweb` 再推。

---

## 7. 常见错误

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `status=-2` 连不上 | Endpoint 填了内网，或填了登录名当 Key | 外网 `oss-ap-southeast-1.aliyuncs.com`；Key 用 `LTAI` |
| `403 The bucket you access does not belong to you`（Actions） | RAM 无 OSS 权限，或账号不一致 | `AliyunOSSFullAccess`；同一账号 |
| `Anonymous user has no right to access this bucket` | 桶私有，或「阻止公共访问」开着 | 公共读 + 关掉阻止公共访问 |
| 浏览器 HostId 是 `www`，报 bucket 不属于你 | 只绑了根域名 | OSS 再绑 `www.yingmotors.net` |
| 只有 `/index.html` 能开，`/` 不行 | 未开静态页面 | 默认首页 `index.html` 并保存 |
| `NeedVerifyDomainOwnership` | 未加 TXT | Cloudflare 加 `_dnsauth` TXT |
| 域名绑定未生效 | 根域名 CNAME 被 flattening | 改绑 `www` |
| Node 20 弃用警告 | `actions/checkout@v4` | 已改 `@v5`，可忽略 |

HTTPS「不安全」：页面能开之后，在 OSS 域名管理给 `www.yingmotors.net` 申请免费证书。
