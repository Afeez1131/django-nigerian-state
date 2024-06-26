#!/bin/bash

# Remove the existing distribution directory
echo "Removing existing distribution directory..."
rm -rf dist/

# clean bdist wheel
echo "cleaning build directory"
python setup.py clean --all bdist_wheel


# Build the source distribution
echo "Building the source distribution..."
python setup.py sdist

# Build the wheel distribution
echo "Building the wheel distribution..."
python setup.py bdist_wheel

# Upload distributions to TestPyPI
echo "Uploading distributions to TestPyPI..."
# python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*

# Clean up
echo "Cleaning up temporary files..."
rm -rf build/  # Remove build directory
rm -rf *.egg-info/  # Remove egg-info directory
