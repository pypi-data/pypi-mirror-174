from setuptools import setup
setup(
    name='bioshed',
    version='0.1.6',
    description='BioShed Cloud Bioinformatics Tookit',
    install_requires=[
        'boto3',
        'pyyaml'
    ],
    python_requires='>=3.0',            # Minimum version requirement of the package
    py_modules=["bioshed"],             # Name of the python package
    package_dir={'bioshed':'bioshed/src'},     # Directory of the source code of the package
    packages=['bioshed/src/bioshed_utils', 'bioshed/src/bioshed_atlas', 'bioshed/src/bioshed_atlas/bioshed_utils', 'bioshed/src/bioshed_atlas/files'],
     data_files=[('bioshed/src/bioshed_atlas/files/', ['bioshed/src/bioshed_atlas/files/search_encode_assay.txt', 'bioshed/src/bioshed_atlas/files/search_encode_assaycategory.txt', 'bioshed/src/bioshed_atlas/files/search_encode_assaytarget.txt', 'bioshed/src/bioshed_atlas/files/search_encode_assaytype.txt', 'bioshed/src/bioshed_atlas/files/search_encode_celltype.txt', 'bioshed/src/bioshed_atlas/files/search_encode_disease.txt', 'bioshed/src/bioshed_atlas/files/search_encode_filetype.txt', 'bioshed/src/bioshed_atlas/files/search_encode_genome.txt', 'bioshed/src/bioshed_atlas/files/search_encode_platform.txt', 'bioshed/src/bioshed_atlas/files/search_encode_species.txt', 'bioshed/src/bioshed_atlas/files/search_encode_tissue.txt']), \
     ('bioshed/src/bioshed_utils/', ['bioshed/src/bioshed_utils/aws_config_constants.json', 'bioshed/src/bioshed_utils/specs.json', 'bioshed/src/bioshed_utils/packages.yaml'])],
    entry_points={
        'console_scripts': [
            'bioshed=bioshed.src.bioshed:bioshed_cli_entrypoint'
        ]
    }
)
