FROM node:14-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

RUN npm install redoc && npm install -g redoc-cli

WORKDIR /code

COPY . /code

CMD ["redoc-cli", "bundle", "openapi.yaml", "-o=docs.html"]
