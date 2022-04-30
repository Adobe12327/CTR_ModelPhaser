import struct
from genericpath import getsize
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter import messagebox
from tkinter.ttk import Treeview
from PIL import Image, ImageTk, ImageFile
import os
from tkinterdnd2 import DND_FILES, TkinterDnD




root = TkinterDnD.Tk()
# root.eval('tk::PlaceWindow . center')
root.title("Model Phaser")
root.resizable(False,False)
frame1 = Frame(root)
frame1.pack(side="bottom", fill="both", expand=True)
frame2 = Frame(root)
frame2.pack(side="bottom", fill="both", expand=True)
fileviewer = Label(root, text="파일을 끌어놓으세요", width=40, height=10)
fileviewer.drop_target_register(DND_FILES)
fileviewer.pack()

replacebtn = Button(frame2, text='교체', width=10)
replacebtn.pack(side='right')

parttable = Treeview(frame1, columns=["이름", "시작", "끝"], displaycolumns=["이름", "시작", "끝"], height=5)
parttable.column('#0', width=20, stretch=NO)
parttable.column("#1", width=150)
parttable.column('#2', width=80)
parttable.column('#3', width=80)
parttable.heading("이름", text="이름", anchor="center")
parttable.heading("시작", text="시작", anchor="center")
parttable.heading("끝", text="끝", anchor="center")
parttable.pack()


def read_float32(f):
    return struct.unpack('f', f.read(4))[0]

def read_float16(f):
    return round(struct.unpack('f', f.read(2))[0], 4)

def read_int32(f):
    return int.from_bytes(f.read(4), 'little')

def read_int16(f):
    return int.from_bytes(f.read(2), 'little')

class PartObj():
    def __init__(self):
        super().__init__()
        self.name = ''
        self.inherit = []
        self.start_offset = ''
        self.end_offset = ''

Objs = []
file = ''

def read_o3d(filepath):
    f = open(filepath, 'rb')
    global file
    file = filepath
    Objcount = read_int32(f)
    TextureCount = read_int32(f)
    for i in range(Objcount):
        useless = read_int32(f)
        f.read(useless)
        subMeshCount = read_int32(f)-1
        meshNameCount = read_int32(f)
        meshName = f.read(meshNameCount).decode('ISO-8859-1')
        f.read(4)
        Starting_Offset = f.tell()
        VerticesCount = read_int32(f)
        Unk2 = read_int32(f)
        IndicesCount = read_int32(f)
        f.read(4)
        startoffset = f.tell()
        f.read(((4*3)+20)*VerticesCount)
        f.seek(startoffset+(4*3))
        f.read(((4*2)+24)*VerticesCount)
        f.seek(startoffset+(4*5))
        f.read(((4*3)+20)*VerticesCount)
        f.seek(-20, 1)
        for i in range(IndicesCount):
            FaceType = read_int32(f)
            Counts = read_int32(f)
            asdf = []
            for i in range(Counts):
                read_int32(f)

        Ending_Offset = f.tell()
        Obj = PartObj()
        Obj.name = meshName
        Obj.start_offset = (str(hex(Starting_Offset)).replace('0x', '')).upper()
        Obj.end_offset = (str(hex(Ending_Offset)).replace('0x', '')).upper()

        for i in range(subMeshCount):
            meshNameCount = read_int32(f)
            meshName = f.read(meshNameCount).decode('ISO-8859-1')
            subMeshCount = read_int32(f)
            Starting_Offset = f.tell()
            VerticesCount = read_int32(f)
            Unk2 = read_int32(f)
            IndicesCount = read_int32(f)
            f.read(4)
            startoffset = f.tell()
            for i in range(VerticesCount):
                f.read(4*3)
                f.read(20)
            f.seek(startoffset+(4*3))
            for i in range(VerticesCount):
                f.read(4*2)
                f.read(24)
            f.seek(startoffset+(4*5))
            for i in range(VerticesCount):
                f.read(4*3)
                f.read(20)
            f.seek(-20, 1)
            for i in range(IndicesCount):
                FaceType = read_int32(f)
                Counts = read_int32(f)
                asdf = []
                for i in range(Counts):
                    read_int32(f)
            Ending_Offset = f.tell()
            Objj = PartObj()
            Objj.name = meshName
            Objj.start_offset = (str(hex(Starting_Offset)).replace('0x', '')).upper()
            Objj.end_offset = (str(hex(Ending_Offset)).replace('0x', '')).upper()
            Obj.inherit.append(Objj)
        Objs.append(Obj)

        f.read(36)

def read_b3d(filepath):
    f = open(filepath, 'rb')
    global file
    file = filepath
    TexturesCount = read_int32(f)
    Textures = []
    Unk1 = read_int32(f)
    for i in range(TexturesCount):
        TextureNameCount = read_int32(f)
        TextureName = f.read(TextureNameCount).decode('ISO-8859-1')
        Textures.append(TextureName)
    for i in range(16):
        if i > 2:
            f.read(4*2)
        f.seek(-4, 1)
        subMeshCount = read_int32(f)-1
        meshNameCount = read_int32(f)
        meshName = f.read(meshNameCount).decode('ISO-8859-1')
        MaterialIndex = None
        if meshName.find("lod") != -1:
            subMeshCount = 0
            f.read(4)
        else:
            MaterialIndex = read_int32(f)
        if meshName.find("lod_") != -1:
            f.read(4)
            f.read(meshNameCount)
            MaterialIndex = read_int32(f)
        Starting_Offset = f.tell()
        VerticesCount = read_int32(f)
        AllofFaceCount = read_int32(f)
        IndicesCount = read_int32(f)
        f.read(4)
        startoffset = f.tell()
        for i in range(VerticesCount):
            f.read(4*3)
            f.read(20)
        f.seek(startoffset+(4*3))
        for i in range(VerticesCount):
            f.read(4*2)
            f.read(24)
        f.seek(startoffset+(4*5))
        for i in range(VerticesCount):
            f.read(4*3)
            f.read(20)
        f.seek(-20, 1)
        for i in range(IndicesCount):
            FaceType = read_int32(f)
            Counts = read_int32(f)
            asdf = []
            for i in range(Counts):
                read_int32(f)
        Ending_Offset = f.tell()
        Obj = PartObj()
        Obj.name = meshName
        Obj.start_offset = (str(hex(Starting_Offset)).replace('0x', '')).upper()
        Obj.end_offset = (str(hex(Ending_Offset)).replace('0x', '')).upper()

        pname = meshName

        if subMeshCount != None:
            for i in range(subMeshCount):
                meshNameCount = read_int32(f)
                meshName = f.read(meshNameCount).decode('ISO-8859-1')
                MaterialIndex = read_int32(f)
                Starting_Offset = f.tell()
                VerticesCount = read_int32(f)
                AllofFaceCount = read_int32(f)
                IndicesCount = read_int32(f)
                f.read(4)
                startoffset = f.tell()
                for i in range(VerticesCount):
                    f.read(4*3)
                    f.read(20)
                f.seek(startoffset+(4*3))
                for i in range(VerticesCount):
                    f.read(4*2)
                    f.read(24)
                f.seek(startoffset+(4*5))
                for i in range(VerticesCount):
                    f.read(4*3)
                    f.read(20)
                f.seek(-20, 1)
                for i in range(IndicesCount):
                    FaceType = read_int32(f)
                    Counts = read_int32(f)
                    asdf = []
                    for i in range(Counts):
                        read_int32(f)
                Ending_Offset = f.tell()
                Objj = PartObj()
                Objj.name = meshName
                Objj.start_offset = (str(hex(Starting_Offset)).replace('0x', '')).upper()
                Objj.end_offset = (str(hex(Ending_Offset)).replace('0x', '')).upper()
                Obj.inherit.append(Objj)
            Objs.append(Obj)

        if pname == "hoo_00_1":
            f.read(88)

        if meshName.find("lod_") != -1 and meshName.find("lod_0") == -1:
            meshNameCount = read_int32(f)
            pmesh = meshName
            meshName = f.read(meshNameCount).decode('ISO-8859-1')
            MaterialIndex = read_int32(f)
            Starting_Offset = f.tell()
            VerticesCount = read_int32(f)
            AllofFaceCount = read_int32(f)
            IndicesCount = read_int32(f)
            f.read(4)
            startoffset = f.tell()
            for i in range(VerticesCount):
                f.read(4*3)
                f.read(20)
            f.seek(startoffset+(4*3))
            for i in range(VerticesCount):
                f.read(4*2)
                f.read(24)
            f.seek(startoffset+(4*5))
            for i in range(VerticesCount):
                f.read(4*3)
                f.read(20)
            f.seek(-20, 1)
            for i in range(IndicesCount):
                FaceType = read_int32(f)
                Counts = read_int32(f)
                asdf = []
                for i in range(Counts):
                    read_int32(f)
            Ending_Offset = f.tell()
            Obj = PartObj()
            Obj.name = meshName+"_1"
            Obj.start_offset = (str(hex(Starting_Offset)).replace('0x', '')).upper()
            Obj.end_offset = (str(hex(Ending_Offset)).replace('0x', '')).upper()
            Objs.append(Obj)
        f.read(36)

def file_enter(event):
    filepath = event.data
    filepath = filepath.replace("}", "")
    filepath = filepath.replace("{", "")
    path, ext = os.path.splitext(filepath)
    global Objs
    Objs = []
    parttable.delete(*parttable.get_children())
    if ext.lower() == '.o3d':
        read_o3d(filepath)
        for obj in Objs:
            part = parttable.insert('', tkinter.END, values=(obj.name, obj.start_offset, obj.end_offset))
            for inh in obj.inherit:
                parttable.insert(part, tkinter.END, values=(inh.name, inh.start_offset, inh.end_offset))
    elif ext.lower() == '.b3d':
        read_b3d(filepath)
        for obj in Objs:
            part = parttable.insert('', tkinter.END, values=(obj.name, obj.start_offset, obj.end_offset))
            for inh in obj.inherit:
                parttable.insert(part, tkinter.END, values=(inh.name, inh.start_offset, inh.end_offset))

def replace_model(event):
    filename = filedialog.askopenfilename(title="파일 선택")
    curItem = parttable.item(parttable.focus())
    start_off = int("0x"+str(curItem['values'][1]), 16)
    end_off = int("0x"+str(curItem['values'][2]), 16)
    f = open(file, 'rb')
    final = bytearray(f.read())
    f.close()
    f = open(filename, 'rb')
    toreplace = bytearray(f.read())
    toreplace.reverse()
    f.close()
    del final[start_off:end_off]
    for bytee in toreplace:
        final.insert(start_off, bytee)
    f = open(file, 'wb')
    f.write(final)
    f.close()
    messagebox.showinfo("교체완료", "성공적으로 교체되었습니다.")
    file_enter(file)

    

fileviewer.dnd_bind('<<Drop>>',file_enter)
replacebtn.bind('<Button-1>', replace_model)

root.mainloop()