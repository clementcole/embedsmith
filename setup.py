from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="embedsmith",
    version="1.0.0",
    author="Clem Cole (ClemChowder)",
    author_email="embedded-project-creator@example.com",
    description="A tool to create standardized embedded project layouts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
                                "embedsmith=embedsmith.cli:main"
                            ],
    },
    include_package_data=True,
    package_data={
        "embeddedsmith": ["templates/*.j2"],
    },
    keywords="embedded, firmware, project, template, mcu, boilerplate, generator",
)