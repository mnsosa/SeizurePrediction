[English](README.md) / [Spanish](README-sp.md) / [Italian](README-it.md)

# Prediccion de convulsiones 🧠

Este repositorio contiene el desarrollo del proyecto final del título de Ingeniería Biomédica, realizado por  Matías N. Sosa y Cristian E. Morilla. La idea es realizar un estudio comparativo de diferentes técnicas de Deep Learning modernas para predecir el período preictal, es decir, el período antes del período convulsivo. Esto se realizará utilizando datos de EEG.


## Organización
La organización del repositorio es la siguiente:

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
├───📄 .gitignore
├───📄 README-sp.md
├───📄 README.md
├───📄 Makefile
├───📄 requirements.txt
└───📄 LICENSE.txt
</pre>

En la carpeta `src` tenemos el código fuente del proyecto. En la carpeta `notebooks` tenemos las diferentes libretas de Jupyter que hemos utilizado para explorar los datos y para pensar algunos procesos. En `sz_utils` se encuentran archivos python importantes. En el archivo `preprocess`, tenemos el código que hemos utilizado para preprocesar los datos. El módulo `data_handler` es el que hemos creado y utilizado para gestionar los datos de CHB. El archivo `Makefile` se utiliza para automatizar la ejecución de los diferentes scripts. El archivo `config.py` contiene la configuración del proyecto, como los caminos a los datos, los caminos a los modelos, etc. El archivo `requirements.txt` contiene las dependencias del proyecto. Finalmente, el archivo `visualizer.py` contiene el código para visualizar los resultados de los experimentos. En la carpeta `demos`, tenemos algunos scripts para mostrar cómo utilizar los diferentes módulos del proyecto.

 

## Instalación [utilizando conda]

1. `conda create -n seizure-prediction python=3.10.4`
2. `conda activate seizure-prediction`
3. `pip install -r requirements.txt`
4. `pip install -e src` (esto instalará el proyecto como un paquete)
5. Descargue los datos de https://physionet.org/content/chbmit/1.0.0/. Utilizando la terminal: `wget -r -np -nH --cut-dirs=3 -R index.html* https://physionet.org/files/chbmit/1.0.0/` **Si ya tiene los datos, puede omitir este paso.**
6. Edite el archivo `src/config.py` para establecer las rutas a los datos. Lo que necesita editar es la clave `CHB_FOLDER_DIR` del diccionario de configuración. 

## Ejecución
La ejecución se realizará utilizando el `Makefile`.

```bash
make OPTION
```
Las diferentes opciones disponibles por ahora son:

1. `web_app`: Ejecutar la aplicación web.

<br>
<br>
<br>

🤓 **Matías Nicolás Sosa**

🤓 **Cristian Ezequiel Morilla**