from alpine:edge

MAINTAINER Michael Spector <michael@viyadb.com>
LABEL Description="Mobile users activity events simulator"

ADD repositories /etc/apk/repositories

RUN apk add --no-cache --update \
      python3 \
      py3-pip \
      py3-scipy \
      py3-numpy \
    && pip3 --no-cache-dir install \
      simpy \
      pytz

ADD tarball.tgz /opt

WORKDIR "/opt/events-generator"
CMD ["/usr/bin/python3", "/opt/events-generator/generate.py"]

