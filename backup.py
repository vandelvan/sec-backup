from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from os import system
from datetime import datetime

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

print("Creando respaldo...")
now = str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
fname = "sec-backup-"+now+".zip"
system("tar -czf "+fname+" /home/$USER")

print("Subiendo respaldo a drive...")
drive = GoogleDrive(gauth)
bkup = drive.CreateFile()
bkup.SetContentFile(fname)
bkup.Upload()

print("Respaldo creado!", fname)

print("Desea descargar un respaldo anterior?")
print("1. Si")
print("2. No")
selec = int(input())
if selec == 1:
    print("Seleccione el archivo a descargar:")
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    i = 1
    for file1 in file_list:
        if file1['title'].find("sec-backup") != -1:
            print(str(i)+". "+file1['title'])
            i = i+1
    selec = int(input())
    i = 1
    idSelec = 0
    for file1 in file_list:
        if file1['title'].find("sec-backup") != -1:
            if selec == i:
                idSelec = file1['id']
                nameSel = file1['title']
                break
            i = i+1
    if idSelec != 0:
        print("Descargando...")
        file2 = drive.CreateFile({'id': idSelec})
        file2.GetContentFile(nameSel)
        print("Listo!")
    else:
        print("No encontrado")
else:
    print("Gracias por usar sec-backup!")