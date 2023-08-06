# FortranRNG
## Fortran RNG for Python3
Installation requires a modern Fortran compiler.
- Gfortran (macOS `brew install gcc`)
- Gfortran (Debian Linux `apt install gcc gfortran`)
- Gfortran (Amazon Linux `yum groupinstall "Development Tools"`)
- Cygwin (Windows `www.cygwin.org/cygwin`, good luck with that!)

### PyPi Installation
```shell
python3 -m pip install FortranRNG
```

### Source Installation
```shell
python3 -m pip install ./FortranRNG
```

### FortranRNG Python Interface
- Boolean Generator
  - `FortranRNG.percent_true(percent: float) -> bool(int)`
- Integer Generators
  - `FortranRNG.random_below(limit: int) -> int`
  - `FortranRNG.random_integer(low: int, high: int) -> int`
  - `FortranRNG.random_range(start: int, stop: int, step: int) -> int`
  - `FortranRNG.d(sides: int) -> int`
  - `FortranRNG.dice(rolls: int, sides: int) -> int`
  - `FortranRNG.plus_or_minus(amount: int) -> int`
  - `FortranRNG.plus_or_minus_linear(amount: int) -> int`
- Float Generators
  - `FortranRNG.canonical() -> float`
  - `FortranRNG.random_float(low, high) -> float`
  - `FortranRNG.triangular(low: float, high: float, mode: float) -> float`
- ZeroCool Index Generators
  - `FortranRNG.random_index(limit) -> int`
  - `FortranRNG.front_linear(limit) -> int`
  - `FortranRNG.middle_linear(limit) -> int`
  - `FortranRNG.back_linear(limit) -> int`
  - `FortranRNG.quantum_linear(limit) -> int`
