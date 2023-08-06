from pathlib import Path
from setuptools import find_packages, setup

dependencies = ['matplotlib', 'numpy', 'cv2']

# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pylogik',
    packages=find_packages(),
    version='0.0.1',
    description='A collection of image and statistical processing functions and classes',
    author='Adrienne Kline',
    author_email='askline1@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    # project_urls={
    #     "Bug Tracker": "https://github.com/adriennekline/psmpy",
    # },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
