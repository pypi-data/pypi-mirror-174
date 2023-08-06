from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
    setup(
        name='zai_python',
        version='0.0.0.1',
        license='MIT',
        description="A Python SDK for the Zai Payments API.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Matthew Clarkson",
        author_email='mpclarkson@gmail.com.com',
        packages=find_packages('zai_python'),
        package_dir={'': 'zai_python'},
        url='https://github.com/cemoh/zai-python',
        keywords='zai payments api sdk',
        install_requires=[
            'requests',
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
     ],
 )