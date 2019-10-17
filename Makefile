install-release-tools:
	pip install --user twine

release:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine check dist/*
	twine upload dist/*