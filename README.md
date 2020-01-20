# Bond API V2

Documentation for the Bond V2 API, used by Bond Bridge and Smart by Bond products. This is the _Local API_ used within the home Wi-Fi network.

## Contribuing

We welcome corrections and improvements to the API documentation. Please open a PR!

By submitting a PR, you are agreeing to have your contribution licensed under the same terms as the rest of the docs. See LICENSE file.

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
