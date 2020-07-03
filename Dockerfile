FROM alpine:3.7
RUN apk add python3 python3-dev postgresql-dev build-base git libc-dev linux-headers pcre pcre-dev bash postgresql-client && \
    mkdir /app && \
    git clone https://github.com/wheezymustafa/python-image-gallery.git /app && \
    pip3 install --upgrade pip setuptools && pip3 install -r /app/requirements.txt && \
    addgroup -S image_gallery && adduser -S -s /bin/bash -G image_gallery image_gallery && ln -s /bin/bash /usr/bin/bash && \
    chown -R image_gallery:image_gallery /app
    
USER image_gallery
WORKDIR /app
CMD ["uwsgi", "--http", ":5555", "--module", "gallery.ui.app:app", "--master", "--processes", "4", "--threads", "2"]
