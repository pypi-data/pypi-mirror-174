from setuptools import setup, find_packages

setup(
    name="prismstudio",
    version="1.0.17",
    description="Python Extension for PrismStudio",
    author="Prism39",
    author_email="jmp@prism39.com",
    url="https://www.prism39.com",
    packages=find_packages(),
    python_requires=">=3.7",
    data_files=[("dlls", ["prism/pytransform/_pytransform.dll"])],
    install_requires=['pandas', 'requests', 'mypy', 'pyarrow', 'py7zr', 'multivolumefile', 'urllib3', 'tqdm', 'orjson', 'IPython'],
    include_package_data=True
)