from setuptools import setup

package_name = 'joystick_pub'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    # py_modules=[
    #     'joystick_pub',
    #     'inputs'
    # ],
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
            'joystick_pub = joystick_pub.joystick_pub:main',
        ],
    },
)
