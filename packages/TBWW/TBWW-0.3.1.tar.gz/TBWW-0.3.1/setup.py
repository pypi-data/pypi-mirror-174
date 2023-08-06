#!/usr/bin/env python3

from setuptools import setup

import sys, os

if sys.argv[0] == "publish" or sys.argv[1] == "publish":
    os.system("python3 setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit(0)

setup(
    name="TBWW",
    version="0.3.1",
    description="Telegram Bot Wrapper Wraper",
    license="GNU GPL 3.0",
    install_requires=["python-telegram-bot"],
    py_modules = ["tbww"]
)
