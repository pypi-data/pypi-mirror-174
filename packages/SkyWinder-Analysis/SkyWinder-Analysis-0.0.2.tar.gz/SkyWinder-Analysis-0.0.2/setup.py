import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SkyWinder-Analysis",
    version="0.0.2",
    author="Carl Bjorn Kjellstrand",
    author_email="bkjell@gmail.com",
    description="A package for image analysis for aeronomy experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PolarMesosphericClouds/SkyWinder-Analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
