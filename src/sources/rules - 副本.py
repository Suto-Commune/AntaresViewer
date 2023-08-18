class Method:
    def __init__(self, how: str, what: list):
        self.how = how
        self.what = what


def rule(string: str):
    # string = "-4hsnnatsumi " + string
    # xpath
    if "@XPath:" in string or "//" in string:
        return [Method("Xpath", [string.replace("@XPath:", "")])]
    else:
        return_list = []
        for i in string.split("@"):
            if "$." in i.split('.')[0]:
                return_list.append(Method("JSONPath", i.replace("$.", "").split(".")))
                ...
            match i.split(":")[0]:
                case "css":
                    return_list.append(Method("JsoupCSS", [i.replace("@css:", "")]))
                    ...
                case "json":
                    return_list.append(Method("JSONPath", i.replace("$.", "").split(".")))
                    ...
                case _:
                    return_list.append(Method("Default", i.split(".")))
                    ...
        return return_list


a = rule(r"class.odd.0@tag.a.0@text||tag.dd.0@tag.h1@text##全文阅读")
for i in a:
    print(f"how={i.how},what={i.what}\n\n")
