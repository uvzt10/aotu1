# استخدام نسخة بايثون خفيفة
FROM python:3.9-slim

# تنصيب أدوات النظام الضرورية للفيديو
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# تعديل صلاحيات ImageMagick للسماح بالكتابة على الفيديو (خطوة ضرورية جداً في اللينكس)
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml

# إعداد مجلد العمل
WORKDIR /app

# نسخ الملفات وتنصيب المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# فتح المنفذ وتشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
