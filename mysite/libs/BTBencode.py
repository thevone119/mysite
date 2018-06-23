# -*- coding: utf-8 -*-
'''
实现BT种子转磁性链接
'''
import bencode
import sys
import hashlib
import base64
import urllib


def BTfileToCode(btfile=None):
    # 读取种子文件
    torrent = open(btfile, 'rb').read()
    return BTByteToCode(torrent)

def BTByteToCode(torrent=None):
    # 计算meta数据
    metadata = bencode.bdecode(torrent)
    hashcontents = bencode.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    return 'magnet:?xt=urn:btih:'+str(b32hash)