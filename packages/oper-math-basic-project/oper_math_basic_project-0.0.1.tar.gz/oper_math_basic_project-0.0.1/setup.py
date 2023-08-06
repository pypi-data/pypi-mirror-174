from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open ("requisitos.txt") as f:
    requisitos= f.read().splitlines()

setup(
    name="oper_math_basic_project",
    version="0.0.1",
    author="Sabuat Urbina Ribeiro",
    author_email="sabuaturbina@yahoo.com",
    description="A pacage with two basic math operations",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sabuat/package-operaciones.git",
    install_requires=requisitos,
    python_requires=">=3.8",
)