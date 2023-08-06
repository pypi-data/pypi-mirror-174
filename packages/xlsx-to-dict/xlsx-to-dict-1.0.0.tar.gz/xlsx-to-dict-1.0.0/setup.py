from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='xlsx-to-dict',
    version='1.0.0',
    license='MIT License',
    author='Jonatan Rodrigues da Silva',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jonatanjrss@gmail.com',
    keywords='xlsx dict',
    description=u'Transforma xlsx file e dict python',
    packages=['xlsx_to_dict', 'tests'],
    install_requires=['openpyxl', 'python-slugify'],)
