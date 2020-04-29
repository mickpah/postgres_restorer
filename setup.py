from setuptools import setup

with open("README.rst", 'r') as file:
    long_description = file.read()

setup(
    name='postgres_restorer',
    packages=['postgres_restorer'],
    version='1.1.2',
    license='MIT',
    description='Simple, lightweight tool that manages postgres databases during integration tests.',
    long_description=long_description,
    author='pyux',
    author_email='maciej.tomaszek@protonmail.com',
    url='https://github.com/pyux/postgres_restorer',
    download_url='https://github.com/pyux/postgres_restorer/archive/1.1.2.tar.gz',
    keywords=['postgres', 'integration', 'tests', 'restoring', 'database'],
    install_requires=[
        'attrs==19.3.0',
        'coverage==5.1',
        'more-itertools==8.2.0',
        'packaging==20.3',
        'pluggy==0.13.1',
        'psycopg2==2.8.5',
        'py==1.8.1',
        'Pygments==2.6.1',
        'pyparsing==2.4.7',
        'pytest==5.4.1',
        'pytest-cov==2.8.1',
        'six==1.14.0',
        'wcwidth==0.1.9'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
