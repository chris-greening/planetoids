from setuptools import setup, find_packages

with open("planetoids/core/version.txt", "r") as f:
    version = f.read().strip()

setup(
    name="planetoids-game",
    version=version,
    author="Chris Greening",
    author_email="chris@christophergreening.com",
    description="A retro-style space shooter game built with Pygame.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chris-greening/planetoids",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "planetoids.core": ["version.txt"],  # 👈 Make sure version.txt is here
    },
    install_requires=[
        "pygame",
        "appdirs"
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "planetoids=planetoids.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ],
)
