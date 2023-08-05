# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_chatops',
 'nautobot_chatops.api',
 'nautobot_chatops.api.views',
 'nautobot_chatops.dispatchers',
 'nautobot_chatops.management.commands',
 'nautobot_chatops.migrations',
 'nautobot_chatops.sockets',
 'nautobot_chatops.tests',
 'nautobot_chatops.tests.workers',
 'nautobot_chatops.workers']

package_data = \
{'': ['*'],
 'nautobot_chatops': ['static/nautobot/*',
                      'static/nautobot_chatops/docs/*',
                      'static/nautobot_chatops/docs/admin/*',
                      'static/nautobot_chatops/docs/admin/install/*',
                      'static/nautobot_chatops/docs/admin/release_notes/*',
                      'static/nautobot_chatops/docs/assets/*',
                      'static/nautobot_chatops/docs/assets/images/*',
                      'static/nautobot_chatops/docs/assets/javascripts/*',
                      'static/nautobot_chatops/docs/assets/javascripts/lunr/*',
                      'static/nautobot_chatops/docs/assets/javascripts/lunr/min/*',
                      'static/nautobot_chatops/docs/assets/javascripts/workers/*',
                      'static/nautobot_chatops/docs/assets/overrides/partials/*',
                      'static/nautobot_chatops/docs/assets/stylesheets/*',
                      'static/nautobot_chatops/docs/dev/*',
                      'static/nautobot_chatops/docs/dev/code_reference/*',
                      'static/nautobot_chatops/docs/images/*',
                      'static/nautobot_chatops/docs/search/*',
                      'static/nautobot_chatops/docs/user/*',
                      'templates/nautobot/*']}

install_requires = \
['Markdown!=3.3.5',
 'PyJWT>=2.1.0,<3.0.0',
 'aiodns>=1.0,<2.0',
 'aiohttp>=3.7.3,<4.0.0',
 'asgiref>=3.4.1,<4.0.0',
 'nautobot-capacity-metrics',
 'nautobot>=1.2.0,<2.0.0',
 'slack-sdk>=3.4.2,<4.0.0',
 'texttable>=1.6.2,<2.0.0',
 'webexteamssdk>=1.3,<2.0']

entry_points = \
{'nautobot.workers': ['clear = nautobot_chatops.workers.clear:clear',
                      'nautobot = nautobot_chatops.workers.nautobot:nautobot']}

setup_kwargs = {
    'name': 'nautobot-chatops',
    'version': '1.10.0',
    'description': 'A plugin providing chatbot capabilities for Nautobot',
    'long_description': '# Nautobot ChatOps\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/nautobot/nautobot-plugin-chatops/develop/docs/assets/icon-ChatOps.png" alt="ChatOps Logo" class="logo" height="200px">\n  <br>\n  <a href="https://github.com/nautobot/nautobot-plugin-chatops/actions"><img src="https://github.com/nautobot/nautobot-plugin-chatops/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n  <a href="https://docs.nautobot.com/projects/chatops/en/latest"><img src="https://readthedocs.org/projects/nautobot-plugin-chatops/badge/"></a>\n  <a href="https://pypi.org/project/nautobot-chatops/"><img src="https://img.shields.io/pypi/v/nautobot-chatops"></a>\n  <a href="https://pypi.org/project/nautobot-chatops/"><img src="https://img.shields.io/pypi/dm/nautobot-chatops"></a>\n  <br>\n  A multi-platform ChatOps bot App for <a href="https://github.com/nautobot/nautobot">Nautobot</a>.\n</p>\n\n- Support for multiple chat platforms (currently Slack, Microsoft Teams, Mattermost, and WebEx)\n- Write a command once and run it on every supported platform, including rich content formatting\n- Extensible - other Nautobot plugins can provide additional commands which will be dynamically discovered.\n- Automatic generation of basic help menus (accessed via `help`, `/command help`, or `/command sub-command help`)\n- Metrics of command usage via the `nautobot_capacity_metrics` plugin.\n\n## Documentation\n\nFull web-based HTML documentation for this app can be found over on the [Nautobot Docs](https://docs.nautobot.com/projects/chatops/en/latest/) website:\n\n- [User Guide](https://docs.nautobot.com/projects/chatops/en/latest/user/app_overview/) - Overview, Using the App, Getting Started\n- [Administrator Guide](https://docs.nautobot.com/projects/chatops/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.\n- [Developer Guide](https://docs.nautobot.com/projects/chatops/en/latest/dev/dev_contributing/) - Extending the App, Code Reference, Contribution Guide.\n- [Release Notes / Changelog](https://docs.nautobot.com/projects/chatops/en/latest/admin/release_notes/)\n- [Frequently Asked Questions](https://docs.nautobot.com/projects/chatops/en/latest/user/app_faq/)\n\n## Try it Out\n\nInterested to see Nautobot ChatOps in action?  It\'s currently setup on the [Demo Instance](https://demo.nautobot.com/) and integrated into [NTC Slack](https://slack.networktocode.com).  You can sign up for that Slack workspace and join the `#nautobot-chat` channel to understand what this bot can do and try it for yourself.  You can try these exact chat commands and many more:\n\n### Command: `/nautobot`\n\n![image](https://user-images.githubusercontent.com/6332586/118281576-5db4e980-b49b-11eb-8574-1332ed4b9757.png)\n\n### Command: `/nautobot get-devices`\n\n![image](https://user-images.githubusercontent.com/6332586/118281772-95239600-b49b-11eb-9c79-e2040dc4a982.png)\n\n### Command: `/nautobot get-interface-connections`\n\n![image](https://user-images.githubusercontent.com/6332586/118281976-ca2fe880-b49b-11eb-87ad-2a41eaa168ed.png)\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/chatops/en/latest/user/app_faq/) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #nautobot).\nSign up [here](https://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nautobot/nautobot-plugin-chatops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
