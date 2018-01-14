import configparser
import os
home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_file = os.path.join(home,'etc','baton.conf')

conf = configparser.ConfigParser()
conf.read(conf_file)
if __name__ == "__main__" :
    print(conf.get('protocol','openflow'))
    print(conf.getint('protocol','openflow'))