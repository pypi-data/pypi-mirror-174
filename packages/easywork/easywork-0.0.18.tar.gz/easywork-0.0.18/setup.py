from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easywork',
    version='0.0.18',
    description='泡面加出品',
    url='https://www.paomian.plus',
    author='paomianplus',
    author_email='paomianplus@foxmail.com',
    install_requires=['colorlog==6.6.0',
                      'fake_useragent==0.1.11',
                      'Pillow==9.0.0',
                      'pycryptodome==3.12.0',
                      'python_dateutil==2.8.2',
                      'requests==2.27.0',
                      'ruamel.base==1.0.0',
                      'setuptools==58.0.4'],
    long_description=long_description,
    packages=find_packages()
)
