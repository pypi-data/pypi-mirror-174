import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mycore", # Replace with your own username
    version="0.0.3",
    author="Huan Zhou",
    author_email="shenarder@163.com",
    description="scn core lib by python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shenarder',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)