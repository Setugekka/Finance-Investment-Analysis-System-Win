import os
from flask_script import Manager, Server
from Api import create_app


env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())
manager = Manager(app)
manager.add_command("server", Server())

if __name__ == "__main__":
    manager.run()
