from distutils.core import setup

with open("README.md", 'r') as file:
    long_description = file.read()

setup(
    name='postgres_restorer',
    packages=['postgres_restorer'],
    version='1.1.0',
    license='MIT',
    description='Simple, lightweight tool that manages postgres databases during integration tests.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='pyux',
    author_email='maciej.tomaszek@protonmail.com',
    url='https://github.com/pyux/postgres_restorer',
    download_url='https://github.com/pyux/postgres_restorer/archive/1.1.0.tar.gz',
    keywords=['postgres', 'integration', 'tests', 'restoring', 'database'],
    install_requires=[
        'attrs',
        'certifi',
        'chardet',
        'codecov',
        'coverage',
        'idna',
        'more-itertools',
        'packaging',
        'pluggy',
        'psycopg2',
        'py',
        'pyparsing',
        'pytest',
        'pytest-cov',
        'requests',
        'six',
        'urllib3',
        'wcwidth'
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
