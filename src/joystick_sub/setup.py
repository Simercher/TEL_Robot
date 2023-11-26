from setuptools import setup

package_name = 'joystick_sub'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aiclub',
    maintainer_email='Simercher@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joystick_sub = joystick_sub.joystick_sub:main',
            'gyrosensor = joystick_sub.gyrosensor:main',
        ],
    },
)
