FROM python:3.11-slim AS builder

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --prefix=/install -r requirements.txt


FROM python:3.11-slim

ENV TZ=UTC

RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app /app/app
COPY scripts /app/scripts
COPY cron /app/cron

COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem
COPY instructor_public.pem /app/instructor_public.pem

RUN mkdir -p /data /cron && chmod 755 /data /cron

RUN crontab /app/cron/2fa-cron

EXPOSE 8080

CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
