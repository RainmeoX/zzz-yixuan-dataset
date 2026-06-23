# 绝区零 - 仪玄角色资料数据集

> 从多个网站爬取的绝区零角色"仪玄"的完整资料，分类整理

## 📋 数据来源

| 来源 | 状态 | 台词数 | 说明 |
|:---|:---:|:---:|:---|
| **BWIKI** | ✅ | 32条 | 哔哩哔哩游戏百科 |
| **米哈游百科** | ✅ | 17条 | 官方百科（Playwright渲染） |
| **Gamekee** | ✅ | 4条 | 游戏百科（Playwright渲染） |
| **Fandom** | ❌ | 0 | Cloudflare防护，无法绕过 |
| **萌娘百科** | ❌ | 0 | Cloudflare防护，无法绕过 |

**合并去重后总台词：40条**

## 📁 数据文件

| 文件 | 内容 | 来源 |
|:---|:---|:---|
| `01_basic_info.json` | 基础信息（阵营、属性、CV等） | BWIKI |
| `02_official_intro.txt` | 官方介绍 | BWIKI |
| `03_detailed_info.txt` | 详细情报（背景故事） | BWIKI |
| `04_cooperation.txt` | 合作备注 | BWIKI |
| `06_skills.json` | 技能信息（21个技能） | BWIKI |
| `07_voices.json` | 语音台词（32条） | BWIKI |
| `mihoyo_full.json` | 米哈游百科完整数据 | 米哈游百科 |
| `gamekee_full.json` | Gamekee完整数据 | Gamekee |
| `all_voices_merged.json` | 所有台词合并去重（40条） | 多源合并 |
| `yixuan_complete.json` | BWIKI所有数据合并 | BWIKI |
| `crawl_yixuan.py` | BWIKI爬虫脚本 | - |

## 🎭 角色简介

**仪玄**是绝区零中的限定UP角色，云岿山第十三代门主。

- **阵营**：云岿山
- **属性**：玄墨
- **特性**：命破
- **生日**：12月3日
- **身高**：172cm
- **中文CV**：张昱
- **日文CV**：能登麻美子

## 📊 数据统计

| 数据类型 | 数量 |
|:---|:---:|
| 基础信息 | 20 项 |
| 技能 | 21 个 |
| 语音台词（去重） | 40 条 |
| 背景故事 | ~1700 字 |

## 🔧 爬虫技术说明

### 成功爬取的网站

1. **BWIKI**：直接requests请求，无反爬
2. **米哈游百科**：SPA应用，用Playwright渲染 + 拦截API请求找到entry_id
3. **Gamekee**：SPA应用，用Playwright渲染 + 搜索找到角色页面

### 未能爬取的网站

1. **Fandom**：Cloudflare Turnstile验证，headless浏览器无法通过
2. **萌娘百科**：Cloudflare 403 Forbidden，API需要授权

### 使用的技术

- `requests`：直接请求（BWIKI）
- `Playwright`：浏览器渲染（米哈游百科、Gamekee）
- `curl_cffi`：模拟Chrome TLS指纹（尝试绕过Cloudflare，未成功）

## 📄 License

数据来源：
- [BWIKI - 绝区零](https://wiki.biligame.com/zzz/)
- [米哈游百科](https://baike.mihoyo.com/zzz/wiki/)
- [Gamekee](https://www.gamekee.com/zzz/)

仅供学习研究使用，游戏内容版权归米哈游所有。
