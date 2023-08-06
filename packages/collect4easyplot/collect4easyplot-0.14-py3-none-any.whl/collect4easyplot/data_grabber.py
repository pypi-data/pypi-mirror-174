import os
import shutil
import pickle
from typing import Any

TMP_PATH = os.environ.get("TEMP")


def collect(data: Any, name: str):
    """ Dump data to file object in TEMP dir. Supposed to be used by EasyPlot """
    easy_plot_data_dir = os.path.join(TMP_PATH, "EasyPlotDataGrabber")
    if not os.path.exists(easy_plot_data_dir):
        os.makedirs(easy_plot_data_dir, exist_ok=True)
    file_path = os.path.join(easy_plot_data_dir, f"{name}.obj")
    file_obj = open(file_path, 'wb')
    pickle.dump(data, file_obj)
    file_obj.close()
    print(f"{name} collected successfully!")


def clear_all():
    easy_plot_data_dir = os.path.join(TMP_PATH, "EasyPlotDataGrabber")
    if not os.path.exists(easy_plot_data_dir):
        return
    for filename in os.listdir(easy_plot_data_dir):
        file_path = os.path.join(easy_plot_data_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
