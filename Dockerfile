FROM python:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /usr/src/app
COPY ./sample_app/requirements/*.txt sample_app/requirements/
RUN pip install -r sample_app/requirements/development.txt
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000"]
