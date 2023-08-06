from setuptools import find_packages, setup

with open("./README.md", "r") as fh:
    long_description = fh.read()


with open("./VERSION") as f:
    version = f.read().strip()


with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()


setup(
    install_requires=[req for req in requirements if req[:2] != "# "],
    name="shroomdk",
    version=version,
    author="dev@flipsidecrypto.com",
    author_email="dev@flipsidecrypto.com",
    description="ShroomDK (SDK) by Flipside Crypto: Query the most comprehensive blockchain data in crypto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlipsideCrypto/sdk/python",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    dependency_links=[],
    python_requires=">=3.7",
)
