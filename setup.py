  
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.0.1"
setup(
    name="galaxy_environment",
    version=__version__,
    description="Measuring Galaxy Environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kayleigh Meneghini",
    author_email="kayleighmeneghini@gmail.com",
    url="https://github.com/kayleighm/galaxy-environment",
    packages=["galaxy_environment"],
    install_requires=[
        "numpy",
        "pandas",
        "math",
    ],
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
