from setuptools import setup, find_packages

setup(
    name='dm3loc',
    version='1.2.0',
    description='Deep-learning Framework with Multi-head Self-attention for Multi-label mRNA Subcellular Localization Prediction and Analyses',
    author='Duolin Wang',
    author_email='deepduoduo@gmail.com',
    install_requires = ['numpy', 'scipy', 'scikit-learn','matplotlib','h5py==2.10.0','keras==2.2.4', 'tensorflow==1.13.1', 'protobuf==3.20.0'],
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        'model': ['DM3Loc/model/*'],
        'testdata': ['DM3Loc/testdata/*']
    }

)
