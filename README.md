# Seizure Prediction 🧠

## Description

This repository contains the development of the final project of the Biomedical Engineering degree, together with my partner Cristian E. Morilla. The idea is to make a comparative study of different modern Deep Learning techniques to predict the pre-ictal period, that is, the period before the convulsive period. This will be done using EEG data.



## Organization

The organization of the repository is as follows:

<pre>
├───📁 src/
│   ├───📁 experiments/
│   │   ├───📁 models/
│   │   │   └───...
│   │   └───📁 notebooks/
│   │       └───...
│   └───📁 preprocessing/
│       └───...
├───📄 Makefile
├───📄 README.md
├───📄 config.py
├───📄 requirements.txt
└───📄 visualizer.py
</pre>

In the `src` folder, we have the source code of the project. In the `experiments` folder, we have the different models that we have tried, and in the `notebooks` folder, we have the notebooks that we have used to develop the project. In the `preprocess` folder, we have the code that we have used to preprocess the data. The `Makefile` is used to automate the execution of the different scripts. The `config.py` file contains the configuration of the project, such as the paths to the data, the paths to the models, etc. The `requirements.txt` file contains the dependencies of the project. Finally, the `visualizer.py` file contains the code to visualize the results of the experiments.



## Install [using conda]

1. `conda create -n seizure-prediction python=3.10.4`
2. `conda activate seizure-prediction`
3. `pip install -r requirements.txt`
4. `pip install -e src` (this will install the project as a package)
5. Download the data from https://physionet.org/content/chbmit/1.0.0/. Using the terminal: `wget -r -np -nH --cut-dirs=3 -R index.html* https://physionet.org/files/chbmit/1.0.0/`. **If you already downloaded the data, you can skip this step.**
6. Edit the `src/config.py` file to set the paths to the data. What you need to edit it is the `CHB_FOLDER_DIR` key from the config dict.



## Run

The running will be done using the `Makefile`. 

```bash
make OPTION
```

The different options available for now are: 

1. `web_app`: Run the web app.




<br>
<br>
<br>

🤓 **Matías Nicolás Sosa**

🤓 **Cristian Ezequiel Morilla**