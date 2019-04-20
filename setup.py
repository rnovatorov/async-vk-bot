from setuptools import setup, find_packages


setup(
    name='async-vk-bot',
    version='0.9.5',
    description='Async VK bot builder',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Suenweek/async-vk-bot',
    author='Roman Novatorov',
    author_email='roman.novatorov@gmail.com',
    # TODO: Bump version when asks gets session instantiation fixed:
    #   https://github.com/theelous3/asks/pull/120
    install_requires=['async-vk-api==0.6.1', 'async_generator']
)
