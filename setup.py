from setuptools import setup

setup(
    name='dtedifier',
    version='0.0.1',
    packages=['dtedifier'],
    include_package_data=True,
    extras_require = {
        'output_as_png': ['pypng'],
    },
    install_requires=[
    ],
    tests_requires=[
        'pytest',
    ]
)
