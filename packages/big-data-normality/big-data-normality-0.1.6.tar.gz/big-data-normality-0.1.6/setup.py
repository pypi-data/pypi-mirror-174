import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="big-data-normality",
    version="0.1.6",
    author="Serhat Erdem",
    author_email="erdemserhat1994@gmail.com",
    description="Normality Test for Big Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serhateerdem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    python_requires=">=3.9",
    install_requires=["numpy>=1.22.3", "pandas>=1.4.2", "scipy>=1.8.0", "statistics>=1.0.3.5"]
)