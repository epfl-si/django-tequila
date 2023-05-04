FROM python:3.8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 \
        telnet \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/django_tequila_app
COPY django_tequila_app django_tequila_app
COPY manage.py manage.py

RUN pip install -r django_tequila_app/requirements/base.txt

EXPOSE 443 4445
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:443"]
