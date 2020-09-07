FROM python:3.8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 \
        telnet \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./sample_app/requirements/*.txt sample_app/requirements/
RUN pip install -r sample_app/requirements/base.txt
COPY . .

EXPOSE 443 4445
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:443"]
