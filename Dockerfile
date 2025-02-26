FROM cimg/node:21.1.0

RUN npm install redoc && npm install -g redoc-cli

WORKDIR /code

COPY . /code

CMD ["redoc-cli", "bundle", "local.yaml", "-o=docs.html"]
