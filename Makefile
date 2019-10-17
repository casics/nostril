install-release-tools:
	pip install --user twine

release-pypi-test:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release-pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine check dist/*
	twine upload dist/*