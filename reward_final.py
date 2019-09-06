from csv import DictReader
from itertools import groupby
from pprint import pprint
import fileinput
import time

def check_for_null_new(allvars):
    first_split =  allvars.split(',')
    ret_val=""
    loop_cnt=1
    for second_split in first_split:
        try:
            individual_split = second_split.split(':')
            if not individual_split[1]:
                pass
            else:
                if loop_cnt == 1:
                    if individual_split[1].isnumeric():
                        ret_val=(individual_split[0]+":"+individual_split[1])
                    else:
                        ret_val=(individual_split[0]+":'"+individual_split[1]+"'")
                else:
                    if individual_split[1].isnumeric():
                        ret_val=ret_val +','+ (individual_split[0]+":"+individual_split[1])
                    else:
                        ret_val=ret_val +','+ (individual_split[0]+":'"+individual_split[1]+"'")
                loop_cnt = loop_cnt + 1
        except:
            print('Something happened in check_for_null_new @')
            
    return (ret_val)

start_time = time.time()       
with open(r'C:\\Amit\\Mariott\\Project Docs\\Marriott_test\\reward.csv',encoding='utf-8-sig') as csvfile:
    r1 = DictReader(csvfile, skipinitialspace=True)
    data = [dict(d) for d in r1]
    #print(data)
    groups = []
    uniquekeys = []

    try:
        for k, g in groupby(data, lambda r: ( r['csId'], r['lut'], r['seqId'], r['ptBal'], r['cur'], r['lt'], r['srtDt'], r['edDt'], r['pts'], r['dt'])):
            #print(k[0])
            groups.append({ "type": "rewd",
                        "csId": int(k[0]),
                        "lut": int(k[1]),
                        "seqId": int(k[2]),
                        "ptBal": int(k[3]),
                        "ntSum" : {check_for_null_new("'cur':"+k[4]+",'lt':"+ k[5])},
                        #"lstSty": {'srtDt': k[6], 'edDt': k[7]},
                        "lstSty": {check_for_null_new("'srtDt':"+k[6]+",'edDt':"+k[7])},
                        #"lstRdp": {'pts': int(k[8]), 'dt': k[9]} })
                        "lstRdp": {check_for_null_new("'pts':"+(k[8])+",'dt':"+k[9])} 
                        })
            
            uniquekeys.append(g)
    except:
        print('Something happened @')
		
#pprint(groups)

with open('C:\\Amit\\Mariott\\Project Docs\\Marriott_test\\reward.json', 'wt') as out:
    pprint(groups, stream=out)

with fileinput.FileInput('C:\\Amit\\Mariott\\Project Docs\\Marriott_test\\reward.json', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("\"", "").replace("'", "\""), end='')

end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))

