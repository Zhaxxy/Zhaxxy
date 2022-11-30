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

def ftpdownload(HOST, PORT, FILE, DIR='', DESTINATION_NAME=''): #download a file from ftp, you must define the dir though or just looks in root
    ftp = FTP()
    ftp.connect(HOST, int(PORT))
    ftp.login()

    if not DIR == '':
        ftp.cwd(DIR)
    if DESTINATION_NAME == '':
        ftp.retrbinary("RETR " + FILE ,open(FILE, 'wb').write)
        ftp.close()
    else:
        ftp.retrbinary("RETR " + FILE ,open(DESTINATION_NAME, 'wb').write)
        ftp.close()

def ftpupload(HOST, PORT, FILE, DIR='', REAL_NAME=''): #upload file to ftp server, must define a dir though or just looks in root
    ftp = FTP()
    ftp.connect(HOST, int(PORT))
    ftp.login()

    if not DIR == '':
        ftp.cwd(DIR)
    if REAL_NAME == '':
        ftp.storbinary('STOR ' + FILE, open(FILE, 'rb'))
        ftp.close()
    else:
        ftp.storbinary('STOR ' + FILE, open(REAL_NAME, 'rb'))
        ftp.close()
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

#last but not least, a function specfically for lbp modding, was not made by me 

def pack12_11_1(normal): #no clue what it does but it converts normals into the format lbp uses, does some magic and gives an integer do be converted into bytes
    x = round(normal[0] * 0x7ff) & 0xfff;
    y = round(normal[1] * 0x3ff) & 0x7ff
    z = int(normal[2] < 0)
    return (x | (y << 12) | (z << 23))

# print(pack12_11_1([-0.9255, 0.0782, -0.3707])) #does some magic and gives an integer do be converted into bytes
