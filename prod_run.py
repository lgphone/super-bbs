import sys
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

from super_bbs.app import create_app

app = create_app()

# run host port
host = '0.0.0.0'
port = 5000

if len(sys.argv) >= 2:
    try:
        port = int(sys.argv[1])
    except Exception:
        pass

if __name__ == '__main__':
    print(f" * Start prod app on: {host}:{port}")
    print(f" * Debug Mode: {app.config.get('DEBUG')}")
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()
