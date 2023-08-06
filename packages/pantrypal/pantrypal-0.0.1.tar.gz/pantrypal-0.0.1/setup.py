import codecs
import os.path
import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Define extra dependencies
dev_dep = [
    "black >= 22.10.0",
    "commitizen >= 2.35.0",
]
all_dep = dev_dep

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pantrypal",
    version=get_version("pantrypal/__init__.py"),
    author="Kieran Mackle",
    author_email="kemackle98@gmail.com",
    license="gpl-3.0",
    description="The Pantry Pal you've been waiting for.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/kieran-mackle/PantryPal/issues",
        "Source Code": "https://github.com/kieran-mackle/PantryPal",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    keywords=["recipes", "cooking", "shopping", "groceries"],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.7",
    install_requires=[
        "python-telegram-bot >= 13.14",
    ],
    extras_require={
        "dev": dev_dep,
        "all": all_dep,
    },
    setup_requires=[
        "setuptools_git",
        "setuptools_scm",
    ],
)
