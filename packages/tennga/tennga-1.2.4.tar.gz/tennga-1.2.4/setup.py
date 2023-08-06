import setuptools

with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tennga",  # 模块名称，也就是主文件夹名字
    version="1.2.4",  # 当前版本
    author="肥希的肥猫",  # 作者
    author_email="281001460@qq.com",  # 作者邮箱
    description="一个实现简易,使用简易的源管理器",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://github.com/shinoairisu/tennga",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据（更多的描述）
    classifiers=[
        # "Environment :: Web Environment",
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.6',
        # 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        # 'Topic :: NLP',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    # 依赖模块
    install_requires=[
        "requests"
        ],
    # python版本
    python_requires=">=3",
)