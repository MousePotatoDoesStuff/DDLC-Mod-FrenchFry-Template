
"""renpy
init -23 python:
"""
class DebugLog:
    base_path=""
    def __init__(self, path:str="./debug.txt", delimiter:str=", "):
        if path.startswith("./"):
            path=self.base_path+path[1:]
        self.path=path
        self.delimiter=delimiter
    
    def reset(self):
        with open(self.path,"w") as file:
            pass
    
    def print(self, *args, delimiter:str=None):
        delimiter=self.delimiter if delimiter is None else delimiter
        raw_list=[]
        for el in args:
            raw_list.append(str(el))
        raw=delimiter.join(raw_list)
        with open(self.path,"a") as file:
            file.write("\n"+raw)
DEBUG=DebugLog()

if __name__ == '__main__':
    pass