import typing

import setuptools

import multi_notifier.__version__


def load_req() -> typing.List[str]:
	with open('requirements.txt') as f:
		return f.readlines()


VERSION = multi_notifier.__version__.__version__

setuptools.setup(
	name="multi_notifier",
	version=VERSION,
	author="Seuling N.",
	description="notify multiple recipients on multiple protocols",
	long_description="notify multiple recipients on multiple protocols",
	packages=setuptools.find_packages(exclude=["tests*"]),
	install_requires=load_req(),
	python_requires=">=3.10",
	license="Apache License 2.0"
)
