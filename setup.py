from setuptools import setup

setup(
    # Application name:
    name="zklib",
    # Version number (initial):
    version="0.1.2",
    # Application author details:
    url="https://github.com/AlSayedGamal/python_zklib",
    author="AlSayed Gamal, Marcos Benitez",
    author_email="mail.gamal@gmail.com, mail.marcosben.333@gmail.com",
    packages=["zklib"],
    install_requires=[
        'psycopg2',
        'psycopg2-binary',
        ],
    license="LICENSE.txt",
    description="Zk Attendance Machine lib",
    long_description=open("README.txt").read(),
    include_package_data=True,

)
