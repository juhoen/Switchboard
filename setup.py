# pylint: disable=all
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-switchboard",
    version="0.0.1",
    author="Juho Enala",
    author_email="juho.enala@gmail.com",
    description="A lightweight package for converting JSON schemas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juhoen/Switchboard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
