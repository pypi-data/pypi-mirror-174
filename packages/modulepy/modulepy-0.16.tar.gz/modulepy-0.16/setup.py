from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="modulepy",
    version="0.16",
    description="module framework",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/modulepy",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=["loguru"],
    keywords="modularity modules",
    packages=find_packages(),
    long_description_content_type="text/markdown"
)
