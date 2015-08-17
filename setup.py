import setuptools


def requirements(filename='requirements.txt'):
    """Returns a list of requirements to install."""
    requires = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                # skip blank lines and comments
                continue
            requires.append(line)

    return requires


setuptools.setup(
    name="twontest",
    version="0.0.1",
    author="Carlos Gil",
    install_requires=requirements(),
    packages=setuptools.find_packages(),
    description="Twitter contest wrecker.",
    tests_require=['nose'],
    test_suite='twontest.tests'
)
