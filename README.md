# 绝区零 - 仪玄角色资料数据集

> 从 BWIKI 爬取的绝区零角色"仪玄"的完整资料，分类整理

## 📋 数据内容

| 文件 | 内容 | 格式 |
|:---|:---|:---|
| `01_basic_info.json` | 基础信息（阵营、属性、CV等） | JSON |
| `02_official_intro.txt` | 官方介绍 | TXT |
| `03_detailed_info.txt` | 详细情报（背景故事） | TXT |
| `04_cooperation.txt` | 合作备注 | TXT |
| `05_story.txt` | 剧情相关 | TXT |
| `06_skills.json` | 技能信息（21个技能） | JSON |
| `07_voices.json` | 语音台词（32条） | JSON |
| `yixuan_complete.json` | 所有数据合并 | JSON |

## 🎭 角色简介

**仪玄**是绝区零中的限定UP角色，云岿山第十三代门主。

- **阵营**：云岿山
- **属性**：玄墨
- **特性**：命破
- **伤害类型**：打击
- **生日**：12月3日
- **身高**：172cm
- **中文CV**：张昱
- **日文CV**：能登麻美子

## 📊 数据统计

| 数据类型 | 数量 |
|:---|:---:|
| 基础信息 | 20 项 |
| 技能 | 21 个 |
| 语音台词 | 32 条 |
| 背景故事 | ~1700 字 |

## 🔧 爬虫脚本

`crawl_yixuan.py` - 从 BWIKI 爬取仪玄资料

```bash
python crawl_yixuan.py
```

## 📄 License

数据来源：[BWIKI - 绝区零](https://wiki.biligame.com/zzz/)
仅供学习研究使用，游戏内容版权归米哈游所有。
