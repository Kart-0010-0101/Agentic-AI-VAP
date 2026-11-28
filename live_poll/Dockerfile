FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir "qrcode[pil]>=8.0"
COPY . /app/
ENV PYTHONUNBUFFERED=1
EXPOSE 8765
CMD ["python", "poll_server.py"]
