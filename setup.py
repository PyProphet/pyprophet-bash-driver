# encoding: utf-8
from __future__ import print_function


from setuptools import setup, find_packages

setup(name="pyprophet-bash",
      version="0.0.1",
      author="Uwe Schmitt, George Rosenberger",
      author_email="uwe.schmitt@id.ethz.ch, rosenberger@imsb.biol.ethz.ch",
      license="BSD",
      install_requires=["pyprophet-cli>=0.0.17"],
      entry_points={'pyprophet_cli_plugin': ['config=pyprophet_bash.main:config']},
      include_package_data=True,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      )
