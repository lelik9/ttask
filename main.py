import argparse
import sched
import sys
import time

from work import Work
from db_func import init_db


def periodic_scheduler(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic_scheduler,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(add_help=True)

        parser.add_argument('-m', '--mode', action="store", help='Input data mode (snmp, file, db)')
        parser.add_argument('-t', '--time', type=int, action="store", help='Timeout in seconds')
        parser.add_argument('-ip', '--ip-address', action="store", help='IP address of node')
        parser.add_argument('-p', '--port', type=int, action="store", help='SNMP port')
        parser.add_argument('-f', '--file', action="store", help='''File name.
                                                                    For "snmp" mode, file with OID.
                                                                    For "file" mode - data file''')

        args = parser.parse_args()

        mode = args.mode
        file_name = args.file
        t = args.time
        ip = args.ip_address
        port = args.port

        scheduler = sched.scheduler(time.time, time.sleep)
        work = Work(file_name)
        init_db()

        if mode == 'db':
            print('db')
            periodic_scheduler(scheduler, t, work.get_data_from_db)
        elif mode == 'file':
            print('file', file_name)
            periodic_scheduler(scheduler, t, work.get_data_from_file)
        elif mode == 'snmp':
            print('snmp', file_name)
            periodic_scheduler(scheduler, t, work.get_data_from_snmp, (ip, port))

        scheduler.run()

    except KeyboardInterrupt:
        sys.exit(1)
