from setuptools import setup, find_packages
import os.path

# read the contents of the README file
from os import path

# this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
#     long_description = f.read()
#     # print(long_description)

# with open(os.path.join(this_directory, "VERSION")) as version_file:
#     __version__ = version_file.read().strip()

setup(
    name="presidio-evaluator",
    version="0.0.69",
    packages=find_packages(exclude=["tests"]),
    url="https://www.github.com/microsoft/presidio-research",
    license="MIT",
    description="PII dataset generator, model evaluator for Presidio and PII data in general",  # noqa
    package_data={
            "presidio_evaluator":
            [
                "data_generator/raw_data/*.csv",
                "data_generator/raw_data/*.yaml",
            ],
        },
    include_package_data=True,
    install_requires=[
        "presidio_analyzer",
        "presidio_anonymizer",
        "spacy>=3.0.0",
        "requests",
        "numpy",
        "pandas",
        "tqdm>=4.32.1",
        "jupyter>=1.0.0",
        "pytest>=4.6.2",
        "haikunator",
        "schwifty",
        "faker",
        "sklearn_crfsuite",
        "python-dotenv",
    ],
)
