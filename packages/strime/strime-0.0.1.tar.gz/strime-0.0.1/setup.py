from setuptools import setup
import io


with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='strime', 
    author='WoidZero',
    version='0.0.1', 
    license='MIT',
    url='https://github.com/woidzero/strime',
    description='A simple string (time+unit) to seconds converter.', 
    packages=['strime'], 
    author_email='woidzeroo@gmail.com', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False)