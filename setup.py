from setuptools import setup

setup(name='Magstim',
    version='1.0.5',
    download_url="https://github.com/kaysoky/MagStim_PyServer",
    packages=['Magstim'],
    install_requires=[
        'pyserial>=2.5', 
        'web.py>=0.37'
    ],
    zip_safe=False,
    platforms=['any'],
)
