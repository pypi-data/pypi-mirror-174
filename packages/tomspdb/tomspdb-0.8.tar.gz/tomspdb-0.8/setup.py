import setuptools
import os.path
import os

HERE = os.path.dirname(__file__) or "."

os.chdir(HERE)


def read(filename):
    with open(filename) as stream:
        return stream.read()


setuptools.setup(
    name="tomspdb",
    version="0.8",
    author="Talwrii",
    author_email="talwrii@gmail.com",
    url="https://github.com/talwrii/tomspdb",
    description="",
    license="MIT",
    keywords="debugger",
    modules=["tomspdb"],
    long_description=read(os.path.join(HERE, "readme.md")),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["tomspdb=tomspdb.tomspdb:main"]},
    classifiers=[],
)
