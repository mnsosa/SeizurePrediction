"""This module is about the data extraction from the summary file and
the edf file.

The summary has the metadata of the dataset.
The summary is a txt file.

The most important function here is get_seizure_data.
"""

import os
import mne
import numpy as np
import pandas as pd
import random
from config import config
from typing import List, Tuple, Dict
from ast import literal_eval


def get_patients() -> List[str]:
    """
    Get all the patients folder.
    IT USES THE CONFIG.PY FILE.

    :return: list of patients
    :rtype: list[str]
    """
    path = config["CHB_FOLDER_DIR"]
    # list the patient in the folder
    # only list if the element it's an other folder
    patients = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return patients


def get_patient_edf(patient: str) -> List[str]:
    """Get all the edf files in a patient folder

    :param patient: the patient code (ex: chb01)
    :type patient: str
    :return: list of edf files
    :rtype: list[str]
    """
    base_path = config["CHB_FOLDER_DIR"]
    patient_path = os.path.join(base_path, patient)
    edf_files = [f for f in os.listdir(patient_path) if f.endswith(".edf")]
    return edf_files


def get_summary(patient: str) -> str:
    """Get the summary of the patient

    :param patient: the patient code (ex: chb01)
    :type patient: str
    :return: the summary of the patient
    :rtype: str
    """
    base_path = config["CHB_FOLDER_DIR"]
    patient_path = os.path.join(base_path, patient)
    summary_path = os.path.join(patient_path, f"{patient}-summary.txt")
    with open(summary_path, "r", encoding="utf-8") as file:
        summary: str = file.read()
    return summary


def get_edf_data(patient: str, edf: str) -> pd.DataFrame:
    """Read raw edf data and corrects the metadata using the summary file

    :param patient: the patient code (ex: chb01)
    :type patient: str
    :param edf: the edf file name
    :type edf: str
    :return: the raw edf data¿
    :rtype: pd.DataFrame
    """
    base_path = config["CHB_FOLDER_DIR"]
    patient_path = os.path.join(base_path, patient)
    edf_path = os.path.join(patient_path, edf)
    mne_data = mne.io.read_raw_edf(edf_path)
    return mne_data.to_data_frame()


def get_seizure_times(patient: str) -> List[Tuple[int, int]]:
    """Get the seizure times from the summary file.
    The seizure times are in seconds.

    Args:
        patient (str): the patient code (ex: chb01)

    Returns:
        list[tuple[int, int]]: list of tuples with the seizure start time and the seizure end time
    """
    summary = get_summary(patient)
    seizure_start_times = [
        line for line in summary.splitlines() if "Start" in line and "seconds" in line
    ]
    # split where the ":" is and get the last element
    # strip it and get the first element (the time) and convert it to int
    seizure_start_times = [
        int(line.split(":")[-1].strip().split(" ")[0]) for line in seizure_start_times
    ]

    seizure_end_times = [
        line for line in summary.splitlines() if "End" in line and "seconds" in line
    ]

    # split where the ":" is and get the last element
    # strip it and get the first element (the time) and convert it to int
    seizure_end_times = [
        int(line.split(":")[-1].strip().split(" ")[0]) for line in seizure_end_times
    ]

    seizure_times = list(zip(seizure_start_times, seizure_end_times))
    number_of_seizures = get_number_of_seizures(patient)
    number_of_seizures = list(number_of_seizures.values())
    indexes_gt_0 = [i for i, x in enumerate(number_of_seizures) if x > 0]
    number_of_seizures_gt_0 = [number_of_seizures[i] for i in indexes_gt_0]
    indexes_times = [i for i, _ in enumerate(seizure_times)]
    groups = []
    i = 0
    for i_gt_0 in number_of_seizures_gt_0:
        groups.append(indexes_times[i : i + i_gt_0])
        i += i_gt_0
    seizure_times_group = []
    for group in groups:
        seizure_times_group.append([seizure_times[i] for i in group])
    return seizure_times_group


def get_number_of_seizures(patient: str) -> Dict[str, int]:
    """Get the number of seizures for each file

    :param patient: The patient name
    :type patient: str
    :return: A dictionary with the file name as key and the number of seizures as value
    :rtype: dict[str, int]
    """
    summary = get_summary(patient)
    number_of_seizures = [
        line for line in summary.splitlines() if "Number of Seizures" in line
    ]
    file_names = [line for line in summary.splitlines() if "File Name" in line]
    file_names = [line.split(":")[-1].strip() for line in file_names]
    number_of_seizures = [
        int(line.split(":")[-1].strip().split(" ")[0]) for line in number_of_seizures
    ]
    file_names_and_seizures = dict(zip(file_names, number_of_seizures))
    return file_names_and_seizures


def get_seizure_data(patient: str) -> pd.DataFrame:
    """Get the seizure data for a patient

    :param patient: The patient name
    :type patient: str
    :return: A dataframe with the file names, number of seizures, start and end times
    :rtype: pd.DataFrame
    """
    file_names_and_seizures = get_number_of_seizures(patient)
    seizure_times = get_seizure_times(patient)
    df = pd.DataFrame(
        {
            "file_name": list(file_names_and_seizures.keys()),
            "number_of_seizures": list(file_names_and_seizures.values()),
        }
    )

    index_list = df[df["number_of_seizures"] > 0].index.tolist()
    for index in index_list:
        index_position = index_list.index(index)
        start_t = seizure_times[index_position]
        # convert start_t to a string
        start_t = str(start_t)
        df.loc[index, "start_end_times"] = start_t
    return df


def get_features() -> List[str]:
    return [
        "FP1-F7",
        "F7-T7",
        "T7-P7",
        "P7-O1",
        "FP1-F3",
        "F3-C3",
        "C3-P3",
        "P3-O1",
        "FP2-F4",
        "F4-C4",
        "C4-P4",
        "P4-O2",
        "FP2-F8",
        "F8-T8",
        "T8-P8-0",
        "P8-O2",
        "FZ-CZ",
        "CZ-PZ",
        "P7-T7",
        "T7-FT9",
        "FT9-FT10",
        "FT10-T8",
    ]


def make_patient_windows(patient: str) -> Tuple[np.ndarray, np.ndarray]:
    """Make preictal and not preictal samples.

    :param patient: patient id name (eg. chb01)
    :type patient: str
    :return: preictal and not preictal samples
    :rtype: Tuple[np.ndarray, np.ndarray]
    """
    features = get_features()

    # 1. Get edf files for patient
    # edf_files = get_patient_edf(patient)
    # 2. Get info about seizures
    seizures = get_seizure_data(patient)
    # 3. Split into the one with and without seizures
    seizures_with = seizures[seizures["number_of_seizures"] > 0]
    seizures_without = seizures[seizures["number_of_seizures"] == 0]
    # 4. For each file with seizures, get the seizure times
    seizure_times = []
    for edf_file in seizures_with["file_name"]:
        seizure_times.append(
            literal_eval(
                seizures_with[seizures_with["file_name"] == edf_file][
                    "start_end_times"
                ].values[0]
            )
        )
    # 5. Get the edf_files_names with seizures
    edf_files_with_seizures = seizures_with["file_name"].values
    # 6. For each seizure_times and edf_files_with_seizures, take 5 minutes (256*60*5) before the seizure
    # from the edf data
    seizure_samples = []
    for edf_file, seizure_time in zip(edf_files_with_seizures, seizure_times):
        edf_data = get_edf_data(patient, edf_file)
        edf_data = edf_data[features]
        first_seizure_time = seizure_time[0][0]
        first_seizure_time *= 256
        if first_seizure_time < 256 * 60 * 5:
            continue # skip seizures that are too close to the start of the file
        seizure_samples.append(
            edf_data[first_seizure_time - 256 * 60 * 5 : first_seizure_time]
        )
    # 7. Split data into 5 second windows
    seizure_windows = []
    for seizure_sample in seizure_samples:
        num_samples = seizure_sample.shape[0]
        samples_per_window = 256 * 5
        seizure_windows.append(
            np.array_split(seizure_sample, num_samples // samples_per_window)
        )
    # 8. No seizure samples
    # Get the edf_files_names without seizures
    edf_files_without_seizures = seizures_without["file_name"].values
    # 9. Randomly 7 edf files without seizures
    random.seed(42)
    try:
        edf_files_without_seizures = random.sample(
            list(edf_files_without_seizures), len(seizure_samples)
        )
    except ValueError:
        # if there are more seizures than no seizures, just use all the no seizure files
        pass
    # 10. For each edf_files_without_seizures, take 5 minutes (256*60*5) before the seizure
    # from the edf data
    no_seizure_samples = []
    for edf_file in edf_files_without_seizures:
        edf_data = get_edf_data(patient, edf_file)
        edf_data = edf_data[features]
        middle_time = edf_data.shape[0] // 2
        no_seizure_samples.append(edf_data[middle_time - 256 * 60 * 5 : middle_time])
    # 11. Split data into 5 second windows
    no_seizure_windows = []
    for no_seizure_sample in no_seizure_samples:
        num_samples = no_seizure_sample.shape[0]
        samples_per_window = 256 * 5
        no_seizure_windows.append(
            np.array_split(no_seizure_sample, num_samples // samples_per_window)
        )
    # 12. From (n, a, (b, c)) to (n*a, b, c)
    seizure_windows = np.array(seizure_windows)
    seizure_windows = np.concatenate(seizure_windows, axis=0)
    # 13. Same for no_seizure_windows
    no_seizure_windows = np.array(no_seizure_windows)
    try:
        no_seizure_windows = np.concatenate(no_seizure_windows, axis=0)
    except ValueError:
        # if there are no no seizure samples, return an empty array
        return seizure_windows, no_seizure_windows 
    return seizure_windows, no_seizure_windows
