FROM python:3.9-slim

WORKDIR usr/src/app

COPY ./requirements.txt ./usr/src/app/

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./usr/src/app/

CMD ["gunicorn", "restrofood.wsgi", "--bind", "127.0.0.0:8000"]
