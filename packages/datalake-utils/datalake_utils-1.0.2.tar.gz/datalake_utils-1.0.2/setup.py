from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='datalake_utils',
    version='1.0.2',
    description="Manipulate data on Amazon S3 using Apache Hadoop filesystem compability",
    # py_modules=["datalake_utils"],
    # package_dir={'': 'datalake_utils'},
    # extras_require={
    #     "dev": [
    #         "pytest >= 3.7",
    #         "check-manifest",
    #         "twine"
    #     ]
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luis Roberto de Oliveira Moro",
    # author_email="vaidhyanathan.sm@gmail.com",
    # url="https://github.com/smv1999/number-utility"
)