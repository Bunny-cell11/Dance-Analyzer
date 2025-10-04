FROM python:3.11-slim

WORKDIR /app

# In your Dockerfile

# This command installs a common set of required libraries for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libfontconfig1

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 600 -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
