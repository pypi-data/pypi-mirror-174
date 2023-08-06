from setuptools import setup, find_packages  # 这个包没有的可以pip一下

file_path = './README.md'

setup(
    name="palp",  # 这里是pip项目发布的名称
    version="0.0.1",  # 版本号，数值大的会优先被pip
    keywords=["palp"],  # 关键字
    description="一个 爬虫框架",  # 描述
    long_description=open(file_path, 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",  # 许可证

    author="郭一会儿",  # 作者
    author_email="1015295213@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]  # 这个项目依赖的第三方库
)
