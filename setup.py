# standard libaries
import logging

# third party libraries
from setuptools import find_packages, setup

logger = logging.getLogger(__name__)

with open("README.md") as fp:
    readme_text = fp.read()

with open("LICENSE") as fp:
    license_text = fp.read()

with open("requirements/requirements.txt") as fp:
    requirements = [line.strip() for line in fp.readlines() if "--extra-index-url" not in line]

setup(
    name="finance_bot",
    version="0.1.0.dev0",
    url="https://github.com/enyquist/finance_bot",
    description="Finance Bot}}",
    long_description=readme_text,
    author="Erik Wyatt-Nyquist",
    author_email="enyquis1@jh.edu",
    license=license_text,
    python_requires="~=3.8",
    install_requires=requirements,
    packages=find_packages(exclude=("tests", "tests.*", "scripts")),
    entry_points={"console_scripts": ["finance_bot=finance_bot.cli:cli"]},
)
