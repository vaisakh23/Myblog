'''
in production server .env needs to be loaded
manually | flask server loads it for us
'''
#from dotenv import load_dotenv

#load_dotenv('.env')

from app import create_app, db
from app.models import User, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

'''
After adding the shell context processor function 
you can work with database entities
(or items returned in the function) without
having to import them
'''
