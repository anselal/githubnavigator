import sys

from app import app
from flask_script import Manager, Server
from flask_debugtoolbar import DebugToolbarExtension

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    toolbar = DebugToolbarExtension(app)
    # app.run(host='127.0.0.1', port=8888)
    server = Server(host='127.0.0.1', port=8888)
    manager = Manager(app)
    manager.add_command("runserver", server)
    manager.run()
