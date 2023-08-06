import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepdriver",
    version="0.0.8",
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
    packages=["deepdriver","deepdriver.sdk","deepdriver.sdk.chart","deepdriver.sdk.data_types","deepdriver.sdk.interface"],
    python_requires=">=3.6"
)