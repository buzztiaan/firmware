# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#
# utils.py - Misc utils. My favourite kind of source file.
#
import gc, sys

class imported:
    # Context manager that temporarily imports
    # a list of modules.
    # LATER: doubtful this saves any memory when all the code is frozen.

    def __init__(self, *modules):
        self.modules = modules

    def __enter__(self):
        # import everything required
        rv = tuple(__import__(n) for n in self.modules)

        return rv[0] if len(self.modules) == 1 else rv

    def __exit__(self, exc_type, exc_value, traceback):

        for n in self.modules:
            if n in sys.modules:
                del sys.modules[n]

        # recovery that tasty memory.
        gc.collect()

# class min_dramatic_pause:
#     # insure that something takes at least N ms
#     def __init__(self, min_time):
#         import utime
# 
#         self.min_time = min_time
#         self.start_time = utime.ticks_ms()
#     
#     def __enter__(self):
#         pass
# 
#     def __exit__(self, exc_type, exc_value, traceback):
#         import utime
# 
#         if exc_type is not None: return
# 
#         actual = utime.ticks_ms() - self.start_time
#         if actual < self.min_time:
#             utime.sleep_ms(self.min_time - actual)
# 

def pretty_delay(n):
    # decode # of seconds into various ranges, need not be precise.
    if n < 120:
        return '%d seconds' % n
    n /= 60
    if n < 60:
        return '%d minutes' % n
    n /= 60
    if n < 48:
        return '%.1f hours' % n
    n /= 24
    return 'about %d days' % n

def pop_count(i):
    # 32-bit population count for integers
    # from <https://stackoverflow.com/questions/9829578>
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)

    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

def get_filesize(fn):
    # like os.path.getsize()
    import uos
    return uos.stat(fn)[6]

class HexWriter:
    # Emulate a file/stream but convert binary to hex as they write
    def __init__(self, fd):
        self.fd = fd

    def __enter__(self):
        self.fd.__enter__()
        return self

    def __exit__(self, *a, **k):
        self.fd.write('\r\n')
        return self.fd.__exit__(*a, **k)

    def write(self, b):
        for ch in b:
            self.fd.write('%02x' % ch)


# EOF
