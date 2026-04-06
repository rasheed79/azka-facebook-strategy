"""
generate_facebook_report.py
Reads competitors_raw.json and generates a detailed comparison report + gap analysis.
Output: .tmp/competitor_comparison.md
"""

import json
import os
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "reports", "competitors_raw.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "reports", "competitor_comparison.md")


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_followers(val):
    if isinstance(val, int):
        if val >= 1000:
            return f"{val//1000}K"
        return str(val)
    return str(val)


def score_page(c):
    """Score a page 0-100 based on available data."""
    score = 0
    # Followers (max 30 pts)
    f = c.get("followers", 0)
    if isinstance(f, int):
        if f >= 30000: score += 30
        elif f >= 10000: score += 22
        elif f >= 1000: score += 12
        elif f >= 100: score += 5
    # Activity (max 25 pts)
    freq = c.get("post_frequency", "")
    if "Daily" in freq: score += 25
    elif "Weekly" in freq: score += 18
    elif "Unknown" not in freq and freq: score += 10
    # Verified (5 pts)
    if c.get("verified"): score += 5
    # About quality (max 15 pts)
    bio = c.get("bio_ar") or c.get("bio_en") or ""
    if len(str(bio)) > 100: score += 15
    elif len(str(bio)) > 30: score += 8
    # Contact info (10 pts)
    if c.get("phone") or c.get("email"): score += 5
    if c.get("website"): score += 5
    # Public visibility (15 pts)
    if c.get("posts_visible_without_login"): score += 15
    return min(score, 100)


def generate_report(data):
    competitors = data["competitors"]
    key_findings = data["key_findings"]
    date_str = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append(f"# تقرير تحليل المنافسين على فيسبوك - أزكى لتقنية المعلومات")
    lines.append(f"**تاريخ التقرير:** {date_str}")
    lines.append(f"**المصدر:** تحليل الصفحات العامة على فيسبوك + البحث على الويب")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## ملخص تنفيذي")
    lines.append("")
    lines.append("### أبرز النتائج:")
    lines.append(f"- **{key_findings['market_observation']}**")
    lines.append(f"- الشركات الرائدة: {', '.join(key_findings['leaders'])}")
    lines.append(f"- شركات غير نشطة: {', '.join(key_findings['inactive'])}")
    lines.append(f"- **الفرصة الذهبية:** {key_findings['opportunity']}")
    lines.append("")
    lines.append("### الفجوات في المحتوى عبر السوق كله:")
    for gap in key_findings["content_gap"]:
        lines.append(f"  - {gap}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Scoring Table
    lines.append("## جدول المقارنة الشامل (10 شركات × 10 أبعاد)")
    lines.append("")
    lines.append("| # | الشركة | المدينة | المتابعون | تكرار النشر | التحقق | الرؤية العامة | قوة البايو | معلومات التواصل | نوع المحتوى | النقاط /100 |")
    lines.append("|---|--------|---------|-----------|-------------|--------|----------------|-----------|-----------------|-------------|------------|")

    scored = []
    for c in competitors:
        s = score_page(c)
        scored.append((s, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    for i, (score, c) in enumerate(scored, 1):
        name = c["name_ar"] or c["name"]
        city = c["location"].split(",")[0] if c["location"] else "—"
        followers = fmt_followers(c.get("followers", "?"))
        freq = c.get("post_frequency", "غير معروف")
        if "Daily" in freq: freq_display = "يومي ✅"
        elif "Weekly" in freq: freq_display = "أسبوعي 🔶"
        elif "Unknown" in str(freq): freq_display = "غير معروف ❓"
        else: freq_display = freq
        verified = "✅" if c.get("verified") else "❌"
        visible = "✅ عام" if c.get("posts_visible_without_login") else "🔒 مقفل"
        has_bio = "قوي ✅" if (len(str(c.get("bio_ar") or "")) + len(str(c.get("bio_en") or ""))) > 100 else "ضعيف ❌"
        has_contact = "✅" if c.get("phone") or c.get("email") else "❌"
        content_types = ", ".join(c.get("content_types", ["غير معروف"])[:2])
        lines.append(f"| {i} | {name} | {city} | {followers} | {freq_display} | {verified} | {visible} | {has_bio} | {has_contact} | {content_types} | **{score}** |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed Analysis Per Company
    lines.append("## التحليل التفصيلي لكل شركة")
    lines.append("")

    for score, c in scored:
        lines.append(f"### {c['name_ar'] or c['name']} | {c['name']}")
        lines.append(f"**الرابط:** {c['facebook_url']}")
        lines.append(f"**النقاط:** {score}/100")
        lines.append("")
        lines.append(f"| المعيار | البيانات |")
        lines.append(f"|---------|----------|")
        lines.append(f"| الموقع | {c.get('location', '—')} |")
        lines.append(f"| التصنيف | {c.get('category', '—')} |")
        lines.append(f"| المتابعون | {fmt_followers(c.get('followers', '?'))} |")
        lines.append(f"| تكرار النشر | {c.get('post_frequency', 'غير معروف')} |")
        lines.append(f"| آخر منشور | {c.get('last_post', '—')} |")
        lines.append(f"| اللغة | {c.get('language', '—')} |")
        lines.append(f"| جودة البايو | {c.get('about_quality', '—')} |")
        bio = c.get("bio_ar") or c.get("bio_en") or "—"
        lines.append(f"| البايو | {str(bio)[:120]}... |" if len(str(bio)) > 120 else f"| البايو | {bio} |")
        lines.append(f"| الموقع الإلكتروني | {c.get('website', '—')} |")
        lines.append(f"| البريد | {c.get('email', '—')} |")
        lines.append(f"| الهاتف | {c.get('phone', '—')} |")
        lines.append("")

        lines.append("**الخدمات:**")
        for svc in c.get("services", []):
            lines.append(f"  - {svc}")
        lines.append("")

        lines.append("**نقاط القوة:**")
        for s in c.get("strengths", []):
            lines.append(f"  - ✅ {s}")
        lines.append("")

        lines.append("**نقاط الضعف:**")
        for w in c.get("weaknesses", []):
            lines.append(f"  - ❌ {w}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Gap Analysis
    lines.append("## تحليل الفجوات والفرص لأزكى")
    lines.append("")
    lines.append("### 1. الفجوة الأكبر: ضعف الحضور الرقمي في القطاع")
    lines.append("")
    lines.append("| المنافس | المتابعون | نشاط الصفحة |")
    lines.append("|---------|-----------|-------------|")

    for _, c in scored:
        name = c["name_ar"] or c["name"]
        f = fmt_followers(c.get("followers", "؟"))
        freq = c.get("post_frequency", "غير معروف")
        if "Daily" in freq: active = "🔥 نشط جداً"
        elif "Weekly" in freq: active = "✅ نشط"
        elif "Unknown" in str(freq): active = "❓ غير معروف"
        else: active = "💤 غير نشط"
        lines.append(f"| {name} | {f} | {active} |")

    lines.append("")
    lines.append("**خلاصة:** الشركة الرائدة (أولتيميت سوليوشنز) لديها 40K متابع فقط - وهذا رقم ضعيف مقارنة بالحجم الكبير لسوق IT السعودي. أزكى يمكنها اختراق السوق والوصول إلى مكانة بارزة خلال 6-12 شهراً.")
    lines.append("")
    lines.append("### 2. فجوة المحتوى الحكومي والمؤسسي")
    lines.append("")
    lines.append("**لا توجد شركة** في القائمة تنشر:")
    lines.append("- قصص نجاح مع الجهات الحكومية")
    lines.append("- محتوى تعليمي عن أنظمة الموارد البشرية الحكومية")
    lines.append("- شراكات مع IBM/Microsoft (أزكى لديها هذه الميزة)")
    lines.append("- إنجازات ومشاريع ملموسة (أزكى 77+ مشروع)")
    lines.append("")
    lines.append("### 3. فجوة التوثيق والمصداقية")
    lines.append("")
    lines.append("**من بين 10 شركات، شركة واحدة فقط لديها علامة التحقق (Verified)** - وهي أولتيميت سوليوشنز.")
    lines.append("أزكى يجب أن تسعى للحصول على التحقق فور إنشاء الصفحة.")
    lines.append("")
    lines.append("### 4. فجوة اللغة العربية")
    lines.append("")
    lines.append("معظم الشركات تستخدم الإنجليزية أو مزيجاً - المحتوى العربي الاحترافي هو فرصة واضحة.")
    lines.append("")
    lines.append("### 5. فجوة التواصل مع رؤية 2030")
    lines.append("")
    lines.append("لا توجد شركة تربط خدماتها بشكل مباشر وواضح برؤية 2030 في محتواها الاجتماعي.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Strategic Recommendations
    lines.append("## التوصيات الاستراتيجية لأزكى")
    lines.append("")
    lines.append("### الموقع الاستراتيجي المقترح:")
    lines.append("> **'أزكى - شريكك في التحول الرقمي الحكومي والمؤسسي منذ 35 عاماً'**")
    lines.append("")
    lines.append("### أولويات الصفحة:")
    lines.append("1. **إنشاء صفحة احترافية** مع About شامل (عربي + إنجليزي)")
    lines.append("2. **النشر يومياً** - هذا هو المعيار للمنافسة مع أولتيميت")
    lines.append("3. **محتوى حكومي متخصص** - هذه الفجوة التنافسية الأكبر")
    lines.append("4. **قصص نجاح** - 77+ مشروع = 77+ قصة محتوى")
    lines.append("5. **التحقق من الصفحة** - ميزة فورية على 9 من 10 منافسين")
    lines.append("6. **تسليط الضوء على شراكات IBM وMicrosoft**")
    lines.append("7. **محتوى تعليمي** عن أنظمة HR والأمن والأرشفة")
    lines.append("8. **ربط بالمناسبات السعودية** (اليوم الوطني، رؤية 2030)")
    lines.append("")

    return "\n".join(lines)


def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
    print("Loading competitor data...")
    data = load_data()
    print(f"Loaded {len(data['competitors'])} competitors")

    print("Generating comparison report...")
    report = generate_report(data)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved to: {OUTPUT_FILE}")
    print(f"Report size: {len(report)} chars")


if __name__ == "__main__":
    main()
