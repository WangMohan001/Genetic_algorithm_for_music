from setuptools import setup, find_packages

setup(
    name="genetic_algorithm_for_music",  # 包名
    version="0.1",
    packages=find_packages(),  # 自动查找所有包
    install_requires=[],  # 外部依赖包
    test_suite='tests',   # 测试套件目录
    include_package_data=True,  # 包含静态文件或数据文件
)