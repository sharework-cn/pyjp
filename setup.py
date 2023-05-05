from setuptools import setup

setup(
    name='pyjp',
    version='0.1',
    description='Calculate the self-running time of methods against JProfiler HTML reports',
    author='sharework',
    author_email='sharework@qq.com',
    url='https://github.com/sharework-cn/pyjp',
    packages=["pyjp"],
    install_requires=[
        'click',
        'cssselect',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'pyjp = pyjp.main:process'
        ]
    },
)
