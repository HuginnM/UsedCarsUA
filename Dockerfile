FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/app'

COPY . .

EXPOSE 8000
CMD ["python", "./app.py"]