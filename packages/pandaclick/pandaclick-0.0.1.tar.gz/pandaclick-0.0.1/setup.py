from setuptools import setup

setup(
    name='Panda Click',
    version='0.1.0',
    description='pandas to clickhouse write',
    author='Ned',
    author_email='bedretdinoff@mail.ru',
    license='BSD 2-clause',
    packages=['pandaclick'],
    install_requires=["pandas","sqlalchemy","requests","jinja2","clickhouse-sqlalchemy"],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)