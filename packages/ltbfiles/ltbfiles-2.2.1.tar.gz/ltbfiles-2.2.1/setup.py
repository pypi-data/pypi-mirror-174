from pathlib import Path
from setuptools import find_packages, setup

def get_readme():
    file = Path().resolve() / "README.md"
    with open(file, encoding="utf-8") as fid:
        return fid.read().strip()

setup(
    name="ltbfiles",
    author="Sven Merk",
    description="Module for loading of files created with spectrometers from LTB",
    long_description=get_readme(),
    packages=find_packages(),
    include_package_data=True,
    url="https://gitlab.com/ltb_berlin/ltb_files",
    install_requires=['numpy'],
    extras_require={
        'tests': ['pytest','pytest-cov','pandas'],
        'publish': ['twine','wheel'],
    }
)
