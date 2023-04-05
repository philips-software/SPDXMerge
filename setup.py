import os

from setuptools import find_packages, setup

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(requirements_path, "r", encoding="utf8") as f:
    required = f.read().splitlines()

setup(
    name='spdxmerge',
    version='0.1.0',
    description="merges content of two/more spdx sboms",
    long_description_content_type="text/markdown",
    url="https://github.com/philips-software/SPDXMerge",
    packages=find_packages(include=['src'], exclude=['test', '*.test', '*.test.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.10.9'
)
