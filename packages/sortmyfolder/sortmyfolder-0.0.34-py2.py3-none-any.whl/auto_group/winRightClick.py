import os
import sys
import winreg as reg

cwd = os.getcwd()

python_exe = sys.executable

key_path = r"Directory\\Background\\shell\\Organiser"

key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)

reg.setValue(key, '', reg.REG_SZ, '&Organise folder')

key1 = reg.CreateKeyEc(key, r"commad")


reg.SetValue(key1, reg.REG_SZ, python_exe +f'"{cwd}\\file_organiser.py"')



