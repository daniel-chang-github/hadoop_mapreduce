import sys

master_list={}

def reset():
    master_list = {}

def flush():
    for key in master_list.keys():
        if master_list[key]['accident_count']>0:
            print(('%s, %s, %s, %s' % (key, master_list[key]['make'], master_list[key]['year'],master_list[key]['accident_count'] )))

for line in sys.stdin:
    
    # Assign key value pair from the output of mapper1.py into variables
    vin_number, values = line.split('\t')
    val_list = [val.replace("'", "").replace("(", "").replace(")", "").replace(" ", "").replace("\n", "")  for val in values.split(",")]
    
    incident_type = val_list[0]
    car_make      = val_list[1]
    car_year      = val_list[2]

    # Use master_list dictionary to keep track of accident_count for each make and year
    if vin_number not in master_list:
        
        master_list[vin_number] = {"make": None, "year": None, "accident_count": 0}

    # Collect the vehicle make and year data from master_list where incident type == "I" to propagate
    if incident_type == "I":
        master_list[vin_number]["make"] = car_make
        master_list[vin_number]["year"] = car_year

    #Increase the accident counter if incident type "A" exists
    if incident_type == "A":
        master_list[vin_number]["accident_count"] += 1

    
      
    





flush()
