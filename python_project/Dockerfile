FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "run.py"]
