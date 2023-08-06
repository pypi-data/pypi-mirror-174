# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysolarfocus', 'pysolarfocus.components', 'pysolarfocus.components.base']

package_data = \
{'': ['*']}

install_requires = \
['pymodbus==2.5.3']

setup_kwargs = {
    'name': 'pysolarfocus',
    'version': '0.99.0',
    'description': 'Unofficial, local Solarfocus client',
    'long_description': "# pysolarfocus: Python Client for Solarfocus eco<sup>_manager-touch_</sup>\n\n## What's Supported \n\n### Software Version\n\nThis integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `21.040`.\n\n### Solarfocus Components\n\n| Components | Supported |\n|---|---|\n| Heating Circuits (_Heizkreis_)| :white_check_mark: |\n| Buffers (_Puffer_) | :white_check_mark: |\n| Solar (_Solar_)| :x:|\n| Boilers (_Boiler_) | :white_check_mark: |\n| Heatpump (_Wärmepumpe_) | :white_check_mark: |\n| Biomassboiler (_Kessel_) | :white_check_mark: | \n\n_Note: Different components or heating systems could be supported in the future_\n\n## Usage\n\n```python\nfrom pysolarfocus import SolarfocusAPI,Systems\n\n# Create the Solarfocus API client\nsolarfocus = SolarfocusAPI(ip=[Your-IP],system=Systems.Vampair)\n# Connect to the heating system\nsolarfocus.connect() \n# Fetch the values\nsolarfocus.update()\n\n# Print the values\nprint(solarfocus.buffers[0])\nprint(solarfocus.heating_circuit[0])\n```\n\n### Handling multiple components e.g. heating circuits\n_Solarfocus systems allow the use of multiple heating circuits, buffers and boilers. The api can be configured to interact with multiple components._\n\n```python \n\n# Create the Solarfocus API client with 2 Heating Circuits\nsolarfocus = SolarfocusAPI(ip=[Your-IP],heating_circuit_count=2,system=Systems.Vampair)\n# Connect to the heating system\nsolarfocus.connect()\n\n# Update all heating circuits\nsolarfocus.update_heating()\n\n# Update only the first heating circuit\nsolarfocus.heating_circuits[0].update()\n# Print the first heating circuit\nprint(solarfocus.heating_circuits[0])\n\n# Set the temperature of the first heating circuit to 30°C\nsolarfocus.heating_circuits[0].indoor_temperatur_external.set_unscaled_value(30)\n# Write the value to the heating system\nsolarfocus.heating_circuits[0].indoor_temperatur_external.commit()",
    'author': 'Jeroen Laverman',
    'author_email': 'jjlaverman@web.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lavermanjj/pysolarfocus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
