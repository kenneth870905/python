def make_print_to_file(path='./'):
    import sys
    import os
    import config_file as cfg_file
    import sys
    import datetime
 
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            self.log = open(os.path.join(path, filename), "a", encoding='utf8',)
        def write(self, message):
            if message == '\n':
                self.log.write(datetime.datetime.now().strftime('——————%H:%M:%S'))
            self.terminal.write(message)
            self.log.write(message)
        def flush(self):
            pass
 
    fileName = datetime.datetime.now().strftime('%Y%m%d')
    sys.stdout = Logger(fileName + '.log', path=path)
