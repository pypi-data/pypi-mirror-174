from setuptools import setup, find_packages


setup(
    name             = "sg-pkg",
    version          = "0.0.0",
    description      = "This is a package",
    packages         = find_packages("src"),
    package_dir      = {"":"src"},
    author           = "",
    author_email     = "",
    licence          = "",
    install_requires = "",   
)