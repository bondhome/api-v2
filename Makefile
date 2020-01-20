build:
	docker build -t olibra.docs .

run_cloud:
	docker run --rm -v ${PWD}:/code -p 8080:8080 olibra.docs redoc-cli serve cloud.yaml -t template.hbs -w

run_local:
	docker run --rm -v ${PWD}:/code -p 8080:8080 olibra.docs redoc-cli serve local.yaml -t template.hbs -w

bundle_cloud:
	docker run --rm -v ${PWD}:/code -p 8080:8080 olibra.docs redoc-cli bundle cloud.yaml -t template.hbs

bundle_local:
	docker run --rm -v ${PWD}:/code -p 8080:8080 olibra.docs redoc-cli bundle local.yaml -t template.hbs

test:
	./ci/test.sh
