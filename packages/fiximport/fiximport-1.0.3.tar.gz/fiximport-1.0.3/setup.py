import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fiximport",
    author="Erik Lanning",
    author_email="cs@eriklanning.com",
    description="Fixes `ModuleNotFoundError` exceptions",
    keywords="ModuleNotFoundError, absolute import, fix imports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ELanning/fiximport",
    project_urls={
        "Documentation": "https://github.com/ELanning/fiximport",
        "Bug Reports": "https://github.com/ELanning/fiximport/issues",
        "Source Code": "https://github.com/ELanning/fiximport",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        "dev": ["check-manifest"],
    },
)
