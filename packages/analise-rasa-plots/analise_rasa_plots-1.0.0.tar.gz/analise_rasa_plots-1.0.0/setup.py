from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="analise_rasa_plots",
    version="1.0.0",
    author="AlcimarMT",
    author_email="alcimartri1998@gmail.com",
    description="create boring and fast plots",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)