import json 
call_dir = "call_info.json"
func_dir = "function_comment_info.json"
result_dir = 'call_comment_info.json'

call_result = []
func_result = []

def read_json(calldir,funcdir):
    with open(calldir,'r') as f:
        callresult = json.load(f)
        f.close()
    with open(funcdir,'r') as f:
        funcresult = json.load(f)
        f.close()
    return callresult, funcresult

if __name__ == "__main__":
    call_result, func_result = read_json(call_dir, func_dir)
    result = []
    idx = 0 
    for func in func_result:
        for call in call_result:
            if str(func['id']) == call['call_func_id']:
                print(0)
                idx += 1
                call['transfer_comment'] = func['comments']
                call['idx'] = idx
                result.append(call)
    with open(result_dir,'w') as f:
        json.dump(result,f)
        f.close()