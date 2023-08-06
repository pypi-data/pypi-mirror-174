import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # 包信息
    name="wudao",
    version="1.0.0",
    author="yufeng",
    author_email="yufeng.zhu@aminer.cn",
    license='MIT',
    description="超大规模中文预训练模型",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://maas.aminer.cn/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'requests',
        'pycryptodome'
    ],
    # 包搜集

)
