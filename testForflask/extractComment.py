import csv
import json
json_dir = "function_info.json"
csv_dir = "result.csv"
result_dir = "function_comment_info.json"

csv_result = {}
json_result = []

def read_csv(csv_dir):
    csvFile = open(csv_dir,"r")
    reader = csv.reader(csvFile)
    for item in reader:
        if reader.line_num == 1:
            continue
        csv_result[item[0]] = item[1:]
    csvFile.close()
    return csv_result
    # for value in csv_result.values():
    #     print (value[0].split("\\")[-1])
    
def read_json(json_dir):
    with open(json_dir, 'r') as load_f:
        json_result = json.load(load_f)
        load_f.close()
    return json_result
        # for func in json_result:
        #      print(func['file'].split("/")[-1])

if __name__ == "__main__":
    csv_result = read_csv(csv_dir)
    json_result = read_json(json_dir)
    result = []
    i = 0
    for value in csv_result.values():
        i += 1
        for func in json_result:
            if value[0].split("\\")[-1] == func['file'].split("/")[-1] and value[1] == func['name'].split(".")[-1]:
                func['comments'] = value[2]
                func['idx'] = i
                result.append(func)
    with open(result_dir,"w") as f:
        json.dump(result,f)
        f.close()
    # print(len(result))