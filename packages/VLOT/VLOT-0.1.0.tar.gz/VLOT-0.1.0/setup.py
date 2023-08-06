from gettext import install
from struct import pack
from setuptools import find_packages, setup

setup(
    name ='VLOT',
    version='0.1.0',
    description='An efficient token vocabulary construction method',
    url ='https://github.com/Jingjing-NLP/VOLT',
    author='Jingjing Xu',
    author_email='jingjingxu@pku.edu.cn',
    packages=find_packages(),
    install_requires = ['tqdm','POT','sentencepiece','subword-nmt'],
    #dependency_links=
    #['https://github.com/moses-smt/mosesdecoder/tarball/master#egg-package-1.0'],
    classifiers=[
       'Development Status :: 1 - Planning',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 3',
       'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    include_package_data=True
)
