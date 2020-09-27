import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RSA",
    version="1.0.0",
    author="WOJCIECH TRZUPEK",
    description="Package contains algorithms for Random Sequential Adsorption simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WTrzupek/RSA",
    py_modules = ["naive, improved, precise"],
    packages = ['RSA'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
