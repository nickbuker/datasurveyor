import pandas as pd
import numpy as np


sample_dict = {
    "id": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    "name": ('Nick', 'Gina', 'Rob', 'Adam', 'Hanna', 'Susan', 'Quentin', 'Caitlyn', 'Matt', 'Nick'),
    "state": ('WA', 'OR', 'WA', 'ID', 'WA', 'Null', 'WA', 'ID', 'WA', 'WA'),
    "app_inst": (True, True, False, True, True, False, True, True, True, True),
    "lylty": (0, 1, 0, 1, 1, 0, 1, 0, 1, 0),
    "spend": (0.0, np.NaN, 10.0, 150.0, 12.0, 0.0, np.NaN, 8.0, 50.0, -10.0),
}


sample_df = pd.DataFrame.from_dict(sample_dict)
