import os
from pathlib import Path
import shutil

class Files:

    def __init__(self, homedir=None):
        if homedir:
            os.chdir(Path.home())

        self.directoryName = os.getcwd().split("\\")[-1]
        self.children = self.__generateChildren__()

    def __generateChildren__(self):
        objects = os.listdir()
        children = []
        for object in objects:
            isdir = False
            name = object

            if os.path.isdir(object):
                isdir = True

            permission = True
            dir = os.getcwd()
            if isdir:
                try:
                    self.cd(object, True)
                except PermissionError:
                    permission = False

            os.chdir(dir)
            if not isdir:
                try:
                    open(os.getcwd() + "\\" + object)
                except PermissionError:
                    permission = False


            children.append(Child(isdir, name, permission))
        return children

    def cd(self, newdir, permCheck=None):
        if newdir == ".." or newdir == "../":
            os.chdir(os.path.dirname(os.getcwd()))
            return Files()
        else:
            abspath = os.path.abspath(newdir)
            os.chdir(abspath)
            if permCheck:
                return None
            else:
                return Files()

    def lf(self, f):
        os.startfile(f)

    def copy(self, name):
        abspath = os.getcwd() + "\\" + name
        return ClipBoard(abspath, name)

    def paste(self, clip):
        try:
            if os.path.isdir(clip.path):
                shutil.copytree(clip.path, os.getcwd() + "\\" + clip.name)
            else:
                shutil.copyfile(clip.path, os.getcwd() + "\\" + clip.name)
            return True

        except PermissionError:
            # print(PermissionError.with_traceback(self, None))
            return False


class ClipBoard:

    def __init__(self, path, name):
        self.path = path
        self.name = name


class Child:

    def __init__(self, isdirectory, name, permission):
        self.isdirectory = isdirectory
        self.name = name
        self.permission = permission

#
# f = Files(True)
# clipboard = None
#
# while True:
#     print(os.getcwd())
#     print("Children:")
#     for child in f.children:
#         print(child.name)
#         print("perm: ", child.permission)
#     print()
#     print("Options:")
#     print("1: cd")
#     print("2: launch file")
#     print("3: copy")
#     print("4: paste")
#     print()
#
#     i = input("Your selection: ")
#
#     i.strip()
#     if i == "1":
#         dir = input("Directory to change into: ")
#         dir.strip()
#         for child in f.children:
#             if child.name == dir:
#                 if child.permission:
#                     f = f.cd(child.name)
#                     break
#                 else:
#                     print("Hey you don't have permission!")
#                     break
#             elif dir == ".." or dir == "../":
#                 f = f.cd(dir)
#                 break
#
#     elif i == "2":
#         dir = input("File to execute: ")
#         dir.strip()
#         for child in f.children:
#             if child.name == dir:
#                 f.lf(child.name)
#                 break
#     elif i == "3":
#         dir = input("File or directory to copy: ")
#         dir.strip()
#         for child in f.children:
#             if child.name == dir:
#                 clipboard = f.copy(child.name)
#                 break
#
#     elif i == "4":
#         if clipboard is not None:
#             print(clipboard.path)
#             if f.paste(clipboard):
#                 print("yay this worked!")
#             else:
#                 print("boo this did not work")
#         else:
#             print("Nothing in clipboard!")
