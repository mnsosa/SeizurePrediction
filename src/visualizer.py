"""A visualizer using streamlit for easy implementation of the project

This module is the main module of the visualizer. It uses the streamlit library
to create a web app that can be used to visualize some data. You can select a
patient and a edf file and then you can visualize the data in different ways.

This module uses the data_handler module to get the data from the files.
"""

import pandas as pd
import streamlit as st
from sz_utils import data_handler


def select_patient() -> str:
    """From the sidebar select a patient

    :return: The name of the patient
    :rtype: str
    """
    option = st.selectbox("Select a patient", data_handler.get_patients())
    return option


def select_edf(patient) -> str:
    """From the sidebar select a edf file

    :param patient: The name of the patient
    :type patient: str
    :return: The name of the edf file
    :rtype: str
    """
    option = st.selectbox("Select an edf file", data_handler.get_patient_edf(patient))
    return option


def select_view() -> str:
    """From the sidebar select a view

    :return: The name of the view
    :rtype: str
    """
    option: str = st.sidebar.selectbox(
        "Select a view", ["Table", "Graph", "Spectrogram"]
    )
    return option


def seizures_info(patient: str, edf_file: str) -> pd.DataFrame:
    """Get the seizure data per edf file

    :param patient: The name of the patient
    :type patient: str
    :param edf_file: The name of the edf file
    :type edf_file: str
    :return: The seizure data per edf file
    :rtype: pd.DataFrame
    """
    all_edfs = data_handler.get_seizure_data(patient)
    n_of_seizures = all_edfs[all_edfs["file_name"] == edf_file]["number_of_seizures"]
    times = all_edfs[all_edfs["file_name"] == edf_file]["start_end_times"]
    # TODO
    return pd.DataFrame()
    

def main_view(edf_data: pd.DataFrame) -> None:
    """Main view of the app

    :param edf_data: The data of the edf file
    :type edf_data: pd.DataFrame
    :return: None
    :rtype: None
    """
    view = select_view()
    if view == "Graph":
        pass
    elif view == "Spectrogram":
        # plot_spectrogram(edf_data)
        pass
    else:
        st.dataframe(edf_data)


def app() -> None:
    """Main function of the app"""
    st.set_page_config(page_title="Seizure Prediction", page_icon=":brain:")
    st.title("EEG Data Visualizer")

    with st.sidebar:
        st.title("Select your EEG data")
        patient = select_patient()
        edf = select_edf(patient)

    edf_data = data_handler.get_edf_data(patient, edf)

    # st.dataframe(seizure_data_per_edf(patient, edf)) TODO
    main_view(edf_data)

    st.write()


if __name__ == "__main__":
    app()
