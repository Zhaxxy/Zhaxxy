# heres a list of functions which ive made over looking over guides online, have fun using them!
# theese functions are not error safe, use them with caution!

##################################################



def integer2hex(integer, nibbleSIZE):
    return hex(integer)[2:].rjust(int(nibbleSIZE), '0') # this one is simple, it converts a integer to a hex string and pads it out so it will fill any storage you need it to
# print(integer2hex(43, 2)) #example will give '002b' as it will be padded to 2 nibbles (4 bytes)


def swap_endianness(hexstring):   # bit more complex but it converts a hex string into little endian or big endian depending on what it was first
    ba = bytearray.fromhex(hexstring)
    ba.reverse()
    sba = ''.join(format(x, '02x') for x in ba)
    abatwo = sba.upper()
    return abatwo
# print(swap_endianness('aabbed')) # will give 'edbbaa' instead of debbaa


import os
def silentfolder(thesussydir): #deletes a folder, if it doesnt find the folder then it does nothing (no throwing error!)
    if os.path.exists(thesussydir) and os.path.isdir(thesussydir):   
        shutil.rmtree(thesussydir)

import os
import os, errno
def silentremove(filetobedeleted): #not by me this function
    try:
        os.remove(filetobedeleted)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

############################################################################################################################################
import os
def silentdeleteprefix(nameprefix): #this version looks for for files with a prefix and deletes them in the same dir as the script
    my_dir = os.path.dirname(os.path.realpath(__file__))
    for fname in os.listdir(my_dir):
        if fname.startswith(nameprefix):
            os.remove(os.path.join(my_dir, fname))
            
def silentdeleteprefix(nameprefix, my_dir): #is very similar to other one expect you define the dir (rerember you need \\ instead of \)
    for fname in os.listdir(my_dir):
        if fname.startswith(nameprefix):
            os.remove(os.path.join(my_dir, fname))
############################################################################################################################################

def write_to_line(file, lineNUM, textwrite,zeroequalsone=True): # write to a line in a file, should be in same dir
    if zeroequalsone: lineNUM -= 1 #if you dont like starting with 0, it takes away, does this by deafult but you can change if you must
    if lineNUM < 0: lineNUM = 0
    # with is like your try .. finally block in this case
    with open(file, 'r') as bob:
        # read a list of lines into data
        data = bob.readlines()



    # now change the 2nd line, note that you have to add a newline
    data[lineNUM] = textwrite + '\n'

    # and write everything back
    with open(file, 'w') as tod:
        tod.writelines(data)


############################################################################################################################################
from ftplib import FTP

def ftp_login_and_connect(HOST, PORT=21): #simple function used to login in anymouslly to a ftp server
    ftp = FTP()
    ftp.connect(HOST, PORT)
    ftp.login()
    return ftp

def ftpdownload(ftp, FILE, DIR='', DESTINATION_NAME=''): #download a file from ftp, you must define the dir though or just looks in root
    old_mememory = ftp.pwd()
    if not DIR == '':
        ftp.cwd(DIR)
    
    if DESTINATION_NAME == '':
        ftp.retrbinary("RETR " + FILE ,open(FILE, 'wb').write)
    else:
        ftp.retrbinary("RETR " + FILE ,open(DESTINATION_NAME, 'wb').write)
    ftp.cwd(old_mememory)

def ftpupload(ftp, FILE, DIR='', REAL_NAME=''): #upload file to ftp server, must define a dir though or just looks in root
    old_mememory = ftp.pwd()
    if not DIR == '':
        ftp.cwd(DIR)
    
    if REAL_NAME == '':
        ftp.storbinary('STOR ' + FILE, open(FILE, 'rb'))
    else:
        ftp.storbinary('STOR ' + FILE, open(REAL_NAME, 'rb'))
    ftp.cwd(old_mememory)

def list_all_files_in_folder_ftp(ftp,source_folder=''): #gets a list of all the folders and files in a folder (inlcuding subdirs), this one took me a while to make!
    def get_list_LIST(path=source_folder):
        lines = []
        ftp.retrlines('LIST ' +path , lines.append)
        lines.pop(0); lines.pop(0) #ill come up with a cleaner method later, get rid of useless non files
        return lines

    old_mememory = ftp.pwd()
    filesnfolders = []
    ftp.cwd(source_folder)

    def recur_over_folder(list,path=source_folder):
        for file in get_list_LIST(path):
            clean_path = f'{path}/{file.split()[-1]}'
            if clean_path in filesnfolders: continue
            else: filesnfolders.append(clean_path)
            if not file.startswith("-"): #again need a cleaner method, used to detirmine if its a file or folder, if it starts with - then its a file
                ftp.cwd(f'{path}/{file.split()[-1]}')
                recur_over_folder(filesnfolders,f'{path}/{file.split()[-1]}')
    recur_over_folder(filesnfolders)
    ftp.cwd(old_mememory)
    return filesnfolders

from ftplib import error_reply
def ftp_delete_file(ftp: FTP, ftp_path: str):
    try:
        ftp.delete(ftp_path)
    except error_reply as e:
        if not e.args[0].startswith('226'): # this is soo idiotic, why does it even raise that error?
            raise


def delete_folder_contents(ftp: FTP, folder_with_stuff: str):
    old_memory = ftp.pwd()
    ftp.cwd(folder_with_stuff)
    
    for file in list_all_files_in_folder_ftp(ftp,folder_with_stuff):
        if file[1]:
            ftp_delete_file(ftp,file[0])
    
    for folder in list_all_files_in_folder_ftp(ftp,folder_with_stuff):
        assert not folder[1], 'we should of already deleted all files!'
        ftp.rmd(folder[0])
        
    ftp.cwd(old_memory)

############################################################################################################################################
import os
import shutil
def ftp_download_folder_wget(HOST,PORT,DIR): #needs wget to be installed
    if not DIR.startswith("/"): DIR = "/" + DIR
    PORT = str(PORT)
    os.system("wget -r ftp://"+ HOST +":"+ PORT + DIR +"*")
    DIR = DIR.replace("/","\\")
    shutil.move(HOST +"+"+PORT+DIR,DIR.split('\\')[-1])
    shutil.rmtree(HOST +"+"+PORT)
############################################################################################################################################
import zipfile
def get_uncompressed_zip_size(file,SI='mb'):
    zp = zipfile.ZipFile(file)
    size = sum([zinfo.file_size for zinfo in zp.filelist])
    SI = SI.upper()
    if SI == 'KB': return float(size) / 1000
    if SI == 'MB': return float(size) / 1000000
    if SI == 'GB': return float(size) / 1000000000
    return float(size)

import re
def get_substring_regex(substring,same_subsubstringsTUPLE):
    for index, subsub in enumerate(same_subsubstringsTUPLE): #making the group
        if re.match(r'^[a-zA-Z0-9]*$',subsub) is None: subsub = '\\' + subsub #< saftey check
        if index == 0: group = '(?:' + subsub + '|'
        elif index == len(same_subsubstringsTUPLE)-1: group += subsub+')'
        else: group += subsub + '|'
    the_regex = ''
    for character in substring:
        if re.match(r'^[a-zA-Z0-9]*$',character) is None: character = '\\' + character #< saftey check
        if character not in same_subsubstringsTUPLE: the_regex += character
        else: the_regex += group
    return the_regex

# simple function to check if a string is a valid ps4 title id
def is_ps4_title_id(input_str: str,/) -> bool: 
    return input_str.startswith('CUSA') and len(input_str) == 9 and input_str[-5:].isdigit()


#last but not least, a function specfically for lbp modding, was not made by me 

def pack12_11_1(normal): #no clue what it does but it converts normals into the format lbp uses, does some magic and gives an integer do be converted into bytes
    x = round(normal[0] * 0x7ff) & 0xfff;
    y = round(normal[1] * 0x3ff) & 0x7ff
    z = int(normal[2] < 0)
    return (x | (y << 12) | (z << 23))

# print(pack12_11_1([-0.9255, 0.0782, -0.3707])) #does some magic and gives an integer do be converted into bytes
