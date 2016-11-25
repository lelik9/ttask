try:
    import configparser
except ImportError:
    from six.moves import configparser

from db_func import db
from models import Kpi, Results
from pysnmp.hlapi import *


class Work:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read('conf.ini')
        self.file_start = self.config.getint('APP', 'file_start')
        self.db_start = self.config.getint('APP', 'db_start')

    def get_data_from_file(self):
        with open(self.filename, 'r') as f:
            f.seek(self.file_start)

            for line in f:
                res = line.rstrip().split(',')
                print('name {}: value {}'.format(res[0], res[1]))
                self.write_to_db(res[0], res[1])

            self.file_start = f.tell()
            self.write_conf('file_start', str(self.file_start))

    def get_data_from_db(self):
        query = db.session.query(Kpi).filter(Kpi.id > self.db_start).all()

        if query:
            for res in query:
                self.write_to_db(res.name, res.value)
            self.db_start = res.id
            self.write_conf('db_start', str(self.db_start))

    def get_data_from_snmp(self, ip='10.10.9.11', port=161):
        with open(self.filename, 'r') as f:
            for line in f:
                res = line.rstrip().split(',')
                transport = UdpTransportTarget((ip, port), timeout=1, retries=5, tagList='')

                g = getCmd(SnmpEngine(),
                           CommunityData('public'),
                           transport,
                           ContextData(),
                           ObjectType(ObjectIdentity(res[0], res[1], 0)))

                result = next(g)[-1]

                for r in result:
                    print(res[1], r[-1].prettyPrint())
                    self.write_to_db(res[1], r[-1].prettyPrint())

    def write_conf(self, position, value):
        print(type(position))
        self.config.set('APP', position, value)
        with open('conf.ini', 'w') as configfile:
            self.config.write(configfile)

    @staticmethod
    def write_to_db(name, value):
        result = Results(name=name,
                         value=value)
        db.add(result)
