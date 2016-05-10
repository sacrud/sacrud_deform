import os
from setuptools import setup

here = os.path.dirname(os.path.realpath(__file__))


def read(name):
    with open(os.path.join(here, name)) as f:
        return f.read()


setup(
    name='sacrud_deform',
    version="0.1.6",
    url='http://github.com/sacrud/sacrud_deform/',
    author='Svintsov Dmitry',
    author_email='root@uralbash.ru',
    packages=['sacrud_deform', ],
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    license="MIT",
    package_dir={'sacrud_deform': 'sacrud_deform'},
    description='Form generator for SQLAlchemy models.',
    long_description=read('README.rst'),
    install_requires=read('requirements.txt'),
    tests_require=read('requirements.txt') + read('requirements-test.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid ",
        "Topic :: Internet",
        "Topic :: Database",
    ],
)
