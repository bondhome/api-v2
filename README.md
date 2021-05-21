# Bond API V2

Source code to documentation for the Bond V2 API, used by Bond Bridge and Smart by Bond products. This is the _Local API_ used within the home Wi-Fi network.

To *read* the docs, please go here: http://docs-local.appbond.com/

## Contribuing

We welcome corrections and improvements to the API documentation. Please open a PR!

By submitting a PR, you are agreeing to have your contribution licensed under the same terms as the rest of the docs. See LICENSE file.

## Prerequisite

To be able to build and run this project, you need to have Docker and Node.js installed.
If you don't know if you have Docker and Node.js or don't know their versions, check it using
```
docker -v
node -v
```

* Docker can be installed from [their webiste](https://www.docker.com/products/docker-desktop).
* Node.js can be installed from [their website](https://nodejs.org/en/download/) or updated using `n` ([see instructions](https://nodejs.org/en/download/package-manager/#n))
  * The minimum Node.js required version is 14.

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
