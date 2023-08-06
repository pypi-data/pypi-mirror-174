from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Trims away empty edges from images'
LONG_DESCRIPTION = 'A package that will trim away the edges with alpha 0 of an image.'

setup(
    name="ImgTrimmer",
    version=VERSION,
    author="Max Poppe",
    author_email="<poppe1max@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'numpy'],
    keywords=['python', 'image', 'trimming', 'cropping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
