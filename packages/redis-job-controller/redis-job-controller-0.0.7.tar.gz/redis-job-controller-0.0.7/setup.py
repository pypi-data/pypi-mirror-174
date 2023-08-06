from setuptools import setup, find_packages


# with open('README.rst') as f:
#     readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()


setup(
    name='redis-job-controller',
    version='0.0.7',
    description='Package for enqueuing and fetching async jobs, using Redis as a queue and result repository',
#    long_description=readme,
    author='Karol Ważny',
#    author_email='me@kennethreitz.com',
#    url='https://github.com/kennethreitz/samplemod',
#    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['redis']
)
