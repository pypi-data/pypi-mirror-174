from setuptools import setup, find_packages
import versioneer

setup(
    name="apwarrant",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python class to integrate Boto3's Cognito client so it is easy to login users. With SRP support.",
    long_description="README",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    author="ArcadiaPower",
    maintainer="ArcadiaPower",
    packages=find_packages(),
    url="https://github.com/ArcadiaPower/warrant",
    license="Apache License 2.0",
    install_requires=[
        "boto3>=1.4.3",
        "envs>=0.3.0",
        "python-jose-cryptodome>=1.3.2",
        "requests>=2.13.0",
    ],
    include_package_data=True,
    zip_safe=True,
)
