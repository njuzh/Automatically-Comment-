import csv
import json
import os

pardir = os.path.abspath(os.path.dirname(os.getcwd()))
datasets = ["flask", "requests", "keras", "django","spaCy"]
#datasets = ["flask"]
file_dir = os.path.join(pardir,"results")
#result_dir = os.path.join(pardir, "results", "function_comment_info.json")

csv_result = {}
json_result = []

def read_csv(csv_dir):
    csvFile = open(csv_dir,"r",encoding="utf8")
    reader = csv.reader(csvFile)
    for item in reader:
        if reader.line_num == 1:
            continue
        csv_result[item[0]] = item[1:]
    csvFile.close()
    return csv_result
    
    
def read_json(json_dir):
    with open(json_dir, 'r') as load_f:
        json_result = json.load(load_f)
        load_f.close()
    return json_result
        # for func in json_result:
        #      print(func['file'].split("/")[-1])

if __name__ == "__main__":
    for dataset in datasets:
        print(dataset)
        csv_result = read_csv(os.path.join(file_dir,dataset + ".csv"))
        
        json_result = read_json(os.path.join(file_dir,"function_info_" + dataset + ".json"))
        # for value in json_result:
        #     print (value)
        result = []
        i = 0
        for value in csv_result.values():
            i += 1
            for func in json_result:
                #print (value[1].split("\\")[-1],func['file'].split("/")[-1])
                if value[1].split("\\")[-1] == func['file'].split("/")[-1] and value[2] == func['name'].split(".")[-1]:
                    func['comments'] = value[3]
                    func['idx'] = i
                    result.append(func)
        with open(os.path.join(file_dir,dataset + "_goodfunc_info.json"),"w", encoding = 'utf8') as f:
            json.dump(result,f)
            f.close()
    # print(len(result))