from alpine:3.6

MAINTAINER Michael Spector <michael@viyadb.com>
LABEL Description="Mobile users activity events simulator"

ADD repositories /etc/apk/repositories
RUN apk add --no-cache --update \
      python2 \
      py2-pip \
      py2-numpy@community
RUN pip install simpy pytz

ADD tarball.tgz /opt

WORKDIR "/opt/events-generator"
CMD ["/opt/events-generator/generate.py"]

