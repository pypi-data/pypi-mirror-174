import setuptools

with open("README.md", "r") as fh:
	description = fh.read()

setuptools.setup(
	name="TimeShut",
	version="0.0.1",
	author="Savvidaios",
	author_email="charissavvidis4@gmail.com",
	packages=["TestPackage"],
	description="A sample test package",
	long_description=description,
	long_description_content_type="text/markdown",
	url="https://github.com/savvidis4/timeshutt.git",
	license='MIT',
	python_requires='>=3.8',
	install_requires=[]
)
