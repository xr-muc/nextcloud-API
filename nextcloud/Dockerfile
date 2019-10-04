ARG NEXTCLOUD_VERSION

FROM nextcloud:$NEXTCLOUD_VERSION-apache

RUN true \
	&& apt-get update \
	&& apt-get install -y wget \
	&& apt-get clean \
	&& true

ARG GROUPFOLDERS_VERSION
RUN true \
	&& wget https://github.com/nextcloud/groupfolders/releases/download/v${GROUPFOLDERS_VERSION}/groupfolders-$GROUPFOLDERS_VERSION.tar.gz -P /tmp \
	&& tar xf /tmp/groupfolders-$GROUPFOLDERS_VERSION.tar.gz -C /tmp/ \
	&& rm /tmp/groupfolders-$GROUPFOLDERS_VERSION.tar.gz \
	&& true
