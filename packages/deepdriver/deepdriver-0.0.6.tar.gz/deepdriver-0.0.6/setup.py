import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepdriver",
    version="0.0.6",
    author="bokchi",
    author_email="molamola.bokchi@gmail.com",
    description="deepdriver experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bokchi.com",
    project_urls={
        "bokchi git hub": "https://github.com/molabokchi",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src/module_python"},
    packages=setuptools.find_packages(where="src/module_python"),
    python_requires=">=3.6",
)