from setuptools import setup
from setuptools import find_packages


setup(
    name="suunto_analyzer",
    version="0.3",
    author="Alessio Sclocco",
    author_email="alessio@sclocco.eu",
    description="Simple tool to analyze activities recorded with Suunto watches",
    license="Apache 2.0",
    keywords="suunto",
    url="https://github.com/isazi/SuuntoAnalyzer",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["matplotlib>=3.4", "numpy>=1.22"],
    extras_require={
        "fit": ["fitdecode>=0.10"],
        "map": ["contextily>=1.2"],
        "dev": ["pytest>=7", "fitdecode>=0.10"],
    },
)
