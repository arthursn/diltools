# diltools

Personal set of tools for manipulating Bähr dilatometer output data

# Installation and requirements

diltools runs in both python2 (>= 2.7) and python3 (>=3.5).

diltools depends on the following non-standard python libraries:

- numpy
- scipy
- matplotlib
- pandas

First clone diltools repository:

```bash
git clone https://github.com/arthursn/diltools
```

Then install diltools by running setup.py:

```bash
python setup.py install
```

Use the `--user` option to install diltools in the user folder:

```bash
python setup.py install --user
```

Please notice that `setuptools` must be installed beforehand.

If diltools is installed using `setup.py`, all dependencies should be automatically solved. Otherwise, the required libraries can be installed from the [Python Package Index](https://pypi.org) using pip:

```bash
pip install numpy scipy matplotlib pandas
```
