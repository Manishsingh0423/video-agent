from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:

    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [
            req.split("#", 1)[0].strip()
            for req in requirements
        ]
        requirements = [req for req in requirements if req]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements


setup(
    name="video-agent",
    version="0.1.0",
    author="Manish singh",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
