from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="firebotpy",
    version="4.15",
    license="MIT",
    description="Python library to connect to Firebots API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Craig Bailey",
    author_email="bailey_craig@me.com",
    url="https://github.com/whatupcraig/Firebotpy",
    download_url="https://github.com/whatupcraig/Firebotpy.git",
    keywords=["firebot", "api", "twitch"],
    install_requires=["requests"],
    packages=['firebotpy'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",  
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
)
