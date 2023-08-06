from setuptools import setup, find_packages
readme = open('README.txt', encoding="utf8")

setup(
    name='quicksqlconnector',
    version='1.4',
    license='MIT',
    license_files='LICENSE',
    author="Anas Raza",
    author_email='anasraza1@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Anas-Dew/QuickSQLConnector',
    keywords='quicksqlconnector, sql, database, mysql',
    install_requires=[
          'mysql-connector-python',
          'prettytable'
      ],
    description='Use MySQLServer like a layman. Super easy to use MySQL with Python',
    long_description=readme.read(),
    long_description_content_type='text/markdown'
)