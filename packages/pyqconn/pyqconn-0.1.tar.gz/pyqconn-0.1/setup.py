import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqconn",
    version="0.1",
    author="Eom Kyoungjun",
    author_email="kj@ekj.kr",
    description="to use various protocols and connections with same interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/adghk0/pyqconn",
    packages=['pyqconn'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)