from setuptools import setup, find_packages

setup(
    name="planetoids-game",
    version="0.2.0",
    author="Chris Greening",
    author_email="chris@christophergreening.com",
    description="A retro-style space shooter game built with Pygame.",
    long_description=open("README.md", encoding="utf-8").read(),  # ✅ Specify encoding
    long_description_content_type="text/markdown",
    url="https://github.com/chris-greening/planetoids",
    packages=find_packages(),
    include_package_data=True,
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
