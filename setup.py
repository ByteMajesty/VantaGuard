import os
from setuptools import setup, find_packages

setup(
    name="vantaguard",
    version="1.0.2",
    author="ByteMajesty",
    description="Real-time IDS and Security Auditor for Linux",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/ByteMajesty/VantaGuard",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "vantaguard=vantaguard.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
)
