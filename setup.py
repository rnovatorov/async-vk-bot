from setuptools import setup, find_packages


setup(
    name='async-vk-bot',
    version='0.9.4',
    description='Async VK bot builder',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Suenweek/async-vk-bot',
    author='Roman Novatorov',
    author_email='roman.novatorov@gmail.com',
    install_requires=['async-vk-api', 'async_generator']
)
