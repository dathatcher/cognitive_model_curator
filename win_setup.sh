py -m venv venv
.\venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
pip install networkx
set PYTHONPATH=.
python -m cmc.run_pipeline
