from models.strat_blenderbot_small import Model as strat_blenderbot_small
from models.vanilla_blenderbot_1B import Model as vanilla_blenderbot_1B
from models.vanilla_blenderbot_small import Model as vanilla_blenderbot_small
from models.emp_dialog_t5 import Model as emp_dialog_t5
from models.know_wo_strat_blenderbot_small import Model as know_wo_strat_blenderbot_small
from models.vanilla_t5 import Model as vanilla_t5
models = {
    'vanilla_t5': vanilla_t5,
    'vanilla_blenderbot_small': vanilla_blenderbot_small,
    'vanilla_blenderbot_1B': vanilla_blenderbot_1B,
    'strat_blenderbot_small': strat_blenderbot_small,
    'emp_dialog_t5': emp_dialog_t5,
    'know_wo_strat_blenderbot_small': know_wo_strat_blenderbot_small,
}
