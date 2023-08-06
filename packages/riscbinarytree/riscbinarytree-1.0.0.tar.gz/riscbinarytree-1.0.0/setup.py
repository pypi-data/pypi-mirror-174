from setuptools import find_packages, setup

setup(
    name="riscbinarytree",
    version="1.0.0",
    author="e11i0t",
    author_email="mpkarthick2002@gmail.com",
    url="https://github.com/RISC-Capstone/risc-binarytree",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,  
    python_requires=">=3.7",
    license="MIT",
    install_requires=[
        "graphviz",
        "setuptools>=60.8.2",
        "setuptools_scm[toml]>=5.0.1",
    ],
    extras_require={
        "dev": [
            "black>=22.1.0",
            "flake8>=4.0.1",
            "isort>=5.10.1",
            "mypy>=0.931",
            "pre-commit>=2.17.0",
            "pytest>=6.2.1",
            "pytest-cov>=2.10.1",
            "sphinx",
            "sphinx_rtd_theme",
            "types-setuptools",
            "types-dataclasses",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Education",
    ],
)
