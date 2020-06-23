import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-ThaaoBlues",
    version="0.0.2",
    author="Example Author",
    author_email="thaaoblues81@gmail.com",
    description="The easiest to configure python chat package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThaaoBlues/Lan_Chat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)