from setuptools import setup, find_packages


def readme(file_name: str):
    try:
        with open(file_name, encoding='utf-8') as f:
            return f.read()
    except:
        return ''


setup(
    name='hbookerLib',
    version='0.1.5',
    packages=find_packages(),
    description='通过开源项目HbookerAppNovelDownloader代码修改而来的API库',
    long_description=readme('README.md'),
    long_description_content_type='text/markdown',  # if you have a README.md
    author='catnovel',
    author_email='cat@cat.com',
    url='https://github.com/catnovel/hbookerLib',
    license=readme('LICENSE'),
    install_requires=[
        'setuptools~=57.4.0',
        'requests~=2.26.0',
        'cryptography~=41.0.7'
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
