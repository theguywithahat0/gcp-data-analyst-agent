from setuptools import setup, find_packages

setup(
    name="data-analyst",
    version="0.1",
    packages=find_packages(),
    author="Meltem Subasioglu",
    author_email="msubasioglu@google.com",
    description="GCP Data Analyst Agent - Multi-Agent System for BigQuery Analytics and ML",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="Apache License 2.0",
) 