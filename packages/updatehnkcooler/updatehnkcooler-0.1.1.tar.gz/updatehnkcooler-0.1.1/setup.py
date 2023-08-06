from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name="updatehnkcooler",
    version="0.1.1",
    author="Eduardo Martinez",
    author_email="eduardo.martinez.2117@gmail.com",
    description="Update coolers info",
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(),
    install_requires = ['google-cloud-storage', 'google-cloud-bigquery', 'pytz'],
    keywords=['heineken', 'python', 'bigquery', 'storage', 'bucket'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)