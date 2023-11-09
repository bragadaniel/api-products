FROM python:3.9.2-slim

WORKDIR /api-products

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "--app", "src/main", "run", "--port=8000"]
