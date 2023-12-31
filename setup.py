from setuptools import setup, find_packages

setup(
    name='hbookerLib',
    version='0.1.1',
    packages=find_packages(),
    description='通过开源项目HbookerAppNovelDownloader代码修改而来的API库',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # if you have a README.md
    author='hang333',
    author_email='cat@cat.com',
    url='https://github.com/catnovel/hbookerLib',
    install_requires=[
        'setuptools~=57.4.0',
        'requests~=2.26.0',
        'crypto~=1.4.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
