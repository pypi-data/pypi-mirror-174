import setuptools

from apkcat import __version__

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apkcat",  # Replace with your own username
    version=__version__,
    author="JunWei Song",
    author_email="sungboss2004@gmail.com",
    description="apkcat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apkcat/apkcat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    entry_points={
        "console_scripts": [
            "ac=apkcat.cli.cli:entry_point",
        ]
    },
    python_requires=">=3.8",
    install_requires=[
        "prettytable",
        "androguard==3.4.0a1",
        "click",
    ],
)
