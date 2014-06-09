from setuptools import setup, find_packages


setup(
    name="XFactory",
    description="Extractor function factory",
    version="0.1",
    author="Giles Brown",
    author_email="gilessbrown@gmail.com",
    include_package_data=True,
    packages=find_packages(exclude=('test',)),
)
