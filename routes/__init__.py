from . import confirm_handlers, handlers, template_handler
from .db_connector import create_table
import os

labelers = [confirm_handlers.bl,template_handler.bl, handlers.bl]

if not os.path.isdir(f"archive") or not os.path.isdir(f"attachments"):
    os.mkdir("archive")
    os.mkdir("attachments")


create_table()
