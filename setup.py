from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='docx-template_ultimate',
    version='0.0.1',
    author='the-romantic-dev',
    author_email='yvalentinasovofficial@gmail.com',
    description='Ultimate lib for Word document template filling',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='github.com',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='files speedfiles ',
    project_urls={
        'GitHub': 'your_github'
    },
    python_requires='>=3.6'
)
