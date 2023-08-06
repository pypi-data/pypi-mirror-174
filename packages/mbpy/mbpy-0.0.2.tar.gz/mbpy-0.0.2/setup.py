from setuptools import find_packages, setup
setup(
    name='mbpy',
    packages=find_packages(),
    version='0.0.2',
    description='microBees Python Library',
    author='microbeestech',
    license='MIT',
    install_requires=[],
    setup_requires=[''],
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["mbpy"],             # Name of the python package

)
