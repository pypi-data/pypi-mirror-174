from setuptools import setup, find_packages

__VERSION = '1.1.1'

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='log.client',
      version=__VERSION,
      description='Easy log library for Elasticsearch',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='dugangandy@qq.com',
      packages=find_packages(),
      license='MIT',
      tests_require=['unittest2'],
      install_requires=['requests>=2.3.0', 'elasticsearch>=7.13.0'],
      classifiers=['Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'License :: OSI Approved :: MIT License'],
      url='https://github.com/dugangandy/log-client-python.git',
      )
