import os
import re
import ASTTest
from collections import OrderedDict

python_root_path = os.getcwd().replace("\\", "/")

versions = """
v3.0.0      2018-08-12  df545a043386557f01fa75a1cd231b57688fa727
v2.2.3      2018-08-10  2e0eb748d3c1b808ed89e86e80a2d1565b4cd896    The 3rd bug-fix release of the v2.2 LTS series
v2.2.2      2018-05-17  b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68    The 2nd bug-fix release of the v2.2 LTS series.
v2.2.1      2018-05-17  1021510fb4bf09680294255527ff07ce7fa3c527    The 1st bug-fix release of the v2.2 LTS series.
v2.2.0      2018-05-06  66e49f9a28f29b9a3a18cd4c6bfd5fdd1836eb0e    The 1st release of the v2.2 LTS series
v2.1.2      2018-01-18  24f0d9c47a00c2e58da421c0621eb2e90579e4c6    The 2nd bug-fix release for the 2.1 series.
v2.1.1      2017-12-10  be7e4e46dc010bc237485081b42e541190754285    The 1st and only planned bug-fix release for the 2.1 series.
v2.1.0      2017-10-08  b392d46466e98cd6a437e16b52b3ed8de23b0b52    This is the second minor release in the Matplotlib 2.x series and the first release with major new features since 1.5.
v2.0.2      2017-05-10  e175a41cb81880dbc553d9140e6ae5717457afa8    Critical bug fixes for 2.0.1
v2.0.1      2017-05-02  cef1be3e6e6cb9b0df403fa2869db4f9f75aff09    Bug fix release for 2.0.x series
v2.0.0      2017-01-17  1bfc7551f32f7b42ba50620a837f03e51d5b7c77    Major release of Matplotlib
v1.5.3      2016-09-09  26382a72ea234ee0efd40543c8ae4a30cffc4f0d    26382a72ea234ee0efd40543c8ae4a30cffc4f0d
v1.5.2      2016-07-03  179de2b384956f8ffa9f073b5a126ff3cd2a9df8    Final planned release for the 1.5.x series.
v1.5.1      2016-01-11  be91fac9fa2b7250080557e723af75124659da4e    First bug fix release for 1.5.x series.
v1.5.0      2015-11-30  a64e2a0219cb5b4a8ed1476c523724d731c67cac    This release of matplotlib has several major new features
v1.4.3      2015-02-16  21f46ff14ea65eeb725a4fd6c36642dddf3fea79    This is the last planned bug-fix release in the 1.4 series.
v1.4.2      2014-11-26  3a828ddb7df3bc597254f875cbbac6aadf48aee0    Minor bug-fix release for 1.4 series
v1.4.1      2014-11-09  809e627f55b83849982c7071891383c0c566c7f5    Bug-fix release for the 1.4 series.
v1.4.0      2014-08-27  a451e2c3af6fb4fd0e707ad7bfc3bd59b1f2715f    This release contains many bug fixes as will as a number of new features
v1.3.1      7e47149a7b05f8e5cf1cc899a7e4e7c90dd4244f
v1.3.0      2013-07-31  1614a0d392076296a8333bb89e9188c1a8ccae76
v1.2.1      8a17df09af8af05bde97532603fff9e6068e328e
v1.2.0      2012-11-30  85b020cfc259193eb9a25d5280e8f0c577fc22f1
v1.1.1      7e47149a7b05f8e5cf1cc899a7e4e7c90dd4244f
v1.1.0      2011-09-25  0fc9830fe946f6221e9ceff2910cd0c2118b0965
v1.0.1      a9f3f3a50745a1ca0e666bb1b6d0b9d782553dd9
v1.0.0      668a769fb6ef399476d573bf86cceb2fa9168495
"""

release_version = """
v1.0.0
v1.0.1
v1.1.0
v1.1.1
v1.2.0
v1.2.1
v1.3.0
v1.3.1
v1.4.0
v1.4.1
v1.4.2
v1.4.3
v1.5.0
v1.5.1
v1.5.2
v1.5.3
v2.0.0
v2.0.1
v2.0.2
v2.1.0
v2.1.1
v2.1.2
v2.2.0
v2.2.1
v2.2.2
v2.2.3
v3.0.0
v3.0.1
"""

release_version = release_version.split()
release_version.reverse()


def iter_files(rootDir, file_list):
    # 遍历根目录
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root, file)
            if file_name.endswith(".py"):
                file_name = file_name.replace("\\", "/").replace("//", "/")
                code_str = ""
                try:
                    with open(file_name, encoding="utf-8") as fr:
                        code_str = fr.read()
                except Exception:
                    print(file_name)
                file_list[file_name] = code_str
        for dirname in dirs:
            # 递归调用自身,只改变目录名称
            iter_files(root + "/" + dirname, file_list)


def get_all_files():
    file_dict = {}
    iter_files("./", file_dict)
    return file_dict


def read_version_commit(project_name):
    project_master_dir = python_root_path + "/git_project/" + project_name + "/" + project_name
    os.chdir(project_master_dir)
    os.system("git reset --hard f28897705bb6a98066ea8b3b5716cd25b6ebd078")
    total_dict_list = []

    print(release_version)
    for tag in release_version:
        os.system("git reset --hard " + tag)
        total_dict_list.append(get_all_files())
        print()
    os.system("git reset --hard f28897705bb6a98066ea8b3b5716cd25b6ebd078")
    file_version = open("../output/versions.txt", "w", encoding="utf-8")
    for i in range(len(total_dict_list) - 1):
        print(release_version[i], "<==>", release_version[i + 1])
        version_list1 = total_dict_list[i]
        version_list2 = total_dict_list[i + 1]
        file_set = set(version_list1.keys()) | set(version_list2.keys())
        file_cnt = 0
        dist_cnt = 0
        index = 0
        for file in file_set:
            code_str1 = version_list1.get(file, "")
            code_str2 = version_list2.get(file, "")
            if code_str1.strip() != code_str2.strip():
                index += 1
                print("\r{} / {}".format(index, len(file_set)), end="  ")
                distance = 0
                try:
                    distance = ASTTest.get_code_str_sim(code_str1, code_str2)
                except:
                    continue
                dist_cnt += distance
                file_cnt += 1
        print(file_cnt, dist_cnt)
        file_version.write(
            release_version[i] + "<==>" + release_version[i + 1] + "," + str(file_cnt) + "," + str(dist_cnt) + "\n")

    os.chdir(python_root_path)
    return total_dict_list


def main():
    project_name = "matplotlib"

    total_dict_list = read_version_commit(project_name)
    print(len(total_dict_list))


if __name__ == "__main__":
    main()
