from setuptools import setup, find_packages
from mangadex_dl.cli import VERSION

with open("README.md") as f:
    long_description = f.read()

setup(
    name="mangadex_dl",
    version=VERSION,
    python_requires=">=3.10",
    install_requires=['mangadex==2.5.2', 'Pillow==9.4.0',
                      'PyPDF2==3.0.1', 'requests==2.28.2'],
    author="John Erinjery",
    author_email="jancyvinod415@gmail.com",
    packages=['mangadex_dl'],
    include_package_data=True,
    url="https://github.com/john-erinjery/mangadex-dl/",
    license="MIT",
    description="A Python CLI that downloads manga from mangadex.org as image or PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "mangadex_dl=mangadex_dl.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
