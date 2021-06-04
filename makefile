test: test-lint test-unit test-integration

test-lint:
# stop the build if there are Python syntax errors or undefined names
	@echo "***** Running flake8 syntax  *****"
	flake8 azspec --count --select=E9,F63,F7,F82 --show-source --statistics
	
# exit-zero treats all errors as warnings.
	@echo "***** Running flake8 warning *****"
	flake8 azspec --count --exit-zero --ignore=F405 --max-complexity=10 --max-line-length=200 --statistics --exclude *_test.py  

# pylint
	@echo "***** Running pylint *****"
	pylint --ignore-patterns=".*_test.py" azspec

test-unit:
	# python3 -m unittest discover -s azext_cdf -p '*_test.py' -v
	pytest -v azext_cdf --color=yes --code-highlight=yes

# test-integration:
# 	pytest -v tests --color=yes --code-highlight=yes -s
# 	@echo "running expect default test"
# 	az cdf test -w ./tests/fixtures/bicep/v2 --down-strategy=always default

clean:
	rm -rf build
	rm -rf dist/
	rm -rf pytest_cache/
	rm -rf *.egg-info

clean-all: clean
	rm -rf $(VENV)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	   
.PHONY: all source-venv
