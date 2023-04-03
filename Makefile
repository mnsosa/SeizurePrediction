web_app:
	streamlit run src/visualizer.py --server.maxMessageSize 1000

generate_dataset:
	cd src/scripts && python generate_dataset.py