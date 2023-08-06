# package_name

Description. 
The package package_name is used to:
   
>>"Processing" module:

  -Histogram matching;
  -Structural similarity;
  -Resize image;

>>Module "Utils":

  -read image;
  -Save Image;
  -Plot image;
  -Plot result;
  -Plot histogram;
	

## Installation

>>Setup walkthrough to host a Python package in the Test Pypi test environment

 Installation of the latest versions of "setuptools" and "wheel"
 
*py -m pip install --user --upgradesetuptools wheel*
  
  Make sure the directory in the terminal is the same as the "setup.py" file
  
C:\User\https://github.com/ozeaseromina/package-template
py setup.py sdist bdist_wheel
 
  *After completing the installation, verify that the folders below have been added to the project:*

   -build;
   -dist;
   -image_processing_test.egg-info.
   -Just upload the files, using Twine, to Test Pypi: 

py -m twine upload --repository testpypi dist/*
 After running the above command in the terminal, you will be asked to enter the username and password. Once this is done, the project will be hosted on Test Pypi. Host it on Pypi directly.
Here the goal is not to use Karina's project to post on my personal Pypi profile, since the project is hers. I still don't have any projects that can be used as a package.
However, keep in mind that Test Pypi, as its name implies, is just a testing environment. In order for the project to be available as a package to be used publicly, it needs to be hosted on the official Pypi website.
Local installation, after hosting on Test Pypi
 installation of dependencies
pip install -r requirements.txt
 Package Installation
Use package manager pip install -i https://test.pypi.org/simple/ image-processing-test to install image_processing-test

pip install image-processing-test

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
pip install package_name
```

## Usage

```python
from package_name.module1_name import file1_name
file1_name.my_function()
```

## Author
Romina Barrientos


## License
[MIT](https://choosealicense.com/licenses/mit/)