import os


def summary(file_name):
    file_name = file_name[:-5]
    code_r = open(os.path.join(os.path.dirname(__file__), "input", file_name + ".java"), "r", encoding='utf8').read()
    code = code_r.replace("−", "-").replace("”", '"')

    def find(class_code, spaces, keyword):
        code_temp = class_code[class_code.find(spaces + keyword):]
        a = code_temp.split(spaces + keyword)
        a = a[1:]
        v = []
        f = []
        for i in range(len(a)):
            temp1 = a[i].find("{")
            temp0 = a[i].find("\n")
            if temp1 == -1 or temp0 < temp1:
                v.append(a[i][1:None if temp0 == -1 else temp0])
            else:
                f.append(a[i][1:temp1])
        return f, v

    code_temp = code[code.find("class " + file_name):]
    class_name = code_temp[:code_temp.find("\n") - 2]
    temp0 = code.find(file_name)
    temp1 = code[temp0:].find("\n")
    code = code[temp0 + temp1:]
    output = "/*\n * " + class_name + ":"
    o_v = ""
    o_f = ""
    is_v = False
    is_f = False
    for i in ["public", "private", "protected"]:
        f, v = find(code, "\n    ", i)
        if len(v) > 0:
            is_v = True
            o_v += "\n *   " + i + ":"
            for j in v:
                o_v += "\n *       " + j
        if len(f) > 0:
            is_f = True
            o_f += "\n *   " + i + ":"
            for j in f:
                o_f += "\n *       " + j
    if is_v:
        o_v = "\n *\n * VARIABLES:" + o_v
    if is_f:
        o_f = "\n * METHODS:" + o_f
    output += o_v + "\n *" + o_f
    if code.find("-- nested") != -1:
        output += "\n *\n * NESTED CLASSES"
        a = code.split("-- nested")[1:]
        a = list(map(lambda i: i[0:i.find("end of nested")], a))
        for n in range(len(a)):
            is_v = False
            is_f = False
            o_v = ""
            o_f = ""
            a[n] = a[n][1:]
            name_class = a[n][:a[n].find(" ")]
            a[n] = a[n][a[n].find("\n") + 1:]
            code_temp = a[n][a[n].find("class " + name_class):]
            class_name = code_temp[:code_temp.find("\n") - 2]
            output += "\n *\n * " + class_name + ":"
            for i in ["public", "private", "protected"]:
                f, v = find(a[n], "\n        ", i)
                if len(v) > 0:
                    is_v = True
                    o_v += "\n *       " + i + ":"
                    for j in v:
                        o_v += "\n *           " + j
                if len(f) > 0:
                    is_f = True
                    o_f += "\n *       " + i + ":"
                    for j in f:
                        o_f += "\n *           " + j
            if is_v:
                o_v = "\n *     VARIABLES:" + o_v
            if is_f:
                o_f = "\n *     METHODS:" + o_f
            output += o_v + o_f
    output += "\n * */\n\n"
    open(os.path.join(os.path.dirname(__file__), "output", file_name + ".java"), "w", encoding='utf8').write(
        output + code_r)


file_list = os.listdir(os.path.join(os.path.dirname(__file__), "input"))
for i in file_list:
    print(i)
    summary(i)
