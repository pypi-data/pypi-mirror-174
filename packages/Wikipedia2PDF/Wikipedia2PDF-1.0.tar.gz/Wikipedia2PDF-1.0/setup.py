from setuptools import setup, find_packages

setup(
    name="Wikipedia2PDF",
    description="Convert any Wikipedia article into PDF.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    version="1.0",
    license="MIT",
    url="https://github.com/cj-praveen/Wikipedia2PDF/",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=["requests", "bs4", "reportlab"]
)
