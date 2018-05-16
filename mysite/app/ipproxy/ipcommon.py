# -*- coding: utf-8 -*-
import socket

# 校验IP，端口是否可用
def checkIpCon(ip, prot):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)
    try:
        sk.connect((ip, prot))
        return True
    except Exception:

        pass
    sk.close()
    return False