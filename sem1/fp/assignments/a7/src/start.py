#
# This module is used to invoke the program's UI and start it. It should not contain a lot of code.
#

import ui
from tests import *

def start():
    test_all()
    ui.print_ui()

start()