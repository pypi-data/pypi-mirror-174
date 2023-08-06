import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='zenpass',
    packages=setuptools.find_packages(),
    version='1.0.2',
    license='Apache License, Version 2.0',
    description='To generate random and strong passwords.',
    author='srg',
    author_email='srg.code@pm.me',
    url='https://github.com/codesrg/zenpass',
    download_url='https://github.com/codesrg/zenpass/releases',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    requires=["pyperclip"],
    entry_points={'console_scripts': ['zenpass=zenpass.__main__:main']
                  },
    python_requires='>=3.6',
)
