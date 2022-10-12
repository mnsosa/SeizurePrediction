####################################################################################################
# The summary has the metadata of the dataset.
# The summary is a txt file.
####################################################################################################
from config import config
import mne
import os


def get_patients() -> list[str]:
    """
    Get all the patients folder. 
    IT USES THE CONFIG.PY FILE.
    """
    path = config['CHB_FOLDER_DIR']
    # list the patient in the folder
    # only list if the element it's an other folder
    patients = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return patients


def get_patient_edf(patient: str) -> list[str]:
    """Get all the edf files in a patient folder"""
    base_path = config['CHB_FOLDER_DIR']
    patient_path = os.path.join(base_path, patient)
    edf_files = [f for f in os.listdir(patient_path) if f.endswith('.edf')]
    return edf_files


def get_summary(patient: str) -> list[str]:
    """Get the summary of the patient"""
    base_path = config['CHB_FOLDER_DIR']
    patient_path = os.path.join(base_path, patient)
    summary_path = os.path.join(patient_path, f'{patient}-summary.txt')
    with open(summary_path, 'r') as f:
        summary = f.read()
    return summary


def get_edf_data(patient: str, edf: str) -> mne.io.edf.edf.RawEDF:
    """Read raw edf data and corrects the metadata using the summary file"""
    base_path = config['CHB_FOLDER_DIR']
    patient_path = os.path.join(base_path, patient)
    edf_path = os.path.join(patient_path, edf)
    mne_data = mne.io.read_raw_edf(edf_path)
    summary = get_summary(patient)
    return mne_data