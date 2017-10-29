from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='task_tracker_api',
    packages=['task_tracker_api'],
    version='0.0.1',
    description='Task Tracker API',
    long_description=readme(),
    url='https://github.com/resurtm/task-tracker-api',
    download_url='https://github.com/resurtm/task-tracker-api/archive/v0.0.1.tar.gz',
    author='resurtm',
    author_email='resurtm@gmail.com',
    license='MIT',
    classifiers=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ]
)
