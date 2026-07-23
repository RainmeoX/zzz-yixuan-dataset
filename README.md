# 绝区零「仪玄」角色资料数据集

从多个网站爬取的绝区零角色"仪玄"的完整资料，分类整理，用于微调训练。

## 项目背景

给 [zzz-yixuan-assistant](https://github.com/RainmeoX/zzz-yixuan-assistant) 准备角色数据：基础信息、技能、语音台词、背景故事。目标是让模型"知道"这个角色，而不只是会说话。

## 数据来源

| 来源 | 状态 | 台词数 | 说明 |
|---|---|---|---|
| BWIKI | ✅ | 32 条 | requests 直连，无反爬 |
| 米哈游百科 | ✅ | 17 条 | SPA 应用，Playwright 渲染 |
| Gamekee | ✅ | 4 条 | SPA 应用，Playwright 渲染 |
| Fandom | ❌ | 0 | Cloudflare 防护，未绕过 |
| 萌娘百科 | ❌ | 0 | Cloudflare 403 |

合并去重后总台词 40 条；技能 21 个；背景故事约 1700 字。

## 数据文件

| 文件 | 内容 | 来源 |
|---|---|---|
| `01_basic_info.json` | 基础信息（阵营 / 属性 / CV 等） | BWIKI |
| `06_skills.json` | 技能信息（21 个） | BWIKI |
| `07_voices.json` | 语音台词（32 条） | BWIKI |
| `all_voices_merged.json` | 所有台词合并去重（40 条） | 多源合并 |
| `yixuan_complete.json` | BWIKI 所有数据合并 | BWIKI |
| `crawl_yixuan.py` | BWIKI 爬虫脚本 | - |

## 我的工作

- 写 BWIKI 直连爬虫
- 用 Playwright 处理 SPA 页面（米哈游百科 / Gamekee）
- 多源合并去重

## 遇到的问题

- **Cloudflare 防护**：Fandom / 萌娘百科有 Turnstile 验证和 403，headless 浏览器和 `curl_cffi` 模拟 TLS 指纹都没绕过
- SPA 页面需要拦截 API 请求才能拿到 `entry_id`，不能直接抓 HTML

## 项目不足

- 只覆盖单个角色，规模小
- Fandom / 萌娘百科的数据缺失
- 未做严格人工校验

## 后续计划

- 扩展到更多角色
- 继续尝试处理 Cloudflare 站点（如换更完整的浏览器环境）

## Reflection

爬虫最难的不是发请求，而是和对抗式站点打交道。这个仓库让我积累了 Playwright 和请求指纹的实战经验，也让我更尊重网站的防护机制——爬取要适度、要合规。

## License

数据来源：BWIKI / 米哈游百科 / Gamekee。仅供学习研究使用，游戏内容版权归米哈游所有。
