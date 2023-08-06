import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="RecruitPlotEasy",
	version="3.0",
	author="Kenji Gerhardt",
	author_email="kenji.gerhardt@gmail.com",
	description="A tool for visualizing the ",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	include_package_data=True,
	python_requires='>=3',
	install_requires=[
		'numpy',
		'pyrodigal',
		'plotly',
	],
	entry_points={
		"console_scripts": [
			"rpe=rpe2_main:main",
			"recruitploteasy=rpe2_main:main",
		]
	}
)

