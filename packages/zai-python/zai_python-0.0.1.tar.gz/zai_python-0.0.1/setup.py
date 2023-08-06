from setuptools import setup, find_packages


setup(
    name='zai_python',
    version='0.0.1',
    license='MIT',
    author="Matthew Clarkson",
    author_email='mpclarkson@gmail.com.com',
    packages=find_packages('zai_python'),
    package_dir={'': 'zai_python'},
    url='https://github.com/cemoh/zai-python',
    keywords='zai payments api',
    install_requires=[
          'requests',
      ],

)