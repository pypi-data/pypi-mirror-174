from setuptools import setup

version = "0.1.0"

with open("./README.md") as file:
    readme = file.read()

setup(
    name="kimbo",
    author="NiumXp",
    url="https://github.com/NiumXp/kimbo",
    version=version,
    packages=["kimbo"],
    include_package_data=True,
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ]
)
