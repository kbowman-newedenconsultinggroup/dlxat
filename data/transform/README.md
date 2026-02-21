mkdir for current date
export users from sd as current.csv
export DLX recipients spreadsheet from Google Doc
python3 ../../assets/dlxat/data/transform/transform.py DLX\ Device\ Recipients\ for\ InvGate\ -\ Intake.csv sd.csv as.csv current.csv
