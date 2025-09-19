from setuptools import setup, find_packages

setup(
    name="snakejack",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.7",
    author="Ben",
    description="A Python implementation of BlackJack (converted from C# SharpJack)",
)