import os
import json
from collections import defaultdict

pardir = os.path.abspath(os.path.dirname(os.getcwd()))
file_dir = os.path.join(pardir, "results")

def read_json(json_dir):
    json_result = []
    result = defaultdict(list)
    with open(json_dir, 'r') as f:
        json_result = json.load(f)
        f.close()
    for item in json_result:
        result[item['name']].append(item['call_func_name'])
    return result
def read_txt(txt_dir):
    txt_result = defaultdict(list)
    with open(txt_dir, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.split('$')
            src = tmp[0]
            dst = tmp[1].split('\n')[0]
            txt_result[src].append(dst)
    #print(txt_result)        
    return txt_result

if __name__ == "__main__":
    static_result = read_json(os.path.join(file_dir,"call_info_scipy.json"))
    dynamic_result = read_txt(os.path.join(file_dir,"scipy_trace.txt"))
    common = dynamic_result.keys() & static_result.keys()
    diff = dynamic_result.keys() - static_result.keys()
    print("static_length:",len(static_result),"dynamic_length:",len(dynamic_result),"common_length:",len(common),"diff_length:",len(diff))
    count = 0
   
    with open("common_scipy.txt", "w", encoding='utf-8') as f:
        result = [dynamic_result[key] for key in common]
        for k,v in zip(common,result):
            f.write(k+"\t"+str(v)+"\n")
    with open("diff_scipy.txt", "w", encoding='utf-8') as f:
        result = [dynamic_result[key] for key in diff]
        for k,v in zip(diff,result):
            f.write(k+"\t"+str(v)+"\n")
    # for d in diff:
    #     print (d)
    # #print(static_result)