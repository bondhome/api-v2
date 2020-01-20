# Bond Api (2.0)

Documentation for backend and firmware api.
You need docker to build/run/bundle the documentation

## Build image

```
make build
```

## Run cloud or local documentation

### Cloud

```
make build
make run_cloud
```

### Local

```
make build
make run_local
```

## Bundle cloud or local documentation

### Cloud

```
make build
make bundle_cloud
```

### Private

```
make build
make bundle_local
```

## Tests

This command should be running with python3 and pyyaml instaled


```
make test
```


## Read documentation

Open browser at [localhost:8000](http://localhost:8000).

## Specification

- [OpenAPI](https://github.com/OAI/OpenAPI-Specification)
- [Swagger](https://swagger.io/docs/specification/about/)
- [API Handyman](https://apihandyman.io/the-story-behind-the-design-of-everyday-apis-book/)
