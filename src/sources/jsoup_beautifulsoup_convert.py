rul = r"class.odd.0@tag.a.0@text||tag.dd.0@tag.h1@text##全文阅读"
print(rul.split("@"))
# basic_rule（用.分割）
# [第一部分] class, id, tag, text, 不需要后续规则，返回所有子标签:children
# [第二部分] 元素名称，但是 text.<xxx> <xxx>为文本内容得一部分
# [第三部分] 位置(大概是第几个？如果没有这一部分会获取所有) 0为第一个，-1,1一样
# '!'=>非
# '-'=>倒序
# @的最后一段为获取内容,如text,textNodes,ownText,href,src,html,all等
# 如需要正则替换在最后加上 ##正则表达式##替换内容，替换内容为空时，第二个##可以省略
