# visualizer using streamlit
from config import config

import streamlit as st
import pandas as pd
import mne
import os


def load_edf(edf_file: str) -> mne.io.edf.edf.RawEDF:
    """Load edf file and return a dataframe"""
    file = edf_file
    return mne.io.read_raw_edf(file)
    

def get_patients_folder() -> list[str]:
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
    """
    Get all the edf files in a patient folder
    """
    base_path = config['CHB_FOLDER_DIR']
    patient_path = os.path.join(base_path, patient)
    edf_files = [f for f in os.listdir(patient_path) if f.endswith('.edf')]
    return edf_files


def select_patient() -> str:
    option = st.sidebar.selectbox(
        'Select a patient',
        get_patients_folder())
    return option


def select_edf(patient) -> str:
    option = st.sidebar.selectbox(
        'Select an edf file',
        get_patient_edf(patient))
    return option


def get_edf_data(patient: str, edf: str) -> mne.io.edf.edf.RawEDF:
    base_path = config['CHB_FOLDER_DIR']
    patient_path = os.path.join(base_path, patient)
    edf_path = os.path.join(patient_path, edf)
    return load_edf(edf_path)


def select_view() -> str:
    option: str = st.sidebar.selectbox(
        'Select a view',
        ['Table', 'Graph', 'Spectrogram'])
    return option


def plot_spectrogram(edf: str) -> None:
    pass


def main_view(edf_data: mne.io.edf.edf.RawEDF) -> None:
    view: str = select_view()
    if view == 'Graph':
        pass
    elif view == 'Spectrogram':
        plot_spectrogram(edf_data)
    else:
        st.dataframe(edf_data.to_data_frame())


def main() -> None:
    st.set_page_config(page_title='Seizure Prediction', page_icon=':brain:')
    st.title("EEG Data Visualizer")

    st.sidebar.title("Select your EEG data")

    patient: str = select_patient()
    edf: str = select_edf(patient)
    edf_data: mne.io.edf.edf.RawEDF = get_edf_data(patient, edf)

    main_view(edf_data) 

    st.write()


if __name__ == "__main__":
    main()
    
    
