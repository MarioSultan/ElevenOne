# Installation

**ElevenOne** is available on PyPI and can be installed easily using `pip`.

## Prerequisites

ElevenOne requires **Python 3.8** or higher. It relies on standard scientific Python libraries:

* [NumPy](https://numpy.org/) (array operations and numerical computing)
* [Pandas](https://pandas.pydata.org/) (data structures and table formatting)
* [Matplotlib](https://matplotlib.org/) (plotting and visualization engine)

*(Optional)* **ReportLab** is required if you intend to generate PDF reports directly.

---

## Installing via PyPI

To install the latest stable version from PyPI, run:

```bash
pip install elevenone
```

---

## Verification

You can verify that ElevenOne is correctly installed by importing it in a Python session:

```python
import elevenone as eo

print(eo.__version__)
```

If no errors occur, ElevenOne is ready for use!