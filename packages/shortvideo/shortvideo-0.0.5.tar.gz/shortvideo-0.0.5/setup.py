from setuptools import setup

packages = ["svwork"]

requires = [
    "requests==2.28.1",
    "requests_toolbelt==0.9.1"
]


setup(
    name='shortvideo',  # 包名称
    version='0.0.5',  # 包版本
    description='',  # 包详细描述
    long_description='https://www.shortvideo.work',   # 长描述，通常是readme，打包到PiPy需要
    author='netfere',  # 作者名称
    author_email='netfere@gmail.com',  # 作者邮箱
    url='https://www.shortvideo.work',   # 项目官网
    packages=packages,    # 项目需要的包
    python_requires=">=3.7",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[    # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    entry_points={
        'console_scripts':[
            'shortvideo = svwork.main:main'
        ]
    },
)