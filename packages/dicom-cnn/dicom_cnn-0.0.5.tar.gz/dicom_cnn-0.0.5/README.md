# dicom_cnn

## Release Procedure

https://packaging.python.org/en/latest/flow/

- Upgrade version in setup.py  
- pipenv run python setup.py sdist  
- pipenv run python setup.py bdist_wheel  
- pipenv run twine upload --config-file .pypirc dist/*  

## Install dependencies
pipenv install [dep]

## Generate requirements
pipenv requirements > requirements.txt