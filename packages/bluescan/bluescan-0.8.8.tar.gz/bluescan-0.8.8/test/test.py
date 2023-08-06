#!/usr/bin/env python

from bluescan.plugin import BluescanPluginManager

whl_path = '/home/x/OneDrive/Projects/bluescan/plugins/blueborne_cve_2017_0785_scanner/dist/blueborne_cve_2017_0785_scanner-0.0.1-py3-none-any.whl'
plugin_name = 'blueborne_cve_2017_0785_scanner'
# BluescanPluginManager.get_plugin_name_from_whl(whl_path)
BluescanPluginManager.install(whl_path)
# BluescanPluginManager.list()
# BluescanPluginManager.uninstall(plugin_name)
