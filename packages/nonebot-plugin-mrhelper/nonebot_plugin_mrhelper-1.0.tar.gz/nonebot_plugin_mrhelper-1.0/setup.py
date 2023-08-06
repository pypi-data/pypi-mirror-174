import setuptools

setuptools.setup(
    name="nonebot_plugin_mrhelper",
    version="1.0",
    author="yanyao",
    author_email="",
    description="基于nonebot2的movie-robot小助手",
    long_description="基于nonebot2的movie-robot小助手\n详情请去 https://github.com/yanyao2333/nonebot-plugin-mrhelper 查看",
    long_description_content_type="text/markdown",
    install_requires=['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0','nonebot2>=2.0.0-beta.4,<3.0.0'],
    url="https://github.com/yanyao2333/nonebot-plugin-mrhelper",
    packages=setuptools.find_packages(),
    python_requires='>=3.8,<4.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)