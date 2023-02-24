"""From the raw dataset (from PhysioNet), we create a dataset for this project. 

The dataset is a CSV file with the following columns:
['time', 'FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 
'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2', 'FZ-CZ', 
'CZ-PZ', 'P7-T7', 'T7-FT9', 'FT9-FT10', 'FT10-T8']

These columns are selected from the raw dataset based on the following criteria:

    - Not all patients have the same number of channels. These channels were selected because 
    they are present in the majority of patients and provide crucial information.
"""
import os
import time
from tqdm import tqdm
from sz_utils import data_handler


def make_dataset():
    # For the e.g. patient chb04
    patient = "chb04"
    # Get edfs from the patient
    edfs = data_handler.get_patient_edf(patient)

    # create "data" folder if it doesn't exist
    if not os.path.exists("../../data"):
        print("Making data folder")
        os.makedirs("../../data")

    t0 = time.time()
    # Read, subsampling and save the data as a csv
    for edf in tqdm(edfs):
        data = data_handler.get_edf_data(patient, edf)
        path = f"../../data/{patient}_{edf}.csv"
        # check if the file already exists
        if os.path.exists(path):
            print(f"{path} already exists")
            continue
        try:
            # save the data
            data.to_csv(path)
        except Exception as e:
            # if fails, delete csv file
            print(f"Error saving {path}: {e}")
            os.remove(path)
            return
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            os.remove(path)
            return

        print(f"Saved {edf} from {patient}")

    print(f"Time elapsed: {time.time() - t0}")

if __name__ == "__main__":
    make_dataset()