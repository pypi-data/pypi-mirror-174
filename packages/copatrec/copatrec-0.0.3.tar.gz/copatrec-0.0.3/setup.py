# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 19:46:15 2021

@author: Siamak Khatami
@Email: siamak.khatami@ntnu.no
@License: https://creativecommons.org/licenses/by-nc-sa/4.0/
          Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
@Source: https://github.com/copatrec
@Document: https://github.com/copatrec
@WebApp: copatrec.org
"""

import setuptools
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setuptools.setup(
    name="copatrec",
    version="0.0.3",
    author="Siamak Khatami",
    author_email="<siamak.khatami@ntnu.no>",
    description="Correlation pattern recognizer (Copatrec), a package to find "
                "nonlinear patterns (regressions) using Machine Learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas',
                      'numpy',
                      'matplotlib',
                      'sklearn',
                      'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
