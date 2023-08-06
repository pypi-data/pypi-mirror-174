from setuptools import setup

setup(
    name='simStatus',
    version='v1.0.4',

    url='https://github.com/Khalil-Youssefi/simStatus',
    author='Khalil Youssefi',
    author_email='kh4lil@outlook.com',
    python_requires='>=3.6',
    py_modules=['simStatus'],
    install_requires=[
    'qrcodeT',
    'requests',
    ],
)
