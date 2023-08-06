import setuptools

with open("README.md", 'r') as f:
  long_description = f.read()

setuptools.setup(
  include_package_data = True,
  name = "algo-beast",
  version = "0.1.2",
  description = "Fyers Api Builder",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/krunaldodiya/algo-beast",
  author = "Krunal Dodiya",
  author_email = "kunal.dodiya1@gmail.com",
  packages = setuptools.find_packages(),
  install_requires = [
    "algo-beast-protocols",
    "certifi",
    "charset-normalizer",
    "click",
    "colorama",
    "idna",
    "pwinput",
    "requests",
    "urllib3",
  ],
  classifiers =[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent"
  ],
  entry_points = {
    'console_scripts': ['algo-beast=algo_beast.cmd:main'],
  }
)
