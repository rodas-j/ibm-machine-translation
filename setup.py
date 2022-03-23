from setuptools import setup

setup(
    name="ibm_model_1_mt",
    version="1.0",
    description="IBM Model One Machine Translation Implementation",
    author="Rodas Jateno & Best Chantanapongvanij",
    packages=["program"],  # same as name
    install_requires=[
        "pandas",
        "numpy",
    ],  # external packages as dependencies
)