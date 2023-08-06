from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


packages = find_packages(exclude=['tests', 'tests.*'])

setup(
    name='source_converter',
    version='0.1.12',
    license='MIT',
    author="Noricha",
    author_email="noricha.vr@gmail.com",
    packages=packages,
    install_requires=[
        'Pygments==2.13.0',
        'requests==2.28.1',
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)
