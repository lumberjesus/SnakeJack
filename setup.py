from setuptools import setup, find_packages

setup(
    name="snakejack",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask>=2.0.0",
        "flask-session>=0.5.0",
    ],
    python_requires=">=3.7",
    author="Ben",
    description="A Python implementation of BlackJack (converted from C# SharpJack)",
    include_package_data=True,
    package_data={
        "snakejack.web": [
            "templates/*.html",
            "static/*.*",
            "static/**/*.*"
        ]
    },
)