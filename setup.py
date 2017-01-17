import json
from setuptools import setup

with open('setup.json') as f:
    data = json.load(f)

setup(**data)
