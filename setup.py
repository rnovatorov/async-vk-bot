from setuptools import setup

setup(
    name='async-vk-bot',
    version='0.0.1',
    description='Async VK bot builder',
    py_modules=['async_vk_bot'],
    url='https://github.com/Suenweek/async-vk-bot',
    author='Roman Novatorov',
    author_email='roman.novatorov@gmail.com',
    install_requires=['trio', 'async-vk-api'],
    dependency_links=['https://github.com/Suenweek/async-vk-api#egg=async-vk-api']
)
