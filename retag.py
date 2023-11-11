#!/usr/bin/env python3

import os
import json
import glob
import subprocess
import argparse
import pyfiglet
from rich import print

print("""[green]
██████╗ ███████╗████████╗ █████╗  ██████╗    ██████╗ ██╗   ██╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝
██████╔╝█████╗     ██║   ███████║██║  ███╗   ██████╔╝ ╚████╔╝ 
██╔══██╗██╔══╝     ██║   ██╔══██║██║   ██║   ██╔═══╝   ╚██╔╝  
██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝██╗██║        ██║   
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝        ╚═╝
[/green]""")
print("by [red]parnex[/red]")

arguments = argparse.ArgumentParser()
arguments.add_argument("-i", '--input', dest="input", help="Original Group/Release Tag.", required=True)
arguments.add_argument("-o", '--output', dest="output", help="Your Group/Release Tag.", required=True)
args = arguments.parse_args()

input_rls = str(args.input)
output_rls = str(args.output)

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)

input_folder = os.path.join(dirPath, 'input')
output_folder = os.path.join(dirPath, 'output')
delete_folder = os.path.join(dirPath, 'output')

with open("config.json") as json_data:
    config = json.load(json_data)

os.chdir(input_folder)

list1 = []
for file in glob.glob("*.mkv"):
    mkv_files = file
    if mkv_files.find(input_rls) != -1:
        list1.append(file)
    else:
        pass

list2 = []
for j in list1:
    final_file_name = j.replace(input_rls, output_rls)
    list2.append(final_file_name)

for k in range(0, len(list2)):
    mkv_title = list2[k][0:-4]
    print(f'\nSelected File : [yellow]{list1[k]}[/yellow]\n')
    subprocess.run(
        f'mkvmerge -o {output_folder}/{list2[k]} --title {mkv_title} --track-name 0:"" --track-name 1:"" {list1[k]}',
        shell=True)
    print('\nRetagged Successfully!')
    print(f'Original : [blue]{list1[k]}[/blue]')
    print(f'Retagged : [green]{list2[k]}[/green]\n')

os.chdir(output_folder)

list3 = []
for file in glob.glob("*.mkv"):
    mkv_files = file
    list3.append(file)

if config['rclone_upload'] == 'True':
    if len(list3) > 1:
        destination_dir = os.path.join(output_folder, mkv_title)
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)
            os.system(f'mv {output_folder}/* {destination_dir}')
            print('\nUploading...')
            subprocess.run(
                f"gclone copy {destination_dir}/ {config['rclone_remote']}: --progress --transfers 20 --drive-chunk-size 128M",
                shell=True)
            print('\nUpload Complete')
        else:
            print(f"Destination Directory '{destination_dir}' Already Exists!")
    else:
        print('\nUploading...')
        subprocess.run(
            f"gclone copy {output_folder}/ {config['rclone_remote']}: --progress --transfers 20 --drive-chunk-size 128M",
            shell=True)
        print('\nUpload Complete.')
else:
    pass
    
