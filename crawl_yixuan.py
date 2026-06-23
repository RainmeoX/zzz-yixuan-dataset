"""
绝区零 - 仪玄角色资料爬虫
从 BWIKI 爬取仪玄的所有信息，分类整理
"""
import re
import json
import html as html_module
import os
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

OUTPUT_DIR = "/home/z/my-project/download/zzz_yixuan_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_page(url):
    """抓取页面"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.encoding = 'utf-8'
        return resp.text
    except Exception as e:
        print(f"抓取失败: {e}")
        return None


def clean_text(text):
    """清理 HTML 标签和空白"""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_module.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_section(html, section_name, next_sections=None):
    """提取指定标题下的内容"""
    # 找标题位置
    pattern = rf'<span class="mw-headline"[^>]*>{section_name}</span>'
    match = re.search(pattern, html)
    if not match:
        return ""
    
    start = match.start()
    
    # 找下一个标题
    end = len(html)
    if next_sections:
        for ns in next_sections:
            next_pattern = rf'<span class="mw-headline"[^>]*>{ns}</span>'
            next_match = re.search(next_pattern, html[start+10:])
            if next_match:
                end = start + 10 + next_match.start()
                break
    else:
        # 找任意下一个标题
        next_match = re.search(r'<span class="mw-headline"', html[start+10:])
        if next_match:
            end = start + 10 + next_match.start()
    
    section = html[start:end]
    return clean_text(section)


def extract_basic_info(html):
    """提取基础信息表"""
    info = {}
    # 找 th/td 对
    pairs = re.findall(r'<th[^>]*>([^<]+)</th>\s*<td[^>]*>(.*?)</td>', html, re.DOTALL)
    for k, v in pairs:
        k_clean = clean_text(k)
        v_clean = clean_text(v)
        if k_clean and v_clean and len(k_clean) < 20:
            info[k_clean] = v_clean
    return info


def extract_skills(html):
    """提取技能信息"""
    skills = []
    # 找技能标题和描述
    # 技能通常在表格里
    skill_tables = re.findall(r'<table[^>]*class="[^"]*wikitable[^"]*"[^>]*>(.*?)</table>', html, re.DOTALL)
    for table in skill_tables[:10]:
        # 找技能名和描述
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 2:
                name = clean_text(cells[0])
                desc = clean_text(' '.join(cells[1:]))
                if name and desc and len(name) < 30 and len(desc) > 10:
                    skills.append({"name": name, "description": desc})
    return skills


def extract_voice_lines(html):
    """提取语音台词（从「」引号内容中提取）"""
    voices = []
    # 找所有「...」内容
    quoted = re.findall(r'「([^」]{5,200})」', html)
    
    # 过滤掉技能名
    skill_keywords = ['攻击', '技', '强化', '终结', '普攻', '闪避', '支援', '连携']
    
    for q in quoted:
        q_clean = re.sub(r'<[^>]+>', '', q).strip()
        if not q_clean or len(q_clean) < 5:
            continue
        # 排除技能名
        if any(kw in q_clean for kw in skill_keywords) and len(q_clean) < 15:
            continue
        # 排除纯技能描述
        if q_clean.startswith('强化') or q_clean.startswith('终结') or q_clean.startswith('普通'):
            continue
        # 只要包含中文标点的才算台词
        if any(p in q_clean for p in '。，！？…—'):
            voices.append({"scene": "台词", "text": q_clean})
    
    # 去重
    seen = set()
    unique_voices = []
    for v in voices:
        if v["text"] not in seen:
            seen.add(v["text"])
            unique_voices.append(v)
    
    return unique_voices


def main():
    print("=" * 60)
    print("绝区零 - 仪玄角色资料爬取")
    print("=" * 60)
    
    # 1. 爬取仪玄主页面
    print("\n[1/4] 爬取仪玄主页面...")
    url = "https://wiki.biligame.com/zzz/%E4%BB%AA%E7%8E%84"
    html = fetch_page(url)
    if not html:
        print("爬取失败！")
        return
    
    print(f"页面大小: {len(html)} 字符")
    
    # 2. 提取各类信息
    print("\n[2/4] 提取角色信息...")
    
    # 基础信息
    basic_info = extract_basic_info(html)
    print(f"基础信息: {len(basic_info)} 项")
    
    # 详细情报
    detail = extract_section(html, "详细情报", ["合作备注", "剧情相关"])
    print(f"详细情报: {len(detail)} 字符")
    
    # 官方介绍
    intro = extract_section(html, "官方介绍", ["详细情报"])
    print(f"官方介绍: {len(intro)} 字符")
    
    # 合作备注
    cooperation = extract_section(html, "合作备注", ["剧情相关"])
    print(f"合作备注: {len(cooperation)} 字符")
    
    # 剧情相关
    story = extract_section(html, "剧情相关", ["活动相关"])
    print(f"剧情相关: {len(story)} 字符")
    
    # 技能
    skills = extract_skills(html)
    print(f"技能: {len(skills)} 个")
    
    # 语音台词
    voices = extract_voice_lines(html)
    print(f"语音台词: {len(voices)} 条")
    
    # 3. 整理数据
    print("\n[3/4] 整理数据...")
    
    dataset = {
        "character": {
            "name": "仪玄",
            "game": "绝区零",
            "source": "https://wiki.biligame.com/zzz/%E4%BB%AA%E7%8E%84"
        },
        "basic_info": basic_info,
        "official_intro": intro,
        "detailed_info": detail,
        "cooperation": cooperation,
        "story": story,
        "skills": skills,
        "voices": voices
    }
    
    # 4. 保存
    print("\n[4/4] 保存数据...")
    
    # 完整数据
    with open(f"{OUTPUT_DIR}/yixuan_complete.json", 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    # 分类保存
    with open(f"{OUTPUT_DIR}/01_basic_info.json", 'w', encoding='utf-8') as f:
        json.dump(basic_info, f, ensure_ascii=False, indent=2)
    
    with open(f"{OUTPUT_DIR}/02_official_intro.txt", 'w', encoding='utf-8') as f:
        f.write(intro)
    
    with open(f"{OUTPUT_DIR}/03_detailed_info.txt", 'w', encoding='utf-8') as f:
        f.write(detail)
    
    with open(f"{OUTPUT_DIR}/04_cooperation.txt", 'w', encoding='utf-8') as f:
        f.write(cooperation)
    
    with open(f"{OUTPUT_DIR}/05_story.txt", 'w', encoding='utf-8') as f:
        f.write(story)
    
    with open(f"{OUTPUT_DIR}/06_skills.json", 'w', encoding='utf-8') as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)
    
    with open(f"{OUTPUT_DIR}/07_voices.json", 'w', encoding='utf-8') as f:
        json.dump(voices, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到: {OUTPUT_DIR}")
    print(f"文件列表:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size = os.path.getsize(f"{OUTPUT_DIR}/{f}")
        print(f"  {f} ({size} bytes)")
    
    # 打印预览
    print(f"\n=== 基础信息 ===")
    for k, v in basic_info.items():
        print(f"  {k}: {v}")
    
    print(f"\n=== 详细情报（前500字）===")
    print(detail[:500])
    
    print(f"\n=== 语音台词示例 ===")
    for v in voices[:5]:
        print(f"  [{v['scene']}] {v['text'][:60]}")


if __name__ == "__main__":
    main()
