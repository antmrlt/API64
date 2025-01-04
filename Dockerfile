FROM python:3.9-slim
# Set environment variables for Python
ENV PYTHONUNBUFFERED 1 :
# Set the working directory inside the container
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 5000
CMD ["python", "app.py"]