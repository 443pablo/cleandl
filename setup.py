from setuptools import setup, find_packages

setup(
    name='cleandl',
    version='0.0.1',
    author='Pablo Gracia',
    author_email='pablo@pablogracia.net',
    description='A tool to automatically organize the downloads folder into categorized views based on file extensions.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        
    ],
    entry_points={
        'console_scripts': [
            'cleandl=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)