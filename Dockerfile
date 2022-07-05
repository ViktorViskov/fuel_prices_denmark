# maintainer info
FROM debian:latest
LABEL maintainer="carrergt@gmail.com"

# config container
RUN apt update
RUN apt install python3 python3-pip ssocr -y
RUN pip3 install fastapi uvicorn jinja2 bs4 requests pillow

# config project
WORKDIR /app
COPY ./ ./
CMD ["sh","./prod_start.sh"]
EXPOSE 9011
