#import zipfile
import os
import sys
import subprocess

def copyFiles(path, target_dir):
    obj = os.scandir(path)
    for entry in obj:
        if entry.is_dir():
            copyFiles(path+"/"+entry.name, target_dir)
        elif entry.is_file():
            if(entry.name.endswith('Twitter.java')):
                fname = path+"/"+entry.name
                target_name = target_dir+'_'+entry.name
                subprocess.run(['cp',fname,target_name])

def mergeDir(path):
    if(len(os.listdir(path)) != 1):
        return
    entry = list(os.scandir(path))[0]
    fname = path+"/"+entry.name
    subprocess.run(f"mv {fname}/* {path}",shell=True)

# def unzip_files(zip_path, target_dir):
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(target_dir)

directory_path = sys.argv[1]
output_path = sys.argv[2]
file_list = os.listdir(directory_path)

for file in file_list:
    out_name = ""
    if(file.endswith('.zip')):
        fname = directory_path+'/'+file
        out_name = output_path+'/'+file[:-4]
        subprocess.run(['unzip',fname,'-d',out_name])
    elif(file.endswith('.tgz') or file.endswith('.tar')):
        fname = directory_path+'/'+file
        out_name = output_path+'/'+file[:-4]
        subprocess.run(['mkdir',out_name])
        subprocess.run(['tar','xfz',fname,'-C',out_name])
    elif(file.endswith('.rar')):
        fname = directory_path+'/'+file
        out_name = output_path+'/'+file[:-4]
        subprocess.run(['mkdir',out_name])
        subprocess.run(['unrar','x',fname,out_name])
    elif(file.endswith('.7z')):
        fname = directory_path+'/'+file
        out_name = output_path+'/'+file[:-4]
        subprocess.run(['7z','x',fname,'-o'+out_name])
    else:
        continue
    mergeDir(out_name)
    # copyFiles(out_name,out_name)
    # subprocess.run(['rm','-rf',out_name])
