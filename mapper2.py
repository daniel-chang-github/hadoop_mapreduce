
import sys

for line in sys.stdin:
    # Remove any spaces
    line = line.strip()
    # Assign key value from output of reducer1.py into variables
    values = line.split(",")

    make = values[1]
    year = values[2].replace(" ","")
    make_year = make+year

    print("%s"%(make_year))