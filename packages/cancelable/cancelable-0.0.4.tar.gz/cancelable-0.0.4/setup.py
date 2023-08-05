from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.4"
DESCRIPTION = "A package that allows to cancel, certain functions that can be a pain, when working with threading."
long_description = (Path(__file__).parent / "README.md").read_text()

# Setting up
setup(
    name="cancelable",
    version=VERSION,
    author="jona799t",
    #author_email="<not@available.com>",
    url = "https://github.com/jona799t/Cancelable",
    description=DESCRIPTION,
    long_description=long_description,
    license_files = ("LICENSE.txt",),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "threading", "sleep", "cancelable", "input"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)