import time
import csv
import os
from random import randint
if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")

identifier = randint(0, 10000)
DOWNLOADS = get_download_folder()
PATH = input('Drag and drop file here: ')
print('Formatting')
try:
    f = open(PATH)
    csv_f = csv.reader(f)
    new = []
    for row in csv_f:
        if 'GMAIL' in row:
            row[0] = 'Username'
        if 'PASSWORD' in row:
            row[1] = 'Password'
        if 'RECOVERY EMAIL' in row:
            row[2] = 'Recovery Email'
        row.pop(3)
        row = row[0:4]
        new.append(row)
    f.close()

    directory = f'{DOWNLOADS}\converted_gmails_{identifier}.csv'

    with open(directory, 'w', newline='') as f:
        output = csv.writer(f)
        for row in new:
            output.writerow(row)
        f.close()
    os.remove(PATH)
    print(f'AYCD/Kylin import formatted: {directory}')
except:
    print('Something\'s not quite right, please try again and import a file from Dispurgen Export')
