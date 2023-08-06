# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hass_mqtt_devices', 'hass_mqtt_devices.cli']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0', 'pyaml>=21.10.1,<22.0.0']

entry_points = \
{'console_scripts': ['ham-create-binary-sensor = '
                     'hass_mqtt_devices.cli.sensors:create_binary_sensor']}

setup_kwargs = {
    'name': 'hass-mqtt-devices',
    'version': '0.1.0',
    'description': '',
    'long_description': '# hass-mqtt-devices\n\nA python 3 module that takes advantage of Home Assistant\'s MQTT discovery\nprotocol to create sensors without having to define anything on the HA side.\n\n## Supported Types\n\n### Binary Sensors\n\n#### Usage\n\n```py\nfrom hass_mqtt_devices.sensors import BinarySensor\n\n# Create a settings dictionary\n#\n# Mandatory Keys:\n#  mqtt_server\n#  mqtt_prefix - defaults to homeassistant\n#  mqtt_user\n#  mqtt_password\n#  device_id\n#  device_name\n#  device_class\n#\n# Optional Keys:\n#  payload_off\n#  payload_on\n#  unique_id\n\nconfigd = {\n    "mqtt_server": "mqtt.example.com",\n    "mqtt_prefix": "homeassistant",\n    "mqtt_user": "mqtt_user",\n    "mqtt_password": "mqtt_password",\n    "device_id": "device_id",\n    "device_name":"MySensor",\n    "device_class":"motion",\n}\nmysensor = BinarySensor(settings=configd)\nmysensor.on()\nmysensor.off()\n\n```\n\n## Scripts Provided\n\nhass_mqtt_devices creates the following helper scripts you can use in your own shell scripts.\n\n- `ham-create-binary-sensor` - Lets you create a binary sensor and set its state',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
