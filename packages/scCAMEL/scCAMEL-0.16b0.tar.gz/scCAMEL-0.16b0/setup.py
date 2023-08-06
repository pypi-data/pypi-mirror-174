import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scCAMEL",
    version="0.16b",
    author="Yizhou Hu",
    author_email="yizhou.hu@ki.se",
    description="scCAMEL: single cell Cross- Annotation and Multimodal Estimation on Lineage trajectory;License: GPL version 3;Developed by: Yizhou Hu, Patrik Ernfors lab, MBB, Karolinska Institutet;Tutorials and other informations in :https://sccamel.readthedocs.io/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sccamel.readthedocs.io/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)