from setuptools import setup, find_packages

setup(
    name='clay.taobao',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Scrapy',
    ],
    author='Clay',
    author_email='clay0510@163.com',
    maintainer='Clay'
)
