import urllib
import requests
import json
import datetime

class markdown(object):
    """Data from source provider"""

    def get_legacy_standings(dict_standings):
        legacy_standings = 'WEST|||EAST|||\n:---:|:---:|:---:|:---:|:---:|:---:\n**TEAM**|*W/L*|*GB*|**TEAM**|*W/L*|*GB*\n'

        for i in range(0,15):
            standings = dict_standings[i+1]
            if i < 8:
                legacy_standings = legacy_standings + standings['conf_rank'] + ' [](/' + standings['west_name'] + ')|' + standings['west_record'] + '|' + standings['west_gb_conf'] + '|' + standings['conf_rank'] + ' [](/' + standings['east_name'] + ')|' + standings['east_record'] + '|' + standings['east_gb_conf'] + '\n'
            else:
                legacy_standings = legacy_standings + '[](/' + standings['west_name'] + ')|' + standings['west_record'] + '|' + standings['west_gb_conf'] + '|[](/' + standings['east_name'] + ')|' + standings['east_record'] + '|' + standings['east_gb_conf'] + '\n'

        return legacy_standings

    def get_widget_standings(dict_standings):
        widget_standings = '- \n - \n     - west\n     - W - L\n     - GB\n     - GB\n     - W - L\n     - east\n\n'
        
        for i in range(0,15):
            standings = dict_standings[i+1]
            widget_standings = widget_standings + '- \n - \n     - [](/' + standings['west_name'] + ')\n     - ' + standings['west_gb_conf'] + '\n     - ' + standings['west_record'] + '\n - ' + standings['conf_rank'] + '\n - [](/#)\n     - [](/' + standings['east_name'] + ')\n     - ' + standings['east_gb_conf'] + '\n     - ' + standings['east_record'] + '\n\n'

        return widget_standings
