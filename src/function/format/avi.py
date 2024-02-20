import inspect
import re
from src.toml_config import config


# 存储关键信息的类


class Name:
    def __init__(self):
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        self.caller_name = caller_module.__name__
        self.default_url = '/' + str(self.caller_name).replace("src.server.event.", "").replace(".", "/")


def is_valid_email(email):
    regex=""
    if config.server.strict:
        # regex for email address
        regex = r'^[\w.%+-]+@(gmail\.com|outlook\.com|yahoo\.com|msn\.com|hotmail\.com|aol\.com|ask\.com|live\.com|qq\.com|0355\.net' \
                      r'|163\.com|163\.net|263\.net|3721\.net|yeah\.net|googlemail\.com|mail\.com|aim\.com|walla\.com|inbox' \
                      r'\.com|126\.com|sina\.com|21cn\.com|sohu\.com|yahoo\.com\.zh_CN|tom\.com|etang\.com|eyou\.com|56\.com|' \
                      r'x' \
                      r'\.zh_CN|chinaren\.com|sogou\.com|citiz\.com|hongkong\.com|ctimail\.com|hknet\.com|netvigator\.com|' \
                      r'mail' \
                      r'\.hk\.com|swe\.com\.hk|ITCCOLP\.COM\.HK|BIZNETVIGATOR\.COM|SEED\.NET\.TW|TOPMARKEPLG\.COM\.TW|PCHOME' \
                      r'\.COM\.TW|hinet\.net\.tw|cyber\.net\.pk|omantel\.net\.om|libero\.it|webmail\.co\.za|xtra\.co\.nz' \
                      r'|pacific\.net\.sg|FASTMAIL\.FM|emirates\.net\.ae|eim\.ae|net\.sy|scs-net\.org|mail\.sy|ttnet\.net\.tr' \
                      r'|superonline\.com|yemen\.net\.ye|y\.net\.ye|cytanet\.com\.cy|aol\.com|netzero\.net|twcny\.rr\.com' \
                      r'|comcast\.net|warwick\.net|cs\.com|verizon\.net|bigpond\.com|otenet\.gr|vsnl\.com|wilnetonline\.net' \
                      r'|cal3\.vsnl\.net\.in|rediffmail\.com|sancharnet\.in|NDF\.VSNL\.NET\.IN|DEL3\.VSNL\.NET\.IN|xtra\.co' \
                      r'\.nz|yandex\.ru|t-online\.de|NETVISION\.NET\.IL|BIGPOND\.NET\.AU|MAIL\.RU|EV|ADSL\.LOXINFO\.COM|SCS' \
                      r'-NET\.ORG|EMIRATES\.NET\.AE|QUALITYNET\.NET|ZAHAV\.NET\.IL|netvision\.net\.il|xx\.org\.il|hn\.vnn\.vn' \
                      r'|hcm\.fpt\.vn|hcm\.vnn\.vn|candel\.co\.jp|zamnet\.zm|amet\.com\.ar|infovia\.com\.ar|mt\.net\.mk' \
                      r'|sotelgui\.net\.gn|prodigy\.net\.mx|citechco\.net|xxx\.meh\.es|terra\.es|wannado\.fr|mindspring\.com' \
                      r'|excite\.com|africaonline\.co\.zw|samara\.co\.zw|zol\.co\.zw|mweb\.co\.zw|aviso\.ci|africaonline\.co' \
                      r'\.ci|afnet\.net|mti\.gov\.na|namibnet\.com|iway\.na|be-local\.com|infoclub\.com\.np)$'
    elif not config.server.strict:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex, email) is not None
