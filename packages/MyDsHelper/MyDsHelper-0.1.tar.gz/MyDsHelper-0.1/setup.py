from setuptools import setup, find_packages

setup(
    name='MyDsHelper',
    version='0.1',
    license='MIT',
    author="Doron Laadan",
    author_email='laadan1235@gmail.com',
    packages=find_packages('DsHelper'),
    package_dir={'': 'DsHelper'},
    url='https://github.com/DL1992/DsHelper',
    keywords='DsHelper',
    install_requires=[
        'deepchecks',
        'seaborn',
        'wordcloud',
        'nltk',
        'wandb',
    ],

)
