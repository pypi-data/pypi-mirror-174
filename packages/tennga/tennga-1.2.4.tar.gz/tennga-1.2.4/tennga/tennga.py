import glob
import json
import logging
import os
import shutil
import tarfile
import requests

#测试服务器 http://localhost:8000/xxx


def init():
    """
    新建文件夹srcf,srcf/blocks,srcf/srcs
    """
    os.makedirs("srcf/blocks", exist_ok=True)
    os.makedirs("srcf/srcs", exist_ok=True)
    if not os.path.exists("srcf/src.json"):
        with open("srcf/src.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([]))


def listsrc() -> list:
    """
    返回src按顺序
    """
    srcs = None
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())
    return srcs


def add(url) -> str:
    """
    将一个源加入src.json
    比如 http://www.baidu.com/xxx.json
    """
    srcs = None
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())

    with open("srcf/src.json", "w", encoding="utf-8") as f:
        srcs.append(url)
        srcs = list(set(srcs))
        f.write(json.dumps(srcs))


def remove(url) -> str:
    """
    删除url源
    删除源从src.json
    删除源文件从srcf/srcs
    """
    srcs = None
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())
    try:
        srcs.remove(url)
    except:
        return False
    with open("srcf/src.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(srcs))
    return True


def update() -> str:
    """
    更新与使用源 下载所有源文件到srcf/srcs下面
    返回所有失败以及成功
    """
    result = ""
    srcs = None
    shutil.rmtree("srcf/srcs")
    os.makedirs("srcf/srcs", exist_ok=True)
    with open("srcf/src.json", "r", encoding="utf-8") as f:
        srcs = json.loads(f.read())
    for i in srcs:
        try:
            res = requests.get(i,stream=True)
        except:
            result += f"{i},failed\n"
            continue
        if res.status_code == 200:
            _, filename = os.path.split(i)
            with open(f"srcf/srcs/{filename}", "wb") as f:
                for chunk in res.iter_content(chunk_size=1024):
                    f.write(chunk)
            result += f"{i},ok\n"
        else:
            result += f"{i},failed\n"
    return result


def freeze(folder=None):
    """
    v1.2.0版本以后新增
    返回:  安装的所有内容
    参数 : 所属文件夹,指的是源里面的虚文件夹，比如 目录1
    """
    files = []
    #分为有folder与无folder
    if folder:  #找出指定文件夹下内容
        folders2 = next(os.walk(f"srcf/{folder}"))[1]
        for j in folders2:
            tempdic = {}
            tempdic["name"] = j
            tempdic["folder"] = folder
            tempdic["uuid"] = ""
            if len(glob.glob(f"srcf/{folder}/{j}/*.lock")) > 0:
                filename = os.path.split(
                    glob.glob(f"srcf/{folder}/{j}/*.lock")[0])[1].split(".")[0]
                tempdic["uuid"] = filename
            files.append(tempdic)
    else:  #无folder就找出所有文件夹下内容
        folders = next(os.walk("srcf"))[1]
        folders.remove("blocks")
        folders.remove("srcs")
        for i in folders:
            folders2 = next(os.walk(f"srcf/{i}"))[1]
            for j in folders2:
                tempdic = {}
                tempdic["name"] = j
                tempdic["folder"] = i
                if len(glob.glob(f"srcf/{i}/{j}/*.lock")) > 0:
                    filename = os.path.split(
                        glob.glob(f"srcf/{i}/{j}/*.lock")[0])[1].split(".")[0]
                    tempdic["uuid"] = filename
                files.append(tempdic)
    return files


def find(file, uuid=None) -> list:
    """
    v1.2.0版本以后使用此替代search
    返回：
    file:所有文件
    uuid:uuid数据是唯一的,替换了原来的时间
    """
    srcs = glob.glob("srcf/srcs/*.json")
    files = []
    for i in srcs:
        jswen = None
        with open(i, "r", encoding="utf-8") as f:
            jswen = json.loads(f.read())
            del jswen["blocks"]
        for j in jswen:
            for z in jswen[j]:  #分为 有uuid 以及 无 uuid
                if uuid != None:
                    if z["uuid"] == uuid and z["name"].find(file) > -1:
                        files.append([j, z["name"], z["uuid"]])
                else:
                    if z["name"].find(file) > -1:
                        files.append([j, z["name"], z["uuid"]])
    return files


def install(folder, name, uuid=None):
    """
    v1.2.0版本以后使用此替代download
    返回：
    folder:所属文件夹，不可忽略
    file:所有文件，不可忽略
    uuid:uuid数据是唯一的,替换了原来的时间,如果忽略则随意安装
    同名库会互相替代。所以安装时注意uuid。
    """
    srcs = glob.glob("srcf/srcs/*.json")
    for i in srcs:
        jswen = None
        blocks = None
        with open(i, "r", encoding="utf-8") as f:
            jswen = json.loads(f.read())
            blocks = jswen["blocks"] if "blocks" in jswen else None
            del jswen["blocks"]

        for j in jswen:
            for z in jswen[j]:  #分为 有uuid 以及 无 uuid
                if uuid != None:
                    if j == folder and z["uuid"] == uuid and z["name"] == name:
                        texts = __download(z, j, blocks)

                        return texts
                else:
                    if j == folder and z["name"] == name:
                        texts = __download(z, j, blocks)
                        return texts
    return "failed"


def uninstall(folder, name):
    """
    v1.2.0版本以后新增
    返回：
    folder:所属文件夹，不可忽略
    file:所有文件，不可忽略
    """
    if os.path.exists(f"srcf/{folder}/{name}"):
        shutil.rmtree(f"srcf/{folder}/{name}")
        return True
    else:
        return False


def getfile(folder, file):
    """
    v1.2.0版本以后新增
    folder是虚文件夹，json里第二层的东西
    返回：
    完整目录。如果对应不存在，返回None
    """
    if os.path.exists(f"srcf/{folder}/{file}"):
        return f"srcf/{folder}/{file}"
    else:
        return None


def getfiles(folder):
    """
    v1.2.0版本以后新增
    返回：
    folder:所属虚文件夹，不可忽略
    file:所有文件，不可忽略
    返回：
    list。如果对应不存在，返回空列表
    """
    folders = []
    if os.path.exists(f"srcf/{folder}"):
        folders2 = next(os.walk(f"srcf/{folder}"))[1]
        for i in folders2:
            folders.append(f"srcf/{folder}/{i}")
    return folders


def __download(filedic, folder, blocks=None) -> str:
    os.makedirs(f"srcf/{folder}/{filedic['name']}", exist_ok=True)
    fp = open(f"srcf/{folder}/{filedic['name']}/{filedic['uuid']}.lock",
              'w',
              encoding="utf-8")
    # with open(f"srcf/{folder}/{filedic['name']}/{filedic['uuid']}.lock",
    #           'w',encoding="utf-8") as f:
    #     f.write("lock")
    links = filedic['urls']
    texts = ""
    filelists = {"files":[],"blocks":[],"allfiles":[]}
    filecont = 0
    
    for i in links:
        link = i.strip()
        if link[0:4] == "http":  #如果是http链接就直接下载
            _, filename = os.path.split(i)
            if filename == "":
                filename = str(filecont) + ".bytes"
                filecont += 1
            try:
                res = requests.get(link,stream=True)
                if res.status_code != 200:
                    texts += f"{filename},failed\n"
                    continue
            except:
                if os.path.exists(f"srcf/{folder}/{filedic['name']}/{filename}"
                                  ):  #如果下载出错就查看本地有没有
                    texts += f"{filename},ok\n"
                    continue
                else:
                    texts += f"{filename},failed\n"
                    continue
            with open(f"srcf/{folder}/{filedic['name']}/{filename}",
                      "wb") as f:
                for chunk in res.iter_content(chunk_size=1024):
                    f.write(chunk)
                filelists["files"].append(filename)
                filelists["allfiles"].append(filename)
                texts += f"{filename},ok\n"
        elif link[0:5] == "block":
            cont, res = __blockReader(link, blocks)
            _, filename = os.path.split(i)
            if res == "ok":
                with open(f"srcf/{folder}/{filedic['name']}/{filename}",
                          "wb") as f:
                    f.write(cont)
                    filelists["blocks"].append(filename)
                    filelists["allfiles"].append(filename)
                texts += f"{filename},ok\n"
            else:
                texts += f"{filename},failed\n"
    fp.write(json.dumps(filelists,ensure_ascii=False))
    fp.close()
    return texts


def __blockReader(blockurl, blocks) -> "bytes,str":
    blockfile = __getmidstring(blockurl, "//", "/")
    _, filename = os.path.split(blockurl)
    if not os.path.exists(f"srcf/blocks/{blockfile}.block"):  #不存在就下载
        co = 0
        for i in blocks:
            if i["name"] == blockfile:
                try:
                    cont = requests.get(i["url"],stream=True)
                    if cont.status_code != 200:
                        return None, "failed"
                except:
                    return None, "failed"
                with open(f"srcf/blocks/{blockfile}.block", "wb") as f:
                    for chunk in cont.iter_content(chunk_size=1024):
                        f.write(chunk)
                co += 1
                break
        if co == 0:
            return None, "failed"
    tar = tarfile.open(f"srcf/blocks/{blockfile}.block")  #从block文件中取出引用文件
    for i in tar.getmembers():
        if i.name == filename:
            f = tar.extractfile(i)
            content = f.read()
            return content, "ok"
    return None, "failed"


def __getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
