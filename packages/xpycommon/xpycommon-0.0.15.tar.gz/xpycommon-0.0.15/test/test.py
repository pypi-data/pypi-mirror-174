#!/usr/bin/env python
import sys


if sys.argv[1] == 'plugin':
    from xpycommon.plugin import PluginManager
    whl_path = '/home/x/OneDrive/Projects/bluescan/plugins/blueborne_cve_2017_0785_scanner/dist/blueborne_cve_2017_0785_scanner-0.0.1-py3-none-any.whl'
    PluginManager.get_plugin_name_from_whl(whl_path)
    PluginManager.install(whl_path)

from xpycommon.common import upgrade
# upgrade()
