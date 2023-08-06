import setuptools

setuptools.setup(
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        'PyATEMMax'
    ],
    extras_require={
        'dev': ['check-manifest']
    }
)