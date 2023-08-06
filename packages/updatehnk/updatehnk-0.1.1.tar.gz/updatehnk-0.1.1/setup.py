from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='updatehnk',
    version='0.1.1',
    description='Update coolers info',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Eduardo Martinez',
    author_email='eduardo.martinez.2117@gmail.com',
    keywords=['heineken', 'python', 'bigquery', 'storage', 'bucket']
)

install_requires = [
    'google-cloud-storage',
    'google-cloud-bigquery',
    'pytz'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)