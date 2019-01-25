#!/bin/sh

cd ..
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

echo "====================="
echo "To install run:"
echo "mkvirtualenv new-env-name"
echo "pip install --index-url https://test.pypi.org/simple/ swapi-gronka"

echo ""

echo "For test install run from this dir:"
echo "pip install -e ."
