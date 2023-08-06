from numpy.distutils.core import setup
from numpy.distutils.core import Extension

with open("README.md", "r") as file:
    long_description = file.read()

dev_status = {
    "Alpha": "Development Status :: 3 - Alpha",
    "Beta": "Development Status :: 4 - Beta",
    "Pro": "Development Status :: 5 - Production/Stable",
    "Mature": "Development Status :: 6 - Mature",
}

setup(
    name='FortranRNG',
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    url="https://github.com/BrokenShell/FortranRNG-API/FortranRNG",
    version="1.1.4",
    ext_modules=[
        Extension(name='FortranRNG', sources=['FortranRNG.f90']),
    ],
    license="Free for non-commercial use",
    description="Fortran RNG for Python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["Darwin", "Linux", "Windows"],
    classifiers=[
        dev_status["Pro"],
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Fortran",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "FortranRNG", "High Performance Random Value Toolkit",
        "percent true",
        "d", "dice",
        "random below", "random integer", "random range",
        "plus or minus", "plus of minus linear",
        "canonical", "random float", "triangular",
        "ZeroCool Algorithms", "random index",
        "front linear", "middle linear", "back linear", "quantum linear",
    ],
    python_requires=">=3.7",
)
