import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="numpy_dataframe",
  version="0.0.1",
  description="A simple dataframe implementation using numpy as its basic element",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Carlos Molinero",
  author_email="",
  license="MIT",
  packages=["numpy_dataframe"],
  zip_safe=False
)
