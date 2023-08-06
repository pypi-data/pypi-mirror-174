import json
import os
import uuid


def openSourceFile(name):
    """
    v1.2.0版本后启用
    返回 json
    """
    js = None
    if not os.path.exists(name):
        with open(name, "w", encoding="utf-8") as f:
            f.write("{}")
    with open(name, "r", encoding="utf-8") as f:
        js = json.loads(f.read())
    return js


def addFile(srcfile, floder, filename):
    """
    v1.2.0版本后启用
    用于添加一个文件
    会给文件添加一个uuid
    """
    dic = {}
    dic["name"] = filename
    dic["uuid"] = str(uuid.uuid4())
    dic["urls"] = []
    if floder not in srcfile:
        srcfile[floder] = []
    for i in srcfile[floder]:
        if i["name"] == filename:
            return srcfile
    srcfile[floder].append(dic)
    return srcfile


def addLink(srcfile, floder, filename, link):
    """
    v1.2.0版本后启用
    用于给文件添加链接
    """
    flo = srcfile[floder]
    for i in flo:
        if i["name"] == filename:
            i["urls"].append(link)
            i["urls"] = list(set(i["urls"]))
            break
    return srcfile


def addKV(srcfile, floder, filename, key, value):
    """
    v1.2.0版本后启用
    用于给文件添加其他数据
    """
    flo = srcfile[floder]
    for i in flo:
        if i["name"] == filename:
            i[key] = value
            break
    return srcfile


def addBlock(srcfile, blockname):
    """
    v1.2.0版本后启用
    用于添加Block
    """
    if "blocks" not in srcfile:
        srcfile["blocks"] = []
    dic = {}
    dic["name"] = blockname
    dic["url"] = ""

    for i in srcfile["blocks"]:
        if i["name"] == blockname:
            return srcfile
    srcfile["blocks"].append(dic)
    return srcfile


def addBlockLink(srcfile, blockname, link):
    """
    v1.2.0版本后启用
    用于给Block添加链接
    """
    flo = srcfile["blocks"]
    for i in flo:
        if i["name"] == blockname:
            i["url"] = link
            break
    return srcfile


def save(name,srcfile):
    """
    name是文件名
    将json保存进数据库
    """
    with open(name,"w",encoding="utf-8") as f:
        f.write(json.dumps(srcfile,ensure_ascii=False))