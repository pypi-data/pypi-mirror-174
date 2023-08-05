from setuptools import setup
setup(
    name='bioshed',
    version='0.1.2',
    description='BioShed Cloud Bioinformatics Tookit',
    install_requires=[
        'boto3',
        'pyyaml'
    ],
    python_requires='>=3.0',            # Minimum version requirement of the package
    py_modules=["bioshed"],             # Name of the python package
    package_dir={'':'bioshed/src'},     # Directory of the source code of the package

    entry_points={
        'console_scripts': [
            'bioshed=bioshed:bioshed_cli_entrypoint'
        ]
    }
)
