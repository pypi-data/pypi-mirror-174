from setuptools import setup, find_packages


VERSION = '1.0.0'

setup(
    name='shiqingTools',  # package name
    version=VERSION,  # package version
    author="buyizhiyou",
    author_email="2557040812@qq.com",
    license="MIT",
    url='https://github.com/buyizhiyou',
    description='some personal tools',  # package description
    packages=find_packages('shiqingTools'),
    package_dir = {'':'shiqingTools'},
    include_package_data = True,
    zip_safe=False,
)
