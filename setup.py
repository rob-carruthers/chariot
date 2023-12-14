from setuptools import find_packages
from setuptools import setup

with open("requirements.txt", encoding="utf-8") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='chariot',
      version="0.0.1",
      description="Your friendly TFL wrapper API controllable via natural language",
      author="Rob Carruthers",
      author_email="rob.m.carruthers@googlemail.com",
      #url="",
      install_requires=requirements,
      packages=find_packages(),
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
