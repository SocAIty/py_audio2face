from setuptools import setup, find_packages

setup(
    name='py_audio2face',
    version='0.1.1',
    description='Python script for Audio2Face lip and face animations, and emotions.',
    author='',
    packages=find_packages(),
    package_data={
        'py_audio2face': ['assets/mark_arkit_solved_default.usd'],
    },
    install_requires=[
        'requests',
        'tqdm',
        'importlib_resources'
    ]
)