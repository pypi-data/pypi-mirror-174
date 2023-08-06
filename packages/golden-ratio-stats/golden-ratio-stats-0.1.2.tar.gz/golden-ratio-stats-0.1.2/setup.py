import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="golden-ratio-stats",
    version="0.1.2",
    author="Serhat Erdem",
    author_email="erdemserhat1994@gmail.com",
    description="Golden Ratio in Statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serhateerdem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    python_requires=">=3.9",
    install_requires=["numpy>=1.23.4", "pandas>=1.5.1"]
)