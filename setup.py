from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brigitte-pkg-youszef",
    version="0.0.1",
    author="Youszef",
    description="A Card Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/youszef/brigitte-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)