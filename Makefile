default: docker_build

docker_build:
	@docker build --tag=chariot:dev .

docker_run:
	@docker run --env-file .env -e PORT=8000 -p 8000:8000 chariot:dev 

