import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lqs-client",
    version="0.0.9",
    author="Nathan Margaglio",
    author_email="nmargaglio@carnegierobotics.com",
    description="LogQS Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carnegierobotics/LogQS-Client",
    project_urls={
        "Bug Tracker": "https://github.com/carnegierobotics/LogQS-Client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["lqs_client", "lqs_client.interface"],
    python_requires=">=3.6",
    install_requires=[
        "fire==0.4.*",
        "python-dotenv==0.*",
        "requests==2.*",
        "xmltodict==0.13.*",
    ],
)
