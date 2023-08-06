from setuptools import setup

setup(
    name='oftoolbox',
    version='0.1.0',    
    description='My personal toolbox.',
    author='Tobias Offermann',
    author_email='tobias.offermann@rwth-aachen.de',
    license='BSD 2-clause',
    packages=['oftoolbox'],
    install_requires=['numpy',                     
                    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
