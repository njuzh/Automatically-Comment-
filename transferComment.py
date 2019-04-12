import json 
import os
pardir = os.path.abspath(os.path.dirname(os.getcwd()))
file_dir = os.path.join(pardir,"results")
datasets = ["flask", "requests", "keras", "django","spaCy"]

call_result = []
func_result = []

def read_json(calldir,funcdir):
    with open(calldir,'r',encoding='utf8') as f:
        callresult = json.load(f)
        f.close()
    with open(funcdir,'r',encoding='utf8') as f:
        funcresult = json.load(f)
        f.close()
    return callresult, funcresult
#def count_method_call(methods):


if __name__ == "__main__":
    for dataset in datasets:
        print (dataset,"analyzing"+"\n")
        call_result, func_result = read_json(os.path.join(file_dir,"call_info_" + dataset + ".json"), os.path.join(file_dir, dataset +"_goodfunc_info" + ".json"))
        result = []
        func_info = []
        idx = 0
        max_call_count = 0 
        for func in func_result:
            func_call_num = 0
            func_call_list = []
            for call in call_result:
                if str(func['id']) == call['call_func_id']:
                    idx += 1
                    func_call_num += 1
                    func_call_list.append(call['name'])
                    call['transfer_comment'] = func['comments']
                    call['idx'] = idx
                    result.append(call)
            func['is_called_num'] =  func_call_num
            func['is_calld_by'] = func_call_list
            if func_call_num > max_call_count:
                max_call_count = func_call_num
            func_info.append(func)
        print("the max method call times of", dataset, "is", max_call_count)
        with open(os.path.join(file_dir,dataset + "_pass_result.json"),'w',encoding='utf8') as f:
            json.dump(result,f)
            f.close()
        with open(os.path.join(file_dir,dataset + "_func_info.json"),'w',encoding='utf8') as f:
            json.dump(func_info,f)
            f.close()
        
        print(dataset,"analyzed"+"\n")