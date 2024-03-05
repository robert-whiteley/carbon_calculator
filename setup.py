from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='carb_calc',
      version='0.0.0',
      description='Carbon Calculator (api)',
      license='MIT',
      author='Carbon Calculator team',
      url='https://github.com/robert-whiteley/carbon_calculator',
      install_requires=requirements,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
