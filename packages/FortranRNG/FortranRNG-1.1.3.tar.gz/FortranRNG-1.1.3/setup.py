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
    version="1.1.3",
    ext_modules=[
        Extension(name='FortranRNG', sources=['FortranRNG.f90']),
    ],
    description="Fortran RNG for Python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[dev_status["Pro"]],
    python_requires=">=3.7",
)
