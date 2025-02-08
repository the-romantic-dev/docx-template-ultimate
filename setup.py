from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='docx-template_ultimate',
    version='0.0.1',
    author='the-romantic-dev',
    author_email='yvalentinasovofficial@gmail.com',
    description='Ultimate lib for Word namespaces template filling',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/the-romantic-dev/docx-template-ultimate',
    packages=find_packages(),
    include_package_data=True,  # Включает файлы из MANIFEST.in
    package_data={
        'dtu.converter': ['*.xslt'],  # Если xslt-файл лежит в папке пакета
    },
    install_requires=["latex2mathml>=3.77.0",
                      "lxml>=5.3.0",
                      "mpmath>=1.3.0",
                      "pillow>=11.1.0",
                      "python-docx>=1.1.2",
                      "sympy>=1.13.3",
                      "typing_extensions>=4.12.2",
                      "docx2pdf>=0.1.8"
                      ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='docx template ultimate',
    project_urls={
        'GitHub': 'https://github.com/the-romantic-dev'
    },
    python_requires='>=3.11'
)
