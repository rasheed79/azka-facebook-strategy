# مشروع: استراتيجية صفحة فيسبوك - أزكى لتقنية المعلومات

**تاريخ الإنشاء:** 2026-04-05  
**الحالة:** مكتمل - جاهز للتنفيذ

---

## نظرة عامة

مشروع متكامل لإنشاء صفحة فيسبوك احترافية لشركة أزكى لتقنية المعلومات (جدة - السعودية)، مبني على تحليل عميق لـ 10 منافسين في السوق السعودي.

---

## GitHub

المستودع العام: **[github.com/rasheed79/azka-facebook-strategy](https://github.com/rasheed79/azka-facebook-strategy)**

- الفرع الوحيد للنشر: **`main`**
- **`index.html`** في **جذر** المستودع = نسخة التقرير التي يفتحها Vercel على `/` (لا تضع المشروع داخل مجلد فرعي كجذر).

---

## تقرير HTML

| الملف | الوصف |
|--------|--------|
| **`reports/azka_facebook_report.html`** | المصدر عند التعديل |
| **`index.html`** (جذر المشروع) | نسخة مطابقة للنشر على Vercel |

بعد تعديل التقرير:

```powershell
.\execution\sync_index_html.ps1
git add -A && git commit -m "تحديث التقرير" && git push origin main
```

---

## ربط Vercel بـ GitHub (خطوات على لوحة Vercel)

افتح المشروع: **[vercel.com/rasheed79s-projects/azka-facebook-strategy](https://vercel.com/rasheed79s-projects/azka-facebook-strategy)**

إذا ظهر **Connect Git Repository** أو لم يكن المستودع مربوطاً:

1. **Settings** (إعدادات المشروع) → **Git**
2. **Connect Git Repository** → اختر **GitHub** واسمح لـ Vercel بالوصول إن طُلب ذلك
3. اختر المستودع **`rasheed79/azka-facebook-strategy`** والفرع **`main`**
4. **Settings** → **General** → تحقق من:
   - **Root Directory:** فارغ (لا تكتب `reports`)
   - **Framework Preset:** **Other**
   - **Build Command:** فارغ
   - **Output Directory:** فارغ
   - **Install Command:** فارغ
5. **Save** ثم من **Deployments** اضغط **⋯** على آخر نشر → **Redeploy** (أو ادفع commit جديد من جهازك ليُنشَر تلقائياً)

### روابط بعد الربط

- `https://azka-facebook-strategy.vercel.app/`
- `https://azka-facebook-strategy.vercel.app/reports/azka_facebook_report.html`

**محلياً:** افتح `index.html` أو `reports/azka_facebook_report.html` في المتصفح.

---

## هيكل المشروع

```
azka-facebook-strategy/
│
├── README.md
├── index.html                         ← نسخة التقرير للجذر (Vercel يفتحها على /)
│
├── directives/
│   └── facebook_competitor_analysis.md   ← الـ SOP والدروس المستفادة
│
├── execution/
│   ├── sync_index_html.ps1            ← نسخ التقرير إلى index.html للنشر
│   ├── generate_facebook_report.py    ← سكريبت توليد تقرير المقارنة
│   └── generate_azka_content.py       ← سكريبت توليد استراتيجية المحتوى
│
└── reports/
    ├── azka_facebook_report.html      ← ⭐ تقرير HTML الشامل (افتحه في المتصفح)
    ├── competitors_raw.json           ← بيانات المنافسين الخام (JSON)
    ├── competitor_comparison.md       ← تقرير المقارنة التفصيلي
    └── azka_facebook_content.md       ← استراتيجية المحتوى الكاملة ⭐
```

---

## الملفات الرئيسية

### ⭐ `reports/azka_facebook_content.md`
**الأهم** — الاستراتيجية الكاملة لصفحة فيسبوك أزكى تشمل:
- إعداد الصفحة (الاسم، Username، About بعربي وإنجليزي)
- الهوية البصرية (الألوان، الخطوط، أسلوب الصور)
- 30 منشور جاهز للنشر مع النص والهاشتاقات والتوقيت
- تقويم محتوى شهري
- استراتيجية النمو والإعلانات

### `reports/competitor_comparison.md`
تقرير مفصل لـ 10 شركات سعودية منافسة يشمل:
- جدول مقارنة شامل بنقاط لكل شركة
- تحليل نقاط القوة والضعف
- الفجوات في السوق التي تستطيع أزكى ملأها

### `reports/competitors_raw.json`
البيانات الخام للمنافسين - مفيد لإعادة التوليد أو التحديث لاحقاً.

---

## الخطوات التالية (للإكمال لاحقاً)

- [ ] إنشاء صفحة الفيسبوك باستخدام المعلومات في `azka_facebook_content.md`
- [ ] رفع صورة الغلاف وصورة الملف الشخصي
- [ ] نشر المنشورات الـ 30 وفق التقويم المقترح
- [ ] متابعة النمو وتحديث الاستراتيجية بعد شهر
- [ ] الحصول على توثيق الصفحة (علامة التحقق الزرقاء)

---

## كيفية إعادة تشغيل السكريبتات

```powershell
# من داخل مجلد المشروع
cd c:\work\Cursor\azka-facebook-strategy

# إعادة توليد تقرير المقارنة
python execution/generate_facebook_report.py

# إعادة توليد استراتيجية المحتوى
python execution/generate_azka_content.py
```

> ملاحظة: السكريبتات تقرأ من `reports/competitors_raw.json` وتكتب في `reports/`

---

## المصادر

- موقع أزكى: http://www.azka.com
- تحليل 10 صفحات فيسبوك لشركات IT سعودية (بيانات 2026-04-05)
