from setuptools import setup

setup(
    name="GMXFit",
    version="0.1.0",
    description="A python toolkit to fit potential energy surface data",
    url="https://github.com/masrul/GMXFit",
    author="Masrul Huda",
    author_email="mmh568@msstate.edu",
    packages=["GMXFit"],
    py_modules=["Fit", "Plotter", "UnitConverter", "GaussIO", "TraPPE", "Util"],
    install_requires=["numpy>=1.14", "scipy>=1.2", "matplotlib>3.0"],
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Molecular Simulation",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
)
