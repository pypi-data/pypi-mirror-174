from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='UC-Quantum-tools',
    version='0.1.8',
    author='Marek Brodke, with support from the University of Cincinnati',
    description='Provides functionaliy for UC-Quantum-Lab development tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='development',
    python_requires='>=3.6',
    license="MIT",
    author_email="brodkemd@mail.uc.edu",
    url="https://github.com/UC-Advanced-Research-Computing/UC-Quantum-tools",
    install_requires=[
        'qiskit>=0.36',
        'matplotlib>=2.2.0',
        'qiskit-aer>=0.10.4',
        'qiskit-ibmq-provider>=0.19.1',
        'qiskit-ignis>=0.7.0',
        'qiskit-terra>=0.20.1',
        "pylatexenc>=2.0"
    ]
)