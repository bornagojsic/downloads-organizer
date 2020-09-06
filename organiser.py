import re
import os


## --------------------------------------------------------------------------------------

## Code from StackOverflow
## https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder

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
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

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

## --------------------------------------------------------------------------------------


def make(name):
	try:
		os.mkdir(name)
	except FileExistsError:
		pass


folders = [
			['Zip files', 
			'.zip .rar .7z'],
			['Font files', 
			'.otf .ttf .woff'],
			['Word files', 
			'.doc .docx .docm .dot .dotx .dotm .odt'],
			['Excel files', 
			'.xls .xlsx .xlsm .xlsb .xlt .xltx .xltm .xla .xlam .ods'],
			['Powerpoint files', 
			'.ppt .pptx .pptm .pot .potx .potm .pps .ppsx .ppsm .ppa .ppax .odp'],
			['PDF files', 
			'.pdf'],
			['Executable files',
			'.exe'],
			['Icon files',
			'.ico'],
			['Cursor files',
			'.ani .cur'],
			['Image files',
			'.png .gif .jpg .jpeg .jpe .jfif .tif .tiff .bmp .dib .heic'],
			['Python files',
			'.py'],
			['C/C++ files',
			'.c .h .cpp .hpp .cxx .hxx .cc .hh'],
		]

path = get_download_folder()

os.chdir(path)

directory = os.listdir(path)

# file_names = [re.findall(r'.+\.', file)[0][::-1][1:][::-1] for file in directory]

for file in directory:
	## Chacks for duplicates
	if re.findall(r'\(.+\)\..*', file):
		os.remove(file)
	for folder in folders:
		[name, exts] = folder
		if any(file.endswith(ext) for ext in exts.split()):
			make(name)
			os.replace(f"{path}\\{file}", f"{path}\\{name}\\{file}")