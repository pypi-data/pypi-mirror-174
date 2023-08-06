from setuptools import setup, find_packages
from CoegilSdk import __version__

setup(
    name='coegil-sdk',
    version=__version__,
    author="Mike Levine",
    author_email="mike@coegil.com",
    description="Coegil Python SDK",
    packages=find_packages(),
    include_package_data=True,
    url="https://coegil.com",
    python_requires='>=3.9',
    py_modules=[
        'CoegilSdk'
    ],
    install_requires=[
        'boto3',
        'requests'
    ]
)