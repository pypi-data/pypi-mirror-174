from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="civiproxy_logs2json",
    version="1.0.3",
    author="Marc Michalsky",
    author_email="michalsky@forumZFD.de",
    packages=find_packages("civiproxy_logs2json", exclude=["test"]),
    description="Translate a CiviProxy logfile into JSON format.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcMichalsky/civiproxy_logs2json",
    license='MIT',
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'cpl2j = civiproxy_logs2json.__main__:main',
        ],
    },
)
