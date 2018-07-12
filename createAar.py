# import os,zipfile,shutil,sys
import sys, getopt,os,shutil,uuid
import zipfile
version = 1.0

manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.google"
    android:versionCode="1"
    android:versionName="1.0" >
</manifest>
'''

def usage():
    print("version",version,"\n")
    print("usage: python3 createAar.py --so=soPath --jar=jarPath -o outputDir")
    print("可选参数:")
    print("-n","指定目标aar文件名")

opts, args = getopt.getopt(sys.argv[1:], "ho:n:",["version", "jar=","so="])
input_file=""
jar_path=""
so_path=""
output_path=""
output_name=""
for op, value in opts:
    if op == "--jar":
        jar_path = os.path.expanduser(value)
    elif op == "--so":
        so_path = os.path.expanduser(value)
    elif op == "-h":
        usage()
        sys.exit()
    elif op == "-o":
        output_path = value
    elif op == "-n":
        output_name = value
uid = str(uuid.uuid1())

# zfile = zipfile.ZipFile(output_file,'w',zipfile.zlib.DEFLATED)
tempdic = os.path.join(os.path.expanduser('~'),'.createaar',uid)
os.makedirs(tempdic)
print('tempdic path',tempdic)
so_buffer_path = os.path.join(tempdic,'jni','armeabi')
os.makedirs(so_buffer_path)
manifest_buffer_path = tempdic
mani_file = open(os.path.join(manifest_buffer_path,'AndroidManifest.xml'),'w')
mani_file.write(manifest)
mani_file.close()
print('so path',so_buffer_path)
jar_buffer_path = os.path.join(tempdic,'libs')
os.makedirs(jar_buffer_path)
print('jar path',jar_buffer_path)
shutil.copy(so_path,so_buffer_path)
shutil.copy(jar_path,jar_buffer_path)

if not output_name.strip():
    output_name = "aarlib"
shutil.make_archive(os.path.join(output_path,output_name),'zip',tempdic)
os.renames(os.path.join(output_path,output_name+'.zip'),os.path.join(output_path,output_name+'.aar'))

