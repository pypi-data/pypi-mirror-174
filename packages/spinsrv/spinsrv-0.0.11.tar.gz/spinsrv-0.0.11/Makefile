build:
	python3 -m build
deploy:
	python3 -m twine upload dist/*
install:
	pip install -e .
fmt:
	python -m black .
types:
	mypy src
test: # these need a citizen account (currently proteins and they do modify it)
	python tests/smoke_test.py
	python tests/smoke_test2.py
	python tests/smoke_test3.py
freeze:
	pip freeze > requirements.txt
