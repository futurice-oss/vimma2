#! /usr/bin/env python3

import argparse
import os, os.path
import subprocess

import util


def parse_args():
    p = argparse.ArgumentParser(description='''Start Celery periodic task
        scheduler (beat)''')
    return p.parse_args()


if __name__ == '__main__':
    parse_args()

    env = dict(os.environ)
    env['DJANGO_SETTINGS_MODULE'] = util.DJANGO_SETTINGS_MODULE
    env['PYTHONPATH'] = util.VIMMASITE_PYTHONPATH

    # add ‘-f logfile’ to send the log to a file
    try:
        subprocess.check_call(['celery', '-A', 'vimma.celery:app', 'beat',
            '-l', 'info'], env=env)
    except KeyboardInterrupt:
        pass
