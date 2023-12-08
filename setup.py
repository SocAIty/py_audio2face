from setuptools import setup, find_packages

setup(
    name='py_audio2face',
    version='0.1.0',
    description='Python script for Audio2Face lip and face animations',
    author='',
    packages=find_packages(),
    #data_files=[('assets', ['py_audio2face/assets/mark_arkit_solved_default.usd'])],
    package_data={
        'py_audio2face': ['assets/mark_arkit_solved_default.usd'],
    },
    install_requires=[
        'requests',
        'tqdm',
        # Add other dependencies as needed
    ]
)