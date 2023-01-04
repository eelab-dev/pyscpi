source ./env/bin/activate
python3 -m pip install --upgrade --force-reinstall ./../dist/pyscpi-0.1.0.tar.gz
python3 osc_read.py
deactivate