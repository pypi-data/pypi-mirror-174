from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description = f.read()

# Must be full path for build to find
with open('C:\\Users\\henri\\github\\chromepilot\\requirements.txt') as f:
    requirements = f.read()

setup(
    name='chromepilot',
    version='0.0.5',
    author='Henrique do Val',
    author_email='henrique.val@hotmail.com',
    description='Chromedriver download manager and imports shortcuts.',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HenriquedoVal/chromepilot',
    packages=find_packages(),
    package_data={'': ['pilot.toml']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'chromepilot = chromepilot.cli:main'
        ]},
    install_requires=requirements,
    python_requires='>=3.8'
)
