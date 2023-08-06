import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HSTI",
    version="0.0.35",
    author="Mads Nibe et. al.",
    author_email="mani@newtec.dk",
    description="The NEWTEC HSTI package contains fundamental functions for the data analysis of hyperspectral thermal images (HSTI).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'': ['data_files/*.txt']},
    package_dir={"": "hsti-analysis"},
    packages=setuptools.find_packages(where="hsti-analysis"),
    python_requires=">=3.6",
    install_requires=[
        "fast-histogram>=0.10",
        "fnnls>=1.0.0",
        "ipython>=7.25.0",
        "jupyter",
        "matplotlib>=3.4.2",
        "notebook>=6.4.0",
        "numpy>=1.19.5",
        "opencv-python>=4.5.2.54",
        "Pillow>=8.4.0",
        "scikit-learn>=0.24.2",
        "scipy>=1.7.0",
        "Screeninfo>=0.8",
        "RangeSlider>=2021.7.4",
        "tk>=0.1.0"
    ]
)
