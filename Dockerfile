# maintainer info
FROM debian:latest
LABEL maintainer="carrergt@gmail.com"

# config container
RUN ln -sf /usr/share/zoneinfo/Europe/Copenhagen /etc/localtime
RUN apt update
RUN apt install python3 python3-pip ssocr -y --no-install-recommends --no-install-suggests
RUN pip3 install fastapi uvicorn jinja2 bs4 requests pillow

# config project
WORKDIR /app
COPY ./ ./
CMD ["sh","./prod_start.sh"]
EXPOSE 9011
