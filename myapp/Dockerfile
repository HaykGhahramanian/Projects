FROM python:3.10-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /myapp

COPY *.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

