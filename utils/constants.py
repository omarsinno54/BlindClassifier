from configparser import ConfigParser

import sys
import os

root_dir = os.path.dirname(os.path.dirname(__file__))
conf_dir = os.path.join(root_dir, 'conf/config.conf')

sys.path.insert(0, root_dir)

parser = ConfigParser()
parser.read(conf_dir)

ORGANIZATION_ID = parser.get(section='ids', option='ORGANIZATION_ID')
API_KEY = parser.get(section='api_keys', option='OPEN_AI_API_KEY')
PROJECT_ID = parser.get(section='ids', option='PROJECT_ID')