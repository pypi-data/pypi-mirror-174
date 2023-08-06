from setuptools import setup, find_namespace_packages

setup(
    name="SearchProblemsAI",
    url="https://github.com/tboulet/AI-Agents-for-Search-Problems",
    author="Timothé Boulet",
    author_email="timothe.boulet0@gmail.com",
    
    packages=find_namespace_packages(),

    version="1.0.1",
    license="MIT",
    description="SearchProblemsAI is a library of AI agents for Search Problems.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)