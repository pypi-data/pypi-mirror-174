import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoRSA",
    version="0.0.6",
    author="Wu Xinyuan",
    author_email="1210011033@i.smu.edu.cn",
    description="A package for RSA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'open3d==0.15.2',
        'numpy==1.21.5',
        'tqdm==4.64.0',
        'pyvista==0.36.1',
    ],
)
