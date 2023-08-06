from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='flask_markdown_to_html',#包名
    version='0.1.2',#版本
    description="可以在flask中查看markdown代码",#包简介
    long_description=long_description,
    long_description_content_type="text/markdown",
  #读取文件中介绍包的详细内容
    include_package_data=True,#是否允许上传资源文件
    author='zyzlaozhang2011',#作者
    author_email='zyzlaozhang2011@163.com',#作者邮件
    maintainer='zyzlaozhang2011',#维护者
    maintainer_email='zyzlaozhang2011@163.com',#维护者邮件
    license='MIT License',#协议
    url='https://github.com/zyzlaozhang/flask-markdown-to-html',#github或者自己的网站地址
    packages=find_packages(),#包的目录
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',#设置编写时的python版本
],
    python_requires='>=3.7',#设置python版本要求
    install_requires=['flask','markdown'],#安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },#设置命令行工具(可不使用就可以注释掉)
    
)