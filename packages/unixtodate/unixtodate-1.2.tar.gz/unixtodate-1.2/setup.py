from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="unixtodate",
    version="1.2",
    author="Network King",
    author_email="5giziuoq@duck.com",
    description="A package to convert timestamp to days",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Gegenwehr/unixtodate",
    packages=['unixtodate'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)