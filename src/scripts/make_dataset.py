from sz_utils import data_handler
import os
import numpy as np
import pandas as pd


def split_arrays(arr, num_windows, window_length) -> np.ndarray:
    """
    Splits each array in the input array into num_windows arrays of size (window_length//2, 22).
    Returns an array of shape (num_windows, window_length//2, 22).

    :param arr: array of shape (num_windows, window_length, 22)
    :type arr: np.ndarray
    :param num_windows: number of windows
    :type num_windows: int
    :param window_length: length of each window
    :type window_length: int
    :return: array of shape (num_windows, window_length//2, 22)
    :rtype: np.ndarray
    """
    # Split each array into two arrays of size (window_length//2, 22)
    split_arrays = np.mean(
        arr.reshape(-1, num_windows, 2, window_length // 2, 22), axis=2
    )

    return split_arrays


def make_dataset(resume: bool = False) -> None:
    """
    Make the dataset.
    For each patient we have a csv file with the windows.
    The windows are downsamples by 2.
    """
    patients = data_handler.get_patients()

    if resume:
        print("Resuming the process of making the dataset")
        # read patients that already have the windows
        patients_with_windows = set(
            [patient.split(".")[0] for patient in os.listdir("../data")]
        )
        # remove patients that already have the windows
        patients = set(patients) - patients_with_windows

        # also skip chb06 because it kills the kernel
        # patients = [patient for patient in patients if patient != "chb06"]  

    # read the csv file
    edf_files_with_features = pd.read_csv(
        "../edf_files_with_features.csv"
    ).values.tolist()

    # how many patients have the features we need
    patients_with_features = set(
        [patient for patient, edf_file in edf_files_with_features]
    )
    print(len(patients_with_features))

    edf_files_per_patient = {}
    for patient, edf_file in edf_files_with_features:
        if patient in edf_files_per_patient:
            edf_files_per_patient[patient] += 1
        else:
            edf_files_per_patient[patient] = 1

    print(edf_files_per_patient)

    # patient that not all edfs have the features we need
    patients_without_all_features = []
    # calculate using edf_files_with_features
    for patient in patients:
        edf_files = data_handler.get_patient_edf(patient)
        if len(edf_files) != edf_files_per_patient[patient]:
            patients_without_all_features.append(patient)

    print(patients_without_all_features)

    # patients that have all the features we need
    patients_with_all_features = set(patients) - set(patients_without_all_features)
    print(patients_with_all_features)

    # now we have the edf files with the features we need
    # and we know which edf files have seizures, we can split the data

    # we save the windows in a csv file, but before we subsample the data by 2
    # so we have 50% of the data
    features = data_handler.get_features()

    for patient in patients_with_all_features:
        try:
            preictal, no_preictal = data_handler.make_patient_windows(patient)
        except Exception as e:
            # write the patient that we could not make the windows and the error
            with open("../data/errors.txt", "a") as f:
                f.write(f"{patient}: {e}")
            continue
        # subsample the data (taking the mean of 2 consecutive values)
        # remember preictal is a ndarray
        preictal = split_arrays(preictal, preictal.shape[0], preictal.shape[1])
        if no_preictal.shape == (0,):  # if there are no no_preictal windows
            no_preictal = np.empty((0, 0, 0))
        else:
            no_preictal = split_arrays(
                no_preictal, no_preictal.shape[0], no_preictal.shape[1]
            )

        # preictal is a ndarray of shape (num_windows, window_length//2, 22)
        # no_preictal is a ndarray of shape (num_windows, window_length//2, 22)

        # reshape the arrayst to (num_windows*window_length//2, 22)
        preictal = preictal.reshape(-1, 22)
        no_preictal = no_preictal.reshape(-1, 22)

        # convert to dataframe
        preictal = pd.DataFrame(preictal, columns=features)
        no_preictal = pd.DataFrame(no_preictal, columns=features)

        # add the label
        preictal["label"] = 1
        no_preictal["label"] = 0

        # concatenate the dataframes
        df = pd.concat([preictal, no_preictal], ignore_index=True)

        # if folder does not exist, create it
        if not os.path.exists("../data"):
            os.makedirs("../data")

        # save the dataframe
        df.to_csv(f"../data/{patient}.csv", index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--resume",
        action="store_true",
        help="If true, resume the process of making the dataset",
    )

    args = parser.parse_args()

    make_dataset(args.resume)
