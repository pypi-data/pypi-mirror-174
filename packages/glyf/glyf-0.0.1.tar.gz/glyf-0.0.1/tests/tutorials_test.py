""" Run tutorials notebooks. """
import os
import pytest
from glob import glob


TEST_DIR = os.getcwd()
NOTEBOOKS_DIR = '../tutorials/'
NOTEBOOKS_PATHS = glob(f'{NOTEBOOKS_DIR}*.ipynb')


@pytest.mark.parametrize('path', NOTEBOOKS_PATHS)
def test_tutorials(path):
    """ Ensure that tutorial works.

    Parameters
    ----------
    filename : str
        Path to tutorial notebook.
    """
    # pylint: disable=import-outside-toplevel
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    os.chdir(NOTEBOOKS_DIR)

    with open(path, 'r') as file:
        notebook = nbformat.read(file, as_version=4)

    executor = ExecutePreprocessor(timeout=600, kernel_name='python3')
    executor.preprocess(notebook)

    os.chdir(TEST_DIR)
