from setuptools import setup
from setuptools import find_namespace_packages

# Load the README file.
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    

    # Define the library name, this is what is used along with `pip install`.
    name='lineFollower',

    # Define the author of the repository.
    author='Daniel Poul Mtowe',

    # Define the Author's email, so people know who to reach out to.
    author_email='danielpoul.dp@gmail.com',

    # Define the version of this library.
    # Read this as
    #   - MAJOR VERSION 0
    #   - MINOR VERSION 1
    #   - MAINTENANCE VERSION 0
    version='0.0.7',

    # Here is a small description of the library. This appears
    # when someone searches for the library on https://pypi.org/search.
    description='A line follower wireless vehicle.',

    # I have a long description but that will just be my README
    # file, note the variable up above where I read the file.
    long_description=long_description,

    # This will specify that the long description is MARKDOWN.
    long_description_content_type="text/markdown",

    # Here is the URL where you can find the code, in this case on GitHub.
    url='https://github.com/sihsch/1wireless-vehicle/tree/master/linefollower',

    # These are the dependencies the library needs in order to run.
    install_requires=[
        'imagezmq==1.1.1',
        'imutils==0.5.4',
        'matplotlib',
        'pyzmq',
    ],

    # Here are the keywords of my library.
    keywords = ' linefollower, wirelessvehicle' ,

    # here are the packages I want "build."
    packages=find_namespace_packages(
        include=['lineFollower', 'lineFollower.*']
    ),

    include_package_data=True,

    # Here I can specify the python version necessary to run this library.
    python_requires='>=3.8',

    # Additional classifiers that give some characteristics about the package.
    # For a complete list go to https://pypi.org/classifiers/.
    classifiers=[



        # Here I'll add the audience this library is intended for.
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        # Here I'll define the license that guides my library.
        'License :: OSI Approved :: MIT License',

        # Here I'll note that package was written in English.
        'Natural Language :: English',

        # Here I'll note that any operating system can use it.
        'Operating System :: OS Independent',

        # Here I'll specify the version of Python it uses.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',


    ]
)