# Gunakan image Python resmi sebagai base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Buat direktori untuk source code app
WORKDIR /app

# Install dependencies system
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv dan dependencies proyek
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Salin source code proyek
COPY . /app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Expose port untuk Django
EXPOSE 8000

# Jalankan entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
