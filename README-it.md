[English](README.md) / [Spanish](README-sp.md) / [Italian](README-it.md)

# Previsione delle crisi 🧠

## Descrizione

Questo repository contiene lo sviluppo del progetto finale del titolo di Ingegneria Biomedica, realizzato da Matías N. Sosa e Cristian E. Morilla. L'idea è di effettuare uno studio comparativo di diverse tecniche di Deep Learning moderne per prevedere il periodo pre-ictale, ovvero il periodo prima del periodo convulsivo. Ciò verrà fatto utilizzando i dati EEG.

Organizzazione
L'organizzazione del repository è la seguente:

<pre>
├───📁 src/
│   ├───📁 demos/
│   │   ├───...
│   ├───📁 notebooks/
│   │   └───...
│   ├───📁 sz_utils/
│   │   └───...
│   ├───📄 visualizer.py
│   ├───📄 config.py
│   └───📄 setup.py
├───📄 Makefile
├───📄 README.md
└───📄 requirements.txt
</pre>

Nella cartella `src` abbiamo il codice sorgente del progetto. Nella cartella `notebooks` abbiamo i diversi notebook Jupyter che abbiamo utilizzato per esplorare i dati e per pensare a alcuni processi. In `sz_utils` ci sono file python importanti. Nel file preprocess, abbiamo il codice che abbiamo utilizzato per preprocessare i dati. Il modulo `data_handler` è quello che abbiamo creato e utilizzato per gestire i dati di CHB. Il file `Makefile` viene utilizzato per automatizzare l'esecuzione dei diversi script. Il file `config.py` contiene la configurazione del progetto, come i percorsi dei dati, i percorsi dei modelli, ecc. Il file `requirements.txt` contiene le dipendenze del progetto. Infine, il file `visualizer.py` contiene il codice per visualizzare i risultati degli esperimenti. Nella cartella `demos`, abbiamo alcuni script per mostrare come utilizzare i diversi moduli del progetto.

## Installazione [utilizzando conda]

1. `conda create -n seizure-prediction python=3.10.4`
2. `conda activate seizure-prediction`
3. `pip install -r requirements.txt`
4. `pip install -e src` (questo installerà il progetto come un pacchetto)
5. Scaricare i dati da https://physionet.org/content/chbmit/1.0.0/. Utilizzando il terminale: `wget -r -np -nH --cut-dirs=3 -R index.html* https://physionet.org/files/chbmit/1.0.0/`. **Se hai già scaricato i dati, puoi saltare questo passaggio.**
6. Modificare il file src/config.py per impostare le percorso dei dati. Ciò che è necessario modificare è la chiave CHB_FOLDER_DIR dell'dizionario di configurazione.

## Esecuzione
L'esecuzione verrà effettuata utilizzando il `Makefile`.

```bash
make OPTION
```

Le diverse opzioni disponibili al momento sono:

1. `web_app`: Eseguire l'applicazione web.


<br>
<br>
<br>


🤓 **Matías Nicolás Sosa**

🤓 **Cristian Ezequiel Morilla**