#!/usr/bin/python3
def make_print_to_file(path='./'):
    import sys
    import os
    import config_file as cfg_file
    import sys
    import datetime
 
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            # self.filename=filename
            # self.log = open(os.path.join(path, filename), "a", encoding='utf8')
        def write(self, message):
            filename = datetime.datetime.now().strftime('%Y%m%d')+'.log'
            self.log = open(os.path.join(path, filename), "a", encoding='utf8')
            if message == '\n':
                self.log.write(datetime.datetime.now().strftime('——————%H:%M:%S'))
            self.terminal.write(message)
            self.log.write(message)
            self.log.close()
        def flush(self):
            pass
 
    # fileName = datetime.datetime.now().strftime('%Y%m%d')
    # sys.stdout = Logger(fileName + '.log', path=path)
    sys.stdout = Logger(path=path)
