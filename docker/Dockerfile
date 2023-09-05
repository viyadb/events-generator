from alpine:edge

MAINTAINER Michael Spector <michael@viyadb.com>
LABEL Description="Mobile users activity events simulator"

ADD repositories /etc/apk/repositories

ENV PATH="/opt/venv/bin:$PATH"

RUN apk add --no-cache --update \
      python3 \
      py3-pip \
      py3-scipy \
      py3-numpy \
    && python3 -m venv --system-site-packages /opt/venv \
    && pip --no-cache-dir install \
      simpy \
      pytz \
      tqdm

ADD tarball.tgz /opt

WORKDIR "/opt/events-generator"
ENTRYPOINT ["python", "/opt/events-generator/generate.py"]

