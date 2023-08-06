from setuptools import setup, find_packages
requirements = ['requests']
setup(
    name='IpfsML',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    license='GNU General Public License v3.0',
    description='A python wrapper for the nft-storage',
    long_description=open('README.md').read(),
    keywords=['nft-storage', 'ipfs SDK'],
    install_requires=requirements,
    url='https://github.com/kbm9696/Store-Retrive-DataSet-Models-in-IPFS',
    author='Balamurugan',
    author_email='kbala007.1996@gmail.com',
    long_description_content_type='text/markdown'
)
