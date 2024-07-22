import os
import re
import setuptools

NAME             = "restful-mongo"
AUTHOR           = "Christophe VG"
AUTHOR_EMAIL     = "contact@christophe.vg"
DESCRIPTION      = "a generic restful access-layer for mongo instances"
LICENSE          = "MIT"
KEYWORDS         = "restful mongo"
URL              = "https://github.com/christophevg/" + NAME
README           = ".github/README.md"
CLASSIFIERS      = [
  "Programming Language :: Python :: 3",
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Developers",
  "Topic :: Database",
  
]
INSTALL_REQUIRES = [
  "flask",
  "flask-restful",
  "pymongo",
  "eventlet",
  "python-dotenv",
  "pageable-mongo",
  
]
ENTRY_POINTS = {
  
}
SCRIPTS = [
  
]

HERE = os.path.dirname(__file__)

def read(file):
  with open(os.path.join(HERE, file), "r") as fh:
    return fh.read()

VERSION = re.search(
  r'__version__ = [\'"]([^\'"]*)[\'"]',
  read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
  setuptools.setup(
    name=NAME,
    version=VERSION,
    packages=setuptools.find_packages(),
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
