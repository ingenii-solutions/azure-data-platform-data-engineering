.PHONY: build \
clean-all clean-lint clean-package clean-setup clean-tests clean-qa \
lint lint-convert \
test setup qa

-include .env

# Package

build-package:
	python setup.py bdist_wheel

clean-all:
	make clean-lint
	make clean-package
	make clean-tests

clean-qa:
	make clean-lint
	make clean-tests

clean-package:
	@rm -rf ./build ./dist ./*.egg-info ./.eggs

clean-lint:
	@rm -rf ./flake8_report.txt ./flake8_report_junit.xml

clean-setup:
	@rm .env

clean-tests:
	@rm -rf ./.pytest_cache **/__pycache__ ./pytest_report_junit.xml

lint:
	make clean-lint
	flake8 --tee --output-file flake8_report.txt

lint-convert:
	flake8_junit flake8_report.txt flake8_report_junit.xml

test:
	make clean-tests
	pytest ./tests --junitxml=pytest_report_junit.xml

qa:
	make lint
	make test
