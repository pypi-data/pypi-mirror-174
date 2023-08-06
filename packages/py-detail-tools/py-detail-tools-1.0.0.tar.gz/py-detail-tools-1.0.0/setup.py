
from setuptools import setup,find_packages
setup(
    name='py-detail-tools',
    version='1.0.0',
    author_email='xiaoyaojianxians@163.com',
    maintainer='robin',
    maintainer_email='xiaoyaojianxians@163.com',
    url='https://pypi.org/manage/account/',
    description='这是一个处理字符串小工具',
    long_description='这是一个处理字符串小工具,后续会不断更新叠加各种字符串处理功能',
    keywords=['字符串','字符处理','正则过滤表情字符','表情字符'],
    packages=find_packages(),
    install_requires=['pyenchant']

)