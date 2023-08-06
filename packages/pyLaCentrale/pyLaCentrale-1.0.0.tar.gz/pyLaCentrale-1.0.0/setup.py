from setuptools import setup, find_packages
import pathlib
import setuptools

here = pathlib.Path(__file__).parent.resolve()

LONG_DESCRIPTION = (here / "README.md").read_text(encoding="utf-8")



VERSION = "1.0.0"
DESCRIPTION = "LaCentrale wrapper for python"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pyLaCentrale",
    version=VERSION,
    author="Quentin Petit",
    author_email="quentin.petit@isae-supmeca.fr",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=["requests","http.client","urllib","time","datetime"],
    keywords=["python", "LaCentrale api", "python lacentrale", "python car"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    url="https://github.com/QuentinPTT/lacentrale-api",
)
