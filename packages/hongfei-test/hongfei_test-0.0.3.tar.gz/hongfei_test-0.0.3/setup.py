from setuptools import setup, find_packages

setup(
    name = 'hongfei_test',
    version = '0.0.3',
    keywords='test',
    description = 'a library for test',
    license = 'MIT License',
    url = 'https://github.com/test/test',
    author = 'hongfei',
    author_email = 'hongfei@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'requests>=2.19.1',
    ],
)
