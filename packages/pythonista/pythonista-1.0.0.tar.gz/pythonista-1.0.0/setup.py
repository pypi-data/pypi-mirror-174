from setuptools import setup, find_packages

setup(
    name="pythonista",
    description="A shortcut command for Python",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    version="1.0.0",
    url="https://github.com/cj-praveen/pythonista/",
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        py=python:cli
    """
)
