from setuptools import setup, find_packages

requirements = [
    'pika==1.3.1',
    'mariadb==1.0.7',
    'mysqlclient==2.0.3',
    'pydantic==1.10.2',
    'loguru==0.6.0',
    'sqlalchemy==1.4.42',
    'loguru==0.6.0',
    'numpy==1.23.4',
]

with open('README.md', 'r') as f:
    description = f.read()


def setup_package():
    __version__ = '0.0.16'
    url = 'https://github.com/Banayaki'

    setup(name='vidis_algorithms_api',
          description=description,
          version=__version__,
          url=url,
          license='MIT',
          author='Artem Mukhin',
          install_requires=requirements,
          packages=find_packages(),
          )


if __name__ == '__main__':
    # pip install --editable .
    setup_package()
