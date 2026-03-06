FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Dependencias para MySQL y ReportLab/Pillow
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Recopilar estáticos para que Nginx los pueda ver después
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Apuntamos a proveedor.wsgi que es donde está tu config
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "proveedor.wsgi:application"]