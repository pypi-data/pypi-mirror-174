import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='binary_packer',
    version='1.0.0',
    author='Komissarov Andrey',
    author_email='Komissar.off.andrey@gmail.com',
    description='Light and fast packer dataclasses to binary',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/moff4/packer',
    install_requires=[
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
