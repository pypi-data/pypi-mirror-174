# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybuildit2",
    version="1.0.0",
    author="SR",
    author_email="info@smartrobotics.jp",
    description="python API for Buildit Actuator (For Buildit Actuator v1.0.1 and above",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['crc8','numpy','pyserial', 'matplotlib', 'numpy', 'pyyaml'],
    url="https://www.smartrobotics.jp/products/buildit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'pybuildit2': ['gui/imgs/*.gif', 'gui/config/*.yml'] },
    entry_points={
        'console_scripts':[
            'builditctl = pybuildit2.cli.builditctl:main',
        ],
        'gui_scripts':[
            'builditctl-gui = pybuildit2.gui.builditctl:main',
        ],
    },
)
