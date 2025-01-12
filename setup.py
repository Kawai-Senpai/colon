from setuptools import setup, find_packages

setup(
    name='colon',
    version='0.1',
    description='A light weight ROS 2 project management and build tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ranit Bhowmick',
    author_email='bhowmickranitking@duck.com',
    url='https://github.com/Kawai-Senpai/colon',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'cmake',
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'colon = colon_build.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
    ],
)
