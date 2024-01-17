import setuptools

setuptools.setup(
    name="parseUrl",
    version="0.0.1",
    author="tuanla-i2023",
    author_email="leanhtuan200222@gmail.com",
    description="parseUrl url request",
    long_description="Parse url request with parameter as page, pageSize, order_by, filter",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    py_modules=['parseUrl'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)