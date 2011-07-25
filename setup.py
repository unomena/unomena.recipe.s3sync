from setuptools import setup, find_packages

setup(
    name='unomena.recipe.s3sync',
    version='0.0.2',
    description='Unomena S3 Sync buildout recipe',
    author='Unomena',
    author_email='dev@unomena.com',
    url='http://unomena.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['boto'],
    zip_safe=False,
    entry_points = {'zc.buildout': ['default = unomena.recipe.s3sync:S3Sync']},
)
