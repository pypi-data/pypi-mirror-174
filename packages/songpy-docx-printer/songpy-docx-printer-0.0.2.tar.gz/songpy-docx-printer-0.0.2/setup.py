from setuptools import setup, find_packages


# with open('README.rst') as f:
#     readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='songpy-docx-printer',
    version='0.0.2',
    description='Support package for package songpy, for printing formatted songbooks to docx files',
#    long_description=readme,
    author='Karol Ważny',
#    author_email='me@kennethreitz.com',
#    url='https://github.com/kennethreitz/samplemod',
#    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ["resources/*"]}
)