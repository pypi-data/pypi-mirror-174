[![Python](https://img.shields.io/github/license/cdtn/glyf.svg)](https://python.org)
[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://python.org)

# Glyf

`Glyf` is a library for easy plotting of multiple images and graphs in Python. It provides a simple interface that allows flexible plots parametrization.

It supports `numpy` arrays as inputs and uses `matplotlib` to produce output visualizations.

## Basic usage

Import is as ordinary as this.
```python
from glyf import plot
```

- Plot single image.
  ```python
  plot(image)
  ```

- Plot image and mask overlayed.
  ```python
  plot([image, mask])
  ```

- Plot image and mask side to side.
  ```python
  plot([image, mask], combine='separate')
  ```

## Advanced usage

See [tutorials](tutorials).

## Installation

```
pip3 install glyf
```

## Acknowledgments

The code in this repository is based on [plotter](https://github.com/analysiscenter/batchflow/tree/54c6b0a4b87eace06abbe464b829cfd797fa2072/batchflow/plotter) module of **batchflow** framework developed by **Data Analysis Center** team under Apache 2.0 license. The main focus of this project is adding new features without needing to keep backward compatibility with API of the original project.
