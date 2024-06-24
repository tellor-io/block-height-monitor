from setuptools import find_packages
from setuptools import setup


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name="block-height-monitor",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": ["monitor=block_height_monitor.check_node:__main__"],
    },
)
