# pytokei
Pytokei is a python binding to [tokei](https://github.com/XAMPPRocky/tokei), from their repo:

---

<p align="center">
Tokei is a program that displays statistics about your code. Tokei will show the number of files, total lines within those files and code, comments, and blanks grouped by language.
</p>

--- 

This wrapper allows to obtain the same reports directly from python.

For more information about `tokei`, please visit its [repo](https://github.com/XAMPPRocky/tokei).

## Installation

```bash
pip install pytokei
```

Requires Python >= 3.7.

Binaries are available for:

?

Otherwise, you can install from source which requires Rust stable to be installed.

## Development

You will need:

- [maturin](https://www.maturin.rs/installation.html) to compile the library

- `maturin develop` / `make develop` to compile the code.

From python side:

Run `make install-dev` inside a virtual environment, `make test`, `make mypy` and `make format` to ensure everything is as expected, and `make docs` to build the documentation.

*There are some problems when building the docs with mkdocstrings, a reminder is in the following [github issue](https://github.com/mkdocstrings/mkdocstrings/issues/404). For the moment, it seems that the best option is to remove the .so file and build the docs without it.*
