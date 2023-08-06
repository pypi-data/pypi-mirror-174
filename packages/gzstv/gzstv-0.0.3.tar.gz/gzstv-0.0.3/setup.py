from setuptools import setup, find_packages

NAME             = "gzstv"
AUTHOR           = "Mushan"
AUTHOR_EMAIL     = "wwd137669793@gmail.com"
DESCRIPTION      = "GZS-TV: A Generalizable zero-shot speaker adaptive text-to-speech and voice conversion model"
LICENSE          = "CC BY-NC 4.0"
KEYWORDS         = "None"
URL              = "https://github.com/mushanshanshan/gzs_tv"
README           = ".github/README.md"
VERSION          = "0.0.3"
CLASSIFIERS      = [
  "Environment :: Console",
  "License :: Free For Educational Use",
  "Programming Language :: Python :: 3.7",
  "Operating System :: POSIX :: Linux"
]
INSTALL_REQUIRES = [
  "Cython",
  "numpy",
]

ENTRY_POINTS = {
    
}

SCRIPTS = [
  
]

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

if __name__ == "__main__":
  setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
    scripts=SCRIPTS,
    include_package_data=True    
  )