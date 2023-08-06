import setuptools

from src.ppcmd import ppc

setuptools.setup(
    name="ppcmd",
    version=ppc.__version__,
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src", include=["*"]),
    python_requires=">=3.8",
    install_requires=[
        "fire == 0.4.0",
        "colorama == 0.4.6",
        "pygit2 == 1.10.1",
    ],
    entry_points="""
        [console_scripts]
        ppc=ppcmd.ppc.ppc:main_
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
