install-prod:
	@pip install -r services/app/requirements.txt

install-dev:
	pip install -r services/app/requirements-dev.txt

gunicorn:
	@cd services/app && gunicorn -b 0.0.0.0:5000 manage:app

initial-tag:
	@git tag -a -m "initial tag" v0.1.0

pre-commit:
	@pre-commit install

initial-tag:
	@git tag -a -m "Initial tag." v0.0.1

init-cz:
	@cz init

bump-tag:
	@cz bump --check-consistency --changelog

lint:
	@black --line-length 120 services/app
	@isort services/app
	@flake8
	# @pydocstyle  services/app/api
	# @pylint --rcfile=.pylintrc ./services/app/api

install-youtube:
	@pip uninstall youtube -y
	@pip install /home/lyle/professional-projects/youtube-wrapper/dist/youtube-0.0.1-py3-none-any.whl

build-dev:
	@docker build -f ./services/app/Dockerfile -t youtube-video-stats-dev:latest ./services/app

run-dev:
	@docker run -p5000:5000 --env-file=./services/app/.env youtube-video-stats-dev:latest

build-prod:
	@docker build -f ./services/app/Dockerfile.prod -t youtube-video-stats-prod:latest ./services/app

run-prod:
	@docker run -p5000:5000 --env-file=./services/app/.env youtube-video-stats-prod:latest

# build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump
