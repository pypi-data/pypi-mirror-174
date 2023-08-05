import os
import sys
import platform

from django.core.management import execute_from_command_line




def main():
    if len(sys.argv) == 2:
        listen = sys.argv[1]
    else:
        listen = '127.0.0.1:8000'
    if platform.system() != 'Windows':
        sys.argv = [
            '',
            '-b',
            listen,
            'APTRS.wsgi:application',
            '--workers=1',
            '--threads=10',
            '--timeout=5600',
        ]
        from gunicorn.app.wsgiapp import run
        run()
    else:
        from waitress import serve
        from .APTRS import wsgi
        serve(
            wsgi.application,
            listen=listen,
            threads=10,
            channel_timeout=5600)