# -*- coding: utf-8 -*-
#
#==================================================================
# 注意：Windows 下请安装32位版本的Python，否则将无法加载 Sunday.dll
#==================================================================

from ctypes import *

class Verify(object):
    def __init__(self):
        self.libpath = "baidu.lib"
        self.libpasswd = "123"

        self.dll = windll.LoadLibrary('Sunday.dll')
        load_lib_from_file = self.dll.LoadLibFromFile
        load_lib_from_file.argtypes = [c_char_p, c_char_p]
        load_lib_from_file.restypes = c_int
        self.index = load_lib_from_file(self.libpath, self.libpasswd)

    def get(self, gif_path):
        img_string = open(gif_path, "rb").read()
        img_buffer = create_string_buffer(img_string)
        ret_value = 'aaaa'
        ret_buffer = create_string_buffer(ret_value)

        get_code_from_buffer = self.dll.GetCodeFromBuffer
        get_code_from_buffer(self.index, byref(img_buffer), len(img_buffer), byref(ret_buffer))

        vcode = ret_buffer.value
        return vcode


if __name__ == "__main__":
    vcode = Verify()
    one = vcode.get('test1.gif')
    two = vcode.get('test2.gif')
    print one,two