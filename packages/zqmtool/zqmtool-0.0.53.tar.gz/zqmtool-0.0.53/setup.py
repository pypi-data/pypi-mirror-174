import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="zqmtool",
    version='0.0.53',
    author='zou_qiming',
    author_email='zqm941028@gmail.com',
    description='zqmtool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=False,
    packages=setuptools.find_packages(),
)