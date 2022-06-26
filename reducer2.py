
import sys

# Initialize accident count dictionary to keep track
accident_count_info = {}


# Flush out reducer key and values with function
def flush():
    """
    Print out the combination of make and year as key and count as value.
    """
    for key in accident_count_info.keys():
        print("%s\t%s"%(accident_count_info[key]['make_year'], accident_count_info[key]['accident_count'] ))

for line in sys.stdin:
    line = line.strip()
    # make, year  = line.split('\t')
    # make_year = make + ' ' + year

    # If key from mapper2.py is not present in the dictionary, create a new entry.
    if line not in accident_count_info:
        accident_count_info[line] = {"make_year": line, "accident_count": 0}

    accident_count_info[line]['accident_count'] += 1

flush()