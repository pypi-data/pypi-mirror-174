from setuptools import setup
setup(
    name='bioshed',
    version='0.1.0',
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
