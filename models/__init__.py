
from models.strat_blenderbot_small import Model as strat_blenderbot_small
from models.vanilla_blenderbot_small import Model as vanilla_blenderbot_small
from models.emp_dialog_t5 import Model as emp_dialog_t5


models = {

    'vanilla_blenderbot_small': vanilla_blenderbot_small,
    'strat_blenderbot_small': strat_blenderbot_small,
    'emp_dialog_t5': emp_dialog_t5,
}
