FROM nextcloud:apache

RUN apt-get update && apt-get install wget && apt-get clean
RUN wget https://github.com/nextcloud/groupfolders/releases/download/v2.0.2/groupfolders-2.0.2.tar.gz -P /tmp \
    && tar xf /tmp/groupfolders-2.0.2.tar.gz -C /tmp/ \
    && rm /tmp/groupfolders-2.0.2.tar.gz
