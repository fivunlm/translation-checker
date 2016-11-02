from setuptools import setup

setup(
    name='tchecker',
    version='0.1.0',
    packages=['tchecker'],
    install_requires=[
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'tchecker = tchecker.__main__:main'
        ]
    })
