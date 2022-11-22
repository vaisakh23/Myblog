import os
import secrets
from PIL import Image
from . import app

def save_profile_pic(picture):
    # create file name
    random_hex = secrets.token_hex(8)
    _, file_extention = os.path.splitext(picture.filename)
    picture_file_name = random_hex + file_extention
    picture_saving_path = os.path.join(app.root_path, 'static/profile_pics', picture_file_name)
    # resize and save picture
    reduce_size_to = (125, 125)
    img = Image.open(picture)
    img.thumbnail(reduce_size_to)
    img.save(picture_saving_path)
    
    return picture_file_name
