
from inputters.strat import Inputter as strat
from inputters.vanilla import Inputter as vanilla
from inputters.emp_dialog_t5 import Inputter as emp_dialog_t5

inputters = {
    'vanilla': vanilla,
    'strat': strat,
    'emp_dialog_t5' : emp_dialog_t5
}



