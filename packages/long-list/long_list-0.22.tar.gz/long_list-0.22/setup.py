from setuptools import setup, find_packages


setup(
    name='long_list',
    version='0.22',
    license='MIT',
    author="Tawfiq Khalilieh",
    author_email='taw.coding@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/tawfiqkhalilieh/LongList',
    keywords='list long_list infinitylist',
    install_requires=[],
)