import yaml

with open('../config.yml') as f:
    config = yaml.safe_load(f)


class Constants(object):
    ebay_app_name = config['EBAY-SECURITY-APPNAME']
