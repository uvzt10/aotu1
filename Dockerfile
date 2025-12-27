# استخدام نسخة بايثون خفيفة
FROM python:3.9-slim

# تنصيب أدوات النظام الضرورية للفيديو
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    ghostscript \
    findutils \
    && rm -rf /var/lib/apt/lists/*

# === الخطوة المصححة ===
# بدلاً من تحديد المسار يدوياً، نستخدم الأمر find للبحث عن ملف policy.xml وتعديله أينما كان
RUN find /etc -name "policy.xml" -exec sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' {} +

# إعداد مجلد العمل
WORKDIR /app

# نسخ الملفات وتنصيب المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# فتح المنفذ وتشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
