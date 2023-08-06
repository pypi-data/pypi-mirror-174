from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'For logging collected data in a filetype of choice'
LONG_DESCRIPTION = "https://github.com/HugeCoderGuy/datawriter README.md"
long_description_content_type = "text/markdown"
url = "https://github.com/HugeCoderGuy/datawriter"

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="datawriter", 
        version=VERSION,
        author="Alex Lewis",
        author_email="alexscottlewis@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

# create new dist:  python setup.py sdist bdist_wheel
# upload to pypi:   twine upload --skip-existing dist/*