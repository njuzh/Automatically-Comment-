import os
import re
import collections
import time
from _collections import OrderedDict

python_root_path = os.getcwd().replace("\\", "/")


def get_log(project_name: str, branch="master") -> list:
    project_master_dir = python_root_path + "/git_project/" + project_name + "/" + branch
    os.chdir(project_master_dir)
    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system(
        "git log  --date=format:'%Y-%m-%d'  --pretty=format:\"%H%  %cd  %s\" > " + output_dir + "/master_log.txt")
    # os.system(
    #     "git log  --date=format:'%Y-%m-%d'  --pretty=format:\"%H%  %cd  %s\" --no-merges > " + output_dir + "/master_log.txt")
    with open(output_dir + "/master_log.txt", encoding="utf-8") as fr:
        lines = fr.readlines()
    os.chdir(python_root_path)
    return lines


def get_diff(project_name: str) -> list:
    project_master_dir = python_root_path + "/git_project/" + project_name + "/master/"
    os.chdir(project_master_dir)
    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system(
        "git log  --date=format:'%Y-%m-%d' --pretty=format:\"%H%  %cd  %s\" --numstat > " + output_dir + "/master_diff.txt")
    # os.system(
    #     "git log  --date=format:'%Y-%m-%d' --pretty=format:\"%H%  %cd  %s\" --diff-filter=ADM --numstat > " + output_dir + "/master_diffT.txt")
    with open(output_dir + "/master_diff.txt", encoding="utf-8") as fr:
        lines = fr.readlines()
    os.chdir(python_root_path)
    return lines


def read_file(file_path):
    with open(file_path, encoding="utf-8") as fr:
        lines = fr.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines


def match_master(project_name: str, master_commit_id) -> list:
    branch = get_log(project_name, branch=project_name)
    version_sha1 = branch[0].split()[0]
    if version_sha1 != master_commit_id:
        print(project_name + " branch and master do not match")
        print(master_commit_id + " != " + version_sha1)
        project_master_dir = python_root_path + "/project/" + project_name + "/" + project_name
        os.chdir(project_master_dir)
        os.system("git reset --hard {}".format(master_commit_id))
    os.chdir(python_root_path)


def is_num(val):
    flag = True
    for item in val:
        if '0' <= item <= '9':
            continue
        else:
            flag = False
            break
    return flag


def is_sha1(val):
    return re.match("[0-9a-f]{8}", val)


def get_java_list(commit_sha_list, diff_lines: str) -> list:
    one_item = []
    num = 0
    # sha1 = commit_sha_list[0][0]
    for line in diff_lines[0:]:
        line = line.strip()
        if len(line) < 1:
            continue
        line_list = re.split(r'\s+', line)
        if is_sha1(line_list[0]):
            num += 1
            if len(one_item) >= 1:
                commit_sha_list[commit_sha_list.index([sha1])].extend(one_item)
            sha1 = line_list[0]
            one_item = []
        elif is_num(line_list[0]) and is_num(line_list[1]) and len(line_list) == 3:
            file_name = line_list[2]
            if not file_name.endswith(".py"):
                continue
            one_item.append(line_list)
    # for item in commit_sha_list[0:]:
    #     print(item)
    return commit_sha_list


def write_diff(master_lines, java_list, project_name):
    from collections import OrderedDict
    diff_dict = OrderedDict()
    project_master_dir = python_root_path + "/project/" + project_name
    os.chdir(project_master_dir)
    output_dir = "csv/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    index = -1
    with open(output_dir + "/commit_diff.csv", "w", encoding="utf-8") as fw:
        fw.write("index,sha1,date,description,add lines,del lines, files...\n")
        for i in range(len(java_list)):  # len(java_list)):
            line = master_lines[i].split()
            index = i
            sha1 = line[0]
            date = eval(line[1])
            desc = re.sub(r",+", r" ", " ".join(line[2:]))
            add_no = 0
            del_no = 0
            file_list = []
            if len(java_list[i]) <= 1:
                fw.writelines(str(index) + "," + sha1 + "," + date + "," + desc + ",0,0\n")
            else:
                for j in range(len(java_list[i]) - 1):
                    add_no += int(java_list[i][j + 1][0])
                    del_no += int(java_list[i][j + 1][1])
                    file_list.append(java_list[i][j + 1][2])
                fw.writelines(
                    str(index) + "," + sha1 + "," + date + "," + desc + "," + str(add_no) + "," + str(
                        del_no) + "," + ",".join(file_list) + "\n")
            # print(index, sha1, date, desc)
            # print(java_list[i])
            # print(line)
            # print()
    return


def reset_diff(java_list, project_name, master_commit_id):
    project_master_dir = python_root_path + "/project/" + project_name + "/" + project_name
    os.chdir(project_master_dir)
    diff_index_dir = "../diff_index/"
    if not os.path.exists(diff_index_dir):
        os.makedirs(diff_index_dir)
    diff_file_dir = "../diff_file/"
    if not os.path.exists(diff_file_dir):
        os.makedirs(diff_file_dir)
    #     os.system("git log  --date=format:'%Y-%m-%d'  --pretty=format:\"%H%  %cd  %s\" --no-merges > " + output_dir + "/master_log.txt")
    #     with open(output_dir + "/master_log.txt", encoding="utf-8") as fr:
    #         lines = fr.readlines()
    commit_index = -1
    file_cnt = 0
    for item in java_list:
        commit_index += 1
        if len(item) < 1:
            continue
        commit_sha1 = item[0]
        for _, _, raw_path in item[1:]:
            file_cnt += 1
            print("当前进度: {:.3f}%  {}/42099  {}/{}".
                  format(file_cnt * 100 / 42099, file_cnt, commit_index, len(java_list) - 1))
            class_path = raw_path.replace("/", "_")[:-5]
            file_name = raw_path.split("/")[-1]
            file_path = diff_file_dir + class_path
            diff_log_path = file_path + "/" + str(commit_index) + "_" + file_name
            # print(raw_path, file_name, file_path, diff_log_path)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            #
            os.system("git diff -p -n 1 {}~1 {} -- {} > {}".
                      format(commit_sha1, commit_sha1, raw_path, diff_log_path.replace(".java", ".txt")))
            diff_path = diff_index_dir + str(commit_index) + "_" + class_path + ".txt"
            os.system("git diff -p -n 1 {}~1 {} -- {} > {}".
                      format(commit_sha1, commit_sha1, raw_path, diff_path))
            print(diff_path)
    os.system("git reset --hard {}".format(master_commit_id))
    os.chdir(python_root_path)


def reset_file_diff(file_dict, project_name, master_commit_sha1):
    project_master_dir = python_root_path + "/project/" + project_name + "/" + project_name
    os.chdir(project_master_dir)
    file_version_dir = "../file_version/"
    if not os.path.exists(file_version_dir):
        os.makedirs(file_version_dir)
    index = -1
    file_cnt = 0
    print(master_commit_sha1)
    os.system("git reset --hard {}".format(master_commit_sha1))
    for raw_path, commit_item in file_dict.items():
        index += 1
        if len(commit_item) <= 0:
            continue
        # if index >= 2:
        #     continue
        for commit_sha, commit_version in commit_item:
            if commit_version == 0:
                print("error")
                return
            file_cnt += 1
            # print(raw_path, commit_version, commit_sha)
            print("当前进度: {:.3f}%  {}/42099\n\n".format(file_cnt * 100 / 37974, file_cnt))
            class_path = raw_path.replace("/", "_")[:-5]
            file_name = raw_path.split("/")[-1]
            file_path = file_version_dir + class_path
            # print(raw_path)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            total_file_name = file_path + "/" + str(commit_version) + "_" + file_name
            reset_cmd = "git checkout {} -- {}".format(commit_sha, raw_path)
            print(reset_cmd)
            os.system(reset_cmd)
            copy_cmd = "copy  " + raw_path.replace("/", "\\") + "  " + total_file_name.replace("/", "\\")
            print(copy_cmd)
            os.system(copy_cmd)

        reset_cmd = "git checkout {} -- {}".format(commit_sha, raw_path)
        print(reset_cmd)
        os.system(reset_cmd)
        total_file_name = file_path + "/" + str(commit_version + 1) + "_" + file_name
        copy_cmd = "copy  " + raw_path.replace("/", "\\") + "  " + total_file_name.replace("/", "\\")
        print(copy_cmd)
        os.system(copy_cmd)

    os.system("git reset --hard {}".format(master_commit_sha1))
    print(master_commit_sha1, "reset to master")
    os.chdir(python_root_path)
    return


import ASTTest


def get_sim(java_list, project_name, master_commit_id):
    project_master_dir = python_root_path + "/git_project/" + project_name + "/" + project_name
    os.chdir(project_master_dir)
    os.system("git reset --hard {}".format(master_commit_id))
    sha_file_dict = OrderedDict()
    for line_list in java_list[0:]:
        commit_sha1 = line_list[0]
        sha_file_dict[commit_sha1] = []
        if len(line_list) <= 1:
            continue
        for file_item in line_list[1:]:
            sha_file_dict[commit_sha1].append(file_item[2])
    print(len(java_list))

    dist_dict = OrderedDict()
    file_dist = OrderedDict()
    index = 0
    total = len(sha_file_dict)
    for commit_sha1, file_list in sha_file_dict.items():
        index += 1
        if index % 100 == 0:
            print("\r{} / {}".format(index, total), end="")
        file_dist[commit_sha1] = []
        dist_dict[commit_sha1] = []
        if len(file_list) == 0:
            file_dist[commit_sha1].append(" u 0")
            dist_dict[commit_sha1].append(" 0 0")
            continue
        dist_sum = 0
        for file in file_list:
            try:
                # print(commit_sha1, file)
                status1 = os.system("git checkout --quiet {} -- {}".format(commit_sha1, file))
                node_str1 = ""
                node_str2 = ""
                if status1 == 0:
                    node_str1 = ASTTest.file2nodes(file)
                # if not os.path.exists(file):
                #     print(commit_sha1, file, "not exist")
                status2 = os.system("git checkout --quiet {}~1 -- {}".format(commit_sha1, file))
                if status2 == 0:
                    node_str2 = ASTTest.file2nodes(file)
                if status1 == 1 and status2 == 0:
                    print(file, "delete in commit", commit_sha1)
                    dist_sum += len(node_str2)
                    file_dist[commit_sha1].append(" - " + file + " " + str(len(node_str2)))
                elif status1 == 0 and status2 == 1:
                    print(file, "add in commit", commit_sha1)
                    dist_sum += len(node_str1)
                    file_dist[commit_sha1].append("+ " + file + " " + str(len(node_str1)))
                elif status1 == 0 and status2 == 0:
                    distance = ASTTest.get_node_sim(node_str1, node_str2)
                    dist_sum += distance
                    file_dist[commit_sha1].append(" d " + file + " " + str(distance))
            except Exception as e:
                pass
        dist_dict[commit_sha1].append(" " + str(dist_sum) + " " + str(len(file_list)))

    os.system("git reset --hard {}".format(master_commit_id))
    print(master_commit_id, "reset to master")
    index = -1
    total = len(file_dist)
    with open("../output/commit_diff.txt", "w", encoding="utf-8") as fw:
        for commit_sha1, v in file_dist.items():
            index += 1
            fw.write(str(total - index) + " " + commit_sha1 + " ".join(v) + "\n")
    index = -1
    total = len(file_dist)
    with open("../output/commit_dist.txt", "w", encoding="utf-8") as fw:
        for commit_sha1, v in dist_dict.items():
            index += 1
            fw.write(str(total - index) + " " + commit_sha1 + " " + " ".join(v) + "\n")
    os.chdir(python_root_path)


def main():
    project_name = "matplotlib"
    # log_lines = get_log(project_name)
    # diff_lines = get_diff(project_name)
    master_lines = read_file(python_root_path + "/git_project/" + project_name + "/output/master_log.txt")
    diff_lines = read_file(python_root_path + "/git_project/" + project_name + "/output/master_diff.txt")

    commit_sha_list = []
    for item in master_lines[0:]:
        commit_sha_list.append([item.split()[0]])

    master_commit_id = commit_sha_list[0][0]
    match_master(project_name, master_commit_id)

    java_list = get_java_list(commit_sha_list, diff_lines)

    get_sim(java_list, project_name, master_commit_id)
    print("master:", master_commit_id)


if __name__ == '__main__':
    main()
