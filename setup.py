import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wisp-icave",
    version="0.0.1",
    author="Ian Cave",
    description="NBA draft predictions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
)
