# -*- coding: utf-8 -*-
"""
Setup script for PyThaiNLP.

https://github.com/PyThaiNLP/pythainlp
"""
from setuptools import find_packages, setup


requirements = [
    "pandas",
]

extras = {
    "fetch":["requests"],
    "array":["numpy"]
}

readme = """
# Hello Python Package
"""
setup(
    name="mypackage-takipipo",
    version="0.0.1",
    description="Test Python Packaging",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="takipipo",
    author_email="ktphap.ncu@gmail.com",
    url="https://github.com/takipipo/explore-sentiment-analysis",
    packages=find_packages(exclude=["tests", "tests.*"]),
    test_suite="tests",
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require=extras,
    license="Apache Software License 2.0",
    zip_safe=False,
    # keywords=[
    #     "test-",
    #     "NLP",
    #     "natural language processing",
    #     "text analytics",
    #     "text processing",
    #     "localization",
    #     "computational linguistics",
    #     "ThaiNLP",
    #     "Thai NLP",
    #     "Thai language",
    # ],
    # classifiers=[
    #     "Development Status :: 5 - Production/Stable",
    #     "Programming Language :: Python :: 3",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: Apache Software License",
    #     "Natural Language :: Thai",
    #     "Topic :: Scientific/Engineering :: Artificial Intelligence",
    #     "Topic :: Text Processing",
    #     "Topic :: Text Processing :: General",
    #     "Topic :: Text Processing :: Linguistic",
    # ],
    # entry_points={
    #     "console_scripts": [
    #         "thainlp = pythainlp.__main__:main",
    #     ],
    # },
    # project_urls={
    #     "Documentation": "https://pythainlp.github.io/docs/3.0/",
    #     "Tutorials": "https://pythainlp.github.io/tutorials/",
    #     "Source Code": "https://github.com/PyThaiNLP/pythainlp",
    #     "Bug Tracker": "https://github.com/PyThaiNLP/pythainlp/issues",
    # },
)

# TODO: Check extras and decide to download additional data, like model files