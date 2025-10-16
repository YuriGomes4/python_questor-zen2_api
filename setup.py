from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='py_zen',
    version='0.0.2',
    license='MIT License',
    author='Yuri Gomes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='yuri@agoradeulucro.com.br',
    keywords='questor zen 2',
    description=u'Wrapper não oficial do Questor Zen 2',
    packages=['py_zen'],
    install_requires=['requests'],)