from setuptools import setup
setup(
    name='bioshed',
    version='0.1.1',
    description='BioShed Cloud Bioinformatics Tookit',
    install_requires=[
        'boto3',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'bioshed=bioshed:bioshed_cli_entrypoint'
        ]
    }
)
