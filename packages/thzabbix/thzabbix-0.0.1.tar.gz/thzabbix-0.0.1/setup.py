import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thzabbix",
    version="0.0.1",
    author="Volodymyr Borysiuk",
    author_email="thorvaldr.hrafn@gmail.com",
    description="Package for work with zabbix api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thorvaldhrafn/thzabbix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)