# Python Waveform Analysis Tools

The [CoRe](http://www.computational-relativity.org/) python package for the analysis of gravitational waves. It incorporates various functions based on previous codes 
[`scidata`](https://bitbucket.org/dradice/scidata/src/default/),
[`WAT`](https://bitbucket.org/bernuzzi/wat/src/master/) and 
[`pyGWAnalysis`](http://svn.einsteintoolkit.org/pyGWAnalysis/trunk/), and includes classes to work with the [CoRe waveform database](core-gitlfs.tpi.uni-jena.de/). 

## Installation

### PyPi

Run the command `pip install core-watpy`. Note that to use this package one needs to type `watpy` only, e.g. `import watpy`.

### From source

The installation relies on standard Python library `setuptools`.
Once the repository is cloned, the installation can be performed in two ways,
depending on the choice of the user:

* Run the command `python setup.py install` or `python setup.py install --user` inside the project directory. 
* Install the module via `pip` running the command `python -m pip install` inside the project directory. It is possible to include the `--user` option and the `-e` option for editing.

## Requirements

`watpy` works with Python3.
The following Python packages are required for installation:

* [Numpy](https://numpy.org/) (Python array-handler)
* [Scipy](https://www.scipy.org/) (Python scientific library)
* [Matplotlib](https://matplotlib.org/) (Nice visualization package)
* [H5py](https://www.h5py.org/) (Pythonic interface to HDF5)

For users interested in interactive usage of this package we suggest ipython notebooks. These can be installed with the following packages:

* [iPython](https://ipython.org/) (Strictly better version of the basic python shell)
* [Jupyter](https://jupyter.org/) (Notebooks, slides, HTML conversion of notebooks and more)

To sync and clone the CoRe DB `watpy` requires a git installation:

* [git](https://git-scm.com/) version control system
* [git-lfs](https://git-lfs.github.com/) API (Large File Storage)


## Content

`watpy` implements few classes to clone and work with CoRe waveforms.

 * `wave()` and `mwaves()` for multipolar waveforms data, see [wave.py](watpy/wave/wave.py)
 * `CoRe_db()` to clone the CoRe DB, add data etc, see [coredb.py](watpy/coredb/coredb.py)
 * `CoRe_idx()` to work with the [CoRe DB index](https://core-gitlfs.tpi.uni-jena.de/core_database/core_database_index/-/tree/master), see [coredb.py](watpy/coredb/coredb.py)
 * `CoRe_sim()` to work with simulation data in a CoRe repository, see [coredb.py](watpy/coredb/coredb.py)
 * `CoRe_run()` to work with one simulation run data in a CoRe repository, see [coredb.py](watpy/coredb/coredb.py)
 * `CoRe_h5()` to work with HDF5 data, see [coredb.py](watpy/utils/coreh5.py)
 * `CoRe_md()` to manage the metadata, see [metadata.py](watpy/codedb/metadata.py)

Please note that in order to use this package one needs to type `watpy` only, e.g. `import watpy`.

See [watpy_CoReDB.ipynb](https://git.tpi.uni-jena.de/core/watpy/-/blob/master/tutorials/watpy_CoReDB.ipynb) and [watpy_wave.ipynb](https://git.tpi.uni-jena.de/core/watpy/-/blob/master/tutorials/watpy_wave.ipynb) for our tutorials on the CoRe DB and waveforms.

## Features

 * Classes for multipolar waveform data
 * Classes to clone the [CoRe database](core-gitlfs.tpi.uni-jena.de/)
 * Gravitational-wave energy and angular momentum calculation routines
 * Psi4-to-h via FFI or time integral routines
 * Waveform alignment and phasing routines
 * Waveform interpolation routines
 * Waveform's spectra calculation
 * Richardson extrapolation
 * Wave objects contain already information on merger quantities (time, frequency)
 * Unit conversion package
 * Compatible numerical-relativity file formats: BAM, Cactus (WhiskyTHC / FreeTHC), CoRe database

 ## Versions
 Code versions are tagged as `MAJOR.MINOR.PATCH` following [semantic versioning](https://semver.org/)
 
 ### Latest version
 [![Python version](https://img.shields.io/badge/watpy-v0.1.1-blue)](https://git.tpi.uni-jena.de/core/watpy/-/tree/v0.1.1) 


