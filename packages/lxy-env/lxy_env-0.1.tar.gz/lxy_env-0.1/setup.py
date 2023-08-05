import setuptools
from pathlib import Path

setuptools.setup(
    name='lxy_env',
    version='0.01',
    description='A OpenAI Gym Env for lxy',
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="lxy_env"),
    install_requires=['gym']


)