import setuptools

with open('cp2k_helper/_version.py', 'r') as fid:
    exec(fid.read())

with open('README.md', 'r') as readme:
    # ignore gifs
    description = ''.join([i for i in readme.readlines()
                           if not i.startswith('![')])

setuptools.setup(name='cp2k_helper',
                 version=__version__,
                 author='Dennis Loevlie',
                 url='https://github.com/loevlie/cp2k_helper',
                 description="A package to help accelerate working with cp2k",
                 long_description=description,
                 long_description_content_type='text/markdown',
                 packages=setuptools.find_packages(),
                 entry_points = {
                        'console_scripts': [
                            'cp2k_helper = cp2k_helper.__main__:main'
                        ]},
                 python_requires='>=3.5',
                 install_requires=['matplotlib',
                                   'numpy>=1.17.2',
                                   'pillow',
                                   'ase>=3.17.0',
                                   'seaborn',
                                   'pandas'])