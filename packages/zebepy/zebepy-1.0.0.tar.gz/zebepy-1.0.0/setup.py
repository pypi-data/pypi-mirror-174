import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Zebepy",
    version="1.0.0",
    author="vodkarm",
    author_email="vodkarm06@protonmail.com",
    description="The first Zebedee python API Wrapper !!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vodkarm/zebepy",
    project_urls={
        "Bug Tracker": "https://github.com/vodkarm/zebepy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)