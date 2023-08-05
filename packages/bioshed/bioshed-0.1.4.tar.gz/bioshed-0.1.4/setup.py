from setuptools import setup
setup(
    name='bioshed',
    version='0.1.4',
    description='BioShed Cloud Bioinformatics Tookit',
    install_requires=[
        'boto3',
        'pyyaml'
    ],
    python_requires='>=3.0',            # Minimum version requirement of the package
    py_modules=["bioshed"],             # Name of the python package
    packages=['bioshed'],
    package_dir={'bioshed':'bioshed/src'},     # Directory of the source code of the package
    package_data={'bioshed': ['bioshed/src/bioshed_utils/*.json', 'bioshed/src/bioshed_utils/*.yaml', 'bioshed/src/bioshed_atlas/files/*.txt', 'bioshed/src/bioshed_atlas/bioshed_utils/*.json', 'bioshed/src/bioshed_atlas/bioshed_utils/*.yaml']},
    scripts=['bioshed/src/bioshed_core_utils.py', 'bioshed/src/bioshed_deploy_core.py', 'bioshed/src/bioshed_init.py', \
             'bioshed/src/bioshed_atlas/atlas_encode_utils.py', 'bioshed/src/bioshed_atlas/atlas_utils.py', \
             'bioshed/src/bioshed_atlas/bioshed_utils/aws_batch_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/aws_s3_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/docker_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/file_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/lambda_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/program_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/quick_utils.py', 'bioshed/src/bioshed_atlas/bioshed_utils/run_main.py', \
             'bioshed/src/bioshed_utils/aws_batch_utils.py', 'bioshed/src/bioshed_utils/aws_s3_utils.py', 'bioshed/src/bioshed_utils/docker_utils.py', 'bioshed/src/bioshed_utils/file_utils.py', 'bioshed/src/bioshed_utils/lambda_utils.py', 'bioshed/src/bioshed_utils/program_utils.py', 'bioshed/src/bioshed_utils/quick_utils.py', 'bioshed/src/bioshed_utils/run_main.py'],
    entry_points={
        'console_scripts': [
            'bioshed=bioshed.src.bioshed:bioshed_cli_entrypoint'
        ]
    }
)
