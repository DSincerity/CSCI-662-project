
from inputters.strat import Inputter as strat
from inputters.vanilla import Inputter as vanilla
from inputters.emp_dialog_t5 import Inputter as emp_dialog_t5
from inputters.vanilla_1B import Inputter as vanilla_1B
from inputters.know_wo_strat import Inputter as know_wo_strat
from inputters.vanilla_t5 import Inputter as vanilla_t5

inputters = {
    'vanilla': vanilla,
    'vanilla_t5': vanilla_t5,
    'strat': strat,
    'emp_dialog_t5' : emp_dialog_t5,
    'vanilla_1B': vanilla_1B,
    'know_wo_strat': know_wo_strat
}



