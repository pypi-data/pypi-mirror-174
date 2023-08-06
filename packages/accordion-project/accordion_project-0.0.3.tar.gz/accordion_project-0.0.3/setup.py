from setuptools import find_packages, setup
setup(
    name='accordion_project',
    packages=find_packages(include=['accordion_project']),
    version='0.0.3',
    description='ACCORDION Utils library',
    author='Konstantinos Tserpes',
    author_email='tserpes@hua.gr',
    license='Apache-2.0',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)