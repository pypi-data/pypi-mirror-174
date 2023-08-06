import re

from setuptools import setup, find_packages

VERSIONFILE = "pyMixtComp/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="pyMixtComp",
    version=verstr,  # version number is set in pyMixtComp/_version.py
    author="Mostafa Abdelrashied",
    description="Mixture models with heterogeneous data sets and partially missing data management.",
    # long_description=open("README.md", "r").read(),
    # long_description_content_type="text/markdown",
    keywords=["clustering", "mixture model", "heterogeneous", "missing data"],
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    packages=find_packages(),
    # packages=["pyMixtComp"],
    include_package_data=True,
    python_requires='>=3.9',
    package_data={"pyMixtComp": ["pyMixtCompBridge.so"], "": ["data/*.csv"]},
    install_requires=["numpy", "pandas", "scikit-learn",
                      "seaborn", "matplotlib", "scipy"],
)
