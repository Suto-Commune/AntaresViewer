import random
import string


def random_string():
    # 可包含的字符集合（字母、数字和符号）
    characters = string.ascii_letters + string.digits + string.punctuation

    # 生成随机字符串
    random_string1 = ''.join(random.choice(characters) for _ in range(15))

    return str(random_string1)
