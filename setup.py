import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tauros-api",
    version="0.0.1",
    author="Altcoins Mex S.A.P.I. de C.V.",
    author_email="contacto@tauros.io",
    description="This module is for connection with Tauros API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coinbtr/tauros-api-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
