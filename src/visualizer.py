"""A visualizer using streamlit for easy implementation of the project

This module is the main module of the visualizer. It uses the streamlit library
to create a web app that can be used to visualize some data. You can select a
patient and a edf file and then you can visualize the data in different ways.

This module uses the data_handler module to get the data from the files.
"""

import mne
import streamlit as st
from sz_utils import data_handler


def select_patient() -> str:
    """From the sidebar select a patient"""
    option = st.sidebar.selectbox("Select a patient", data_handler.get_patients())
    return option


def select_edf(patient) -> str:
    """From the sidebar select a edf file"""
    option = st.sidebar.selectbox(
        "Select an edf file", data_handler.get_patient_edf(patient)
    )
    return option


def select_view() -> str:
    """From the sidebar select a view"""
    option: str = st.sidebar.selectbox(
        "Select a view", ["Table", "Graph", "Spectrogram"]
    )
    return option


def plot_spectrogram(edf: mne.io.edf.edf.RawEDF) -> None:
    """Plot the spectrogram of the edf file in streamlit"""
    raise NotImplementedError


def main_view(edf_data: mne.io.edf.edf.RawEDF) -> None:
    """Main view of the app"""
    view: str = select_view()
    if view == "Graph":
        pass
    elif view == "Spectrogram":
        plot_spectrogram(edf_data)
    else:
        st.dataframe(edf_data.to_data_frame())
    return None


def app() -> None:
    """Main function of the app"""
    st.set_page_config(page_title="Seizure Prediction", page_icon=":brain:")
    st.title("EEG Data Visualizer")

    st.sidebar.title("Select your EEG data")

    patient: str = select_patient()
    edf: str = select_edf(patient)
    edf_data: mne.io.edf.edf.RawEDF = data_handler.get_edf_data(patient, edf)

    main_view(edf_data)

    st.write()


if __name__ == "__main__":
    app()
