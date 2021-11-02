FROM python:3.8

RUN groupadd -r runner && useradd --no-log-init -r -g runner runner

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workdir
USER runner:runner
COPY --chown=runner:runner . .
