source ./env/bin/activate
python3 -m pip install --upgrade --force-reinstall pyscpi --find-links=./../dist/
python3 osc_read.py
deactivate