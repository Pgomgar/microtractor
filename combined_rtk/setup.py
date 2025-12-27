from setuptools import find_packages, setup
import glob
import os

package_name = 'combined_rtk'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), ['package.xml', *glob.glob('launch/*')]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pgomgar',
    maintainer_email='pgomgar@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
