import numpy as np
import zlib
import math
import sys
import os
import subprocess
import json


#----------------------------------------------------
#      Megasepryte V 1.0
#---------------------------------------------------





class Project:
    def __init__(self, name):
        self.name = name
        self.path = None
        self.aseprite_files = {}
        self.scenes = {}
        self.next_scene_number = 3
        self.tracks = {}


    def import_aseprite_file(self, scene, file):    #, scene_name):
        if ((file.split("."))[1]) != "ase" and file.split(".")[1] != "aseprite":
            raise OSError("Incorrect file type, must be .ase or .aseprite")

        self.aseprite_files.update({scene:Aseprite_file(file)})
        self.scenes.update({scene:Scene(scene, self.next_scene_number)})
        self.scenes[scene].extract_scene(self.aseprite_files[scene])
        self.next_scene_number +=1

    def init_project(self, path):
        self.path = path
        try:
            os.mkdir(path+"/megasepryte")
            os.mkdir(path+"/megasepryte/testbed")
            os.mkdir(path+"/megasepryte/savefolder")
        except:
            pass
        
        # fiks mappestruktur.
        # lim inn standard filer der de skal. Inkl alle standard asm filer, og asm68k.exe og build.bat
         
    def import_deflemask_file(self, file):
        with open(file, "rb") as deflemask_file:
            compressed_deflemask_file = deflemask_file.read()
        track_data = zlib.decompress(compressed_deflemask_file)
        name_len = int.from_bytes(track_data[18:19], "little")
        title = (track_data[19:19+name_len]).decode("utf-8")

        self.tracks.update({title:Deflemask_track(track_data)})

    
    def test_project(self):
        # Assemble sammen hele rukla og launch .bin fila i blastem eller noe
        pass

    def test_scene(self, scene_name):
        file = open(f"{self.path}/megasepryte/testbed/test.asm", "w")
        write_test_scene_gamestate(file, scene_name)
        file = open(f"{self.path}/{scene_name}_main.asm", "w")
        write_test_scene_main(file)
        file = open(f"{self.path}/megasepryte/testbed/palette.asm", "w")
        self.write_palette(file, scene_name)
        file = open(f"{self.path}/megasepryte/testbed/tiles.asm", "w")
        self.write_tiles(file, scene_name)
        file = open(f"{self.path}/megasepryte/testbed/planeA.asm", "w")
        self.write_plane_A(file, scene_name)
        file = open(f"{self.path}/megasepryte/testbed/planeB.asm", "w")
        self.write_plane_B(file, scene_name)
        file = open(f"{self.path}/buildtest.bat", "w")
        write_buildtest(file,scene_name)
        file.close()
        
        subprocess.call([f'{self.path}/buildtest.bat'], cwd=self.path)
        os.remove(f"{self.path}/megasepryte/testbed/test.asm")
        os.remove(f"{self.path}/{scene_name}_main.asm")
        os.remove(f"{self.path}/megasepryte/testbed/palette.asm")
        os.remove(f"{self.path}/megasepryte/testbed/planeA.asm")
        os.remove(f"{self.path}/megasepryte/testbed/planeB.asm")
        os.remove(f"{self.path}/megasepryte/testbed/tiles.asm")
        os.remove(f"{self.path}/buildtest.bat")

    def list_scenes(self):
        for key in self.scenes:
            print(key)

    def open_file(self):
        pass

    def save_project_as(self, path):
        project = {}
        for key in self.scenes:
            list = []
            list.append({"palette":self.scenes[key].palette.palette_list})
            list.append({"tiles":self.scenes[key].tiles.tiles})
            list.append({"plane_a":self.scenes[key].nametable_plane_a.nametable})
            list.append({"plane_b":self.scenes[key].nametable_plane_b.nametable})
            list.append({"sprites":self.scenes[key].sprites.sprite_list})
            project.update({self.scenes[key].name:list})
        
        project = json.dumps(project)

        with open(f"{path}/{self.name}.megasepryte", "w") as outfile:
            outfile.write(project)

    def save_project(self):
        project = {}
        for key in self.scenes:
            list = []
            list.append({"palette":self.scenes[key].palette.palette_list})
            list.append({"tiles":self.scenes[key].tiles.tiles})
            list.append({"plane_a":self.scenes[key].nametable_plane_a.nametable})
            list.append({"plane_b":self.scenes[key].nametable_plane_b.nametable})
            list.append({"sprites":self.scenes[key].sprites.sprite_list})
            project.update({self.scenes[key].name:list})
        
        project = json.dumps(project)

        with open(f"{self.path}/megasepryte/savefolder/{self.name}.megasepryte", "w") as outfile:
            outfile.write(project)

    def new_scene(self, scene_name):
        number = self.next_scene_number
        if number < 10:
            number = (f"0{number}")
        else:
            number = (f"{number}")
        
        self.scenes.update({scene_name:None})
        
        try:
            os.mkdir(f"{self.path}/Gamestates/{number}_{scene_name}")
        except:
            pass
        try:
            os.mkdir(f"{self.path}/Gamestates/{number}_{scene_name}/gfx")
        except:
            pass
        try:
            os.mkdir(f"{self.path}/Gamestates/{number}_{scene_name}/gfx/palette")
            os.mkdir(f"{self.path}/Gamestates/{number}_{scene_name}/gfx/tiles")
            os.mkdir(f"{self.path}/Gamestates/{number}_{scene_name}/gfx/nametables")
        except:
            pass
        include = open(f"{self.path}/Framework/gamestate_includes.asm", "a")
        include.write(f'    include "gamestates/{number}_{scene_name}/{scene_name}.asm"\n')


    def export_scene(self, scene_name):
        self.export_palette(scene_name)
        self.export_tiles(scene_name)
        self.export_plane_a(scene_name)
        self.export_plane_b(scene_name)

    def export_palette(self, scene_name):
        include = open(f"{self.path}/Framework/gamestate_includes.asm", "a")
        include.write(f'    include "gamestates/{self.scenes[scene_name].scene_number}_{scene_name}/gfx/palette/{scene_name}_palette.asm"\n')
        file = open(f"{self.path}/Gamestates/{self.scenes[scene_name].scene_number}_{scene_name}/gfx/palette/{scene_name}_palette.asm", "w")
        self.write_palette(file, scene_name)

    def write_palette(self, file, scene_name):
        print_header(file)
        file.write(f"{scene_name}_palette_0:\n")
        for m in range(16):
            file.write(f"   dc.w    ${self.scenes[scene_name].palette.palette_list[m]}\n")
        file.write("\n")
        file.write(f"{scene_name}_palette_1:\n")
        for m in range(16):
            file.write(f"   dc.w    ${self.scenes[scene_name].palette.palette_list[m+16]}\n")
        file.write("\n")
        file.write(f"{scene_name}_palette_2:\n")
        for m in range(16):
            file.write(f"   dc.w    ${self.scenes[scene_name].palette.palette_list[m+32]}\n")
        file.write("\n")
        file.write(f"{scene_name}_palette_3:\n")
        for m in range(16):
            file.write(f"   dc.w    ${self.scenes[scene_name].palette.palette_list[m+48]}\n")

    def export_tiles(self, scene_name):
        file = open(f"{self.path}/Gamestates/{self.scenes[scene_name].scene_number}_{scene_name}/gfx/tiles/{scene_name}_tileset.asm", "w")
        self.write_tiles(file, scene_name)


    def write_tiles(self, file, scene_name):
        print_header(file)
        file.write(f"{scene_name}_tileset:\n")
        for n in range(len(self.scenes[scene_name].tiles.tiles)):
            for m in range(8):
                file.write(f"   dc.l    ${self.scenes[scene_name].tiles.tiles[n][m]}\n")
            file.write("\n")
        file.write(f"{scene_name}_tileset_end:\n")
        file.write(f"{scene_name}_tileset_size_b    equ ({scene_name}_tileset_end-{scene_name}_tileset)\n")
        file.write(f"{scene_name}_tileset_size_w    equ ({scene_name}_tileset_size_b/2)\n")
        file.write(f"{scene_name}_tileset_size_l    equ ({scene_name}_tileset_size_b/4)\n")
        file.write(f"{scene_name}_tileset_size_t    equ ({scene_name}_tileset_size_b/32)\n")

    def export_plane_a(self, scene_name):
        file = open(f"{self.path}/Gamestates/{self.scenes[scene_name].scene_number}_{scene_name}/gfx/nametables/{scene_name}_nametable_plane_A.asm", "w")
        print_header(file)
        self.write_plane_A(file, scene_name)

    def write_plane_A(self, file, scene_name):
        count = 0
        file.write(f"{scene_name}_nametable_plane_A:\n")
        for n in range(len(self.scenes[scene_name].nametable_plane_a.nametable)):
            file.write("    dc.w    ")
            count = 0
            for m in range(len(self.scenes[scene_name].nametable_plane_a.nametable[n])):
                if m == self.scenes[scene_name].nametable_plane_a.plane_width - 1:
                    file.write(f"${self.scenes[scene_name].nametable_plane_a.nametable[n][m]}")
                    count = 0
                elif count == 63:
                    file.write(f"${self.scenes[scene_name].nametable_plane_a.nametable[n][m]}\n")
                    file.write("    dc.w    ")
                    count = 0
                else:
                    file.write(f"${self.scenes[scene_name].nametable_plane_a.nametable[n][m]},")
                    count += 1
            file.write("\n")
        file.write("\n")
        file.write(f"{scene_name}_nametable_plane_A_end:\n")
        file.write(f"{scene_name}_nametable_plane_A_size_b  equ ({scene_name}_nametable_plane_A_end-{scene_name}_nametable_plane_A)\n")
        file.write(f"{scene_name}_nametable_plane_A_size_w  equ ({scene_name}_nametable_plane_A_size_b/2)\n")
        file.write(f"{scene_name}_nametable_plane_A_size_l  equ ({scene_name}_nametable_plane_A_size_b/4)\n")
        file.write(f"{scene_name}_nametable_plane_A_width  equ ${'{0:0{1}X}'.format((self.scenes[scene_name].nametable_plane_a.plane_width),2)}\n")
        file.write(f"{scene_name}_nametable_plane_A_height  equ ${'{0:0{1}X}'.format((self.scenes[scene_name].nametable_plane_a.plane_height),2)}\n")

    def export_plane_b(self, scene_name):
        file = open(f"{self.path}/Gamestates/{self.scenes[scene_name].scene_number}_{scene_name}/gfx/nametables/{scene_name}_nametable_plane_B.asm", "w")
        print_header(file)
        self.write_plane_B(file, scene_name)
        
    def write_plane_B(self, file, scene_name):
        count = 0
        file.write(f"{scene_name}_nametable_plane_B:\n")
        for n in range(len(self.scenes[scene_name].nametable_plane_b.nametable)):
            file.write("    dc.w    ")
            count = 0
            for m in range(len(self.scenes[scene_name].nametable_plane_b.nametable[n])):
                if m == (self.scenes[scene_name].nametable_plane_b.plane_width - 1):
                    file.write(f"${self.scenes[scene_name].nametable_plane_b.nametable[n][m]}")
                    count = 0
                elif count == 63:
                    file.write(f"${self.scenes[scene_name].nametable_plane_b.nametable[n][m]}\n")
                    file.write("    dc.w    ")
                    count = 0
                else:
                    file.write(f"${self.scenes[scene_name].nametable_plane_b.nametable[n][m]},")
                    count += 1
            file.write("\n")
        file.write("\n")
        file.write(f"{scene_name}_nametable_plane_B_end:\n")
        file.write(f"{scene_name}_nametable_plane_B_size_b  equ ({scene_name}_nametable_plane_B_end-{scene_name}_nametable_plane_B)\n")
        file.write(f"{scene_name}_nametable_plane_B_size_w  equ ({scene_name}_nametable_plane_B_size_b/2)\n")
        file.write(f"{scene_name}_nametable_plane_B_size_l  equ ({scene_name}_nametable_plane_B_size_b/4)\n")
        file.write(f"{scene_name}_nametable_plane_B_width  equ ${'{0:0{1}X}'.format((self.scenes[scene_name].nametable_plane_b.plane_width),2)}\n")
        file.write(f"{scene_name}_nametable_plane_B_height  equ ${'{0:0{1}X}'.format((self.scenes[scene_name].nametable_plane_b.plane_height),2)}\n")

    def check_filestructure(self):
        #path = (f"")
        pass

    def set_local_project_folder(self):
        pass

    def list_project_file_scenes(self, file_path):
        file = open(file_path)
        data = json.load(file)
        for i in data:
            print(i)
        file.close()

    def open_project_file(self, file_path):
        file = open(file_path)
        data = json.load(file)
        for i in data:
            self.open_scene(i, data)
        file.close()

    def open_project_file_scene(self, file_path, scene_name):
        file = open(file_path)
        data = json.load(file)
        self.open_scene(scene_name, data)
        file.close()

    def open_scene(self, scene_name, data):        
        self.new_scene(scene_name)
        self.scenes.update({scene_name:Scene(scene_name, self.next_scene_number)})

        self.scenes[scene_name].palette.palette_list = data[scene_name][0]["palette"]

        self.scenes[scene_name].tiles.tiles = data[scene_name][1]["tiles"]

        self.scenes[scene_name].nametable_plane_a.nametable = data[scene_name][2]["plane_a"]
        self.scenes[scene_name].nametable_plane_a.plane_height = len(self.scenes[scene_name].nametable_plane_a.nametable)
        self.scenes[scene_name].nametable_plane_a.plane_width = len(self.scenes[scene_name].nametable_plane_a.nametable[0])
        

        self.scenes[scene_name].nametable_plane_b.nametable = data[scene_name][3]["plane_b"]
        self.scenes[scene_name].nametable_plane_b.plane_height = len(self.scenes[scene_name].nametable_plane_b.nametable)
        self.scenes[scene_name].nametable_plane_b.plane_width = len(self.scenes[scene_name].nametable_plane_b.nametable[0])

        self.next_scene_number += 1




class Aseprite_file:
    def __init__(self, file):
        try:
            self.external_file = open(file, "rb")
        except FileNotFoundError:
            print("Nope, did not find the file")
            sys.exit(1)

        self.header = Aseprite_file_header(self.external_file)
        self.frames = Aseprite_file_frames(self.external_file)
        self.seeker = 144
        self.chunks = []
        self.get_chunks(self.seeker, self.external_file)

    def get_chunks(self,seeker,asepritefile):
        chunk_no = 0
        if self.frames.no_chunks_new == 0:
            chunk_no = self.frames.no_chunks_old
        else:
            chunk_no = self.frames.no_chunks_new
        for n in range(chunk_no):
            self.chunks.append(Chunk(asepritefile,seeker))
            seeker += self.chunks[n].chunk_size

#class Imported_scene:
 #   def __init__(self,palette, tiles, plane_a, plane_b):
  #      self.tiles = 

class Scene:
    def __init__(self, scene_name, scene_number):
        self.name = scene_name
        self.scene_number = ""
        self.palette = MD_palette()
        self.tiles = MD_tiles()
        self.nametable_plane_a = MD_nametable()
        self.nametable_plane_b = MD_nametable()
        self.sprites = MD_sprites()

        if scene_number < 10:
            self.scene_number = (f"0{scene_number}")
        else:
            self.scene_number = (f"{scene_number}")
        
    def extract_scene(self, internal_file):
        self.palette.extract_palette(internal_file)
        self.tiles.extract_tiles(internal_file)
        self.nametable_plane_a.extract_nametable(internal_file, 2)
        self.nametable_plane_b.extract_nametable(internal_file, 1)

class MD_tiles:
    def __init__(self):
        self.tiles = []
         
    def extract_tiles(self, internal_file):        
        temp = []
        for n in range(len(internal_file.chunks)):
            if internal_file.chunks[n].chunk_type == "Tileset chunk":
                for m in range(len(internal_file.chunks[n].chunk_data.tileset_mdformat.tileset)):
                    temp.append(internal_file.chunks[n].chunk_data.tileset_mdformat.tileset[m])
                tiles_for_removal = list(dict.keys(internal_file.chunks[n].chunk_data.tile_duplicates))
                for n in range(len(tiles_for_removal)):
                    temp.remove(temp[tiles_for_removal[n]])
                for n in range(len(temp)):
                    tile = []
                    for m in range(8):
                        tile.append(str(temp[n][0+(8*m)]) + str(temp[n][1+(8*m)]) + str(temp[n][2+(8*m)]) + str(temp[n][3+(8*m)]) + str(temp[n][4+(8*m)]) + str(temp[n][5+(8*m)]) + str(temp[n][6+(8*m)]) + str(temp[n][7+(8*m)]))
                    self.tiles.append(tile)



class MD_palette:
    def __init__(self):
        self.palette_list = []

    def extract_palette(self, internal_file):
        for n in range(len(internal_file.chunks)):
            if internal_file.chunks[n].chunk_type == "Palette chunk":
                for m in range(64):
                    red = internal_file.chunks[n].chunk_data.palette[m].red
                    green = internal_file.chunks[n].chunk_data.palette[m].green
                    blue =  internal_file.chunks[n].chunk_data.palette[m].blue

                    if red == 0:
                        red = "0"
                    elif red == 52:
                        red = "2"
                    elif red == 87:
                        red = "4"
                    elif red == 116:
                        red = "6"
                    elif red == 144:
                        red = "8"
                    elif red == 172:
                        red = "A"
                    elif red == 206:
                        red = "C"
                    elif red == 255:
                        red = "E"
                    else:
                        red = "F"

                    if green == 0:
                        green = "0"
                    elif green == 52:
                        green = "2"
                    elif green == 87:
                        green = "4"
                    elif green == 116:
                        green = "6"
                    elif green == 144:
                        green = "8"
                    elif green == 172:
                        green = "A"
                    elif green == 206:
                        green = "C"
                    elif green == 255:
                        green = "E"
                    else:
                        green = "F"

                    if blue == 0:
                        blue = "0"
                    elif blue == 52:
                        blue = "2"
                    elif blue == 87:
                        blue = "4"
                    elif blue == 116:
                        blue = "6"
                    elif blue == 144:
                        blue = "8"
                    elif blue == 172:
                        blue = "A"
                    elif blue == 206:
                        blue = "C"
                    elif blue == 255:
                        blue = "E"
                    else:
                        blue = "F"
                    self.palette_list.append(f"0{blue}{green}{red}")





class MD_nametable:
    def __init__(self):
        self.nametable = []
        self.plane_width = 0
        self.plane_height = 0


    def extract_nametable(self,internal_file, layer_index):
        self.cel_pos_y = 0
        self.cel_pos_x = 0
        self.cel_width = 0
        self.cel_height = 0
        self.plane_width = int(internal_file.header.width / 8)
        self.plane_height = int(internal_file.header.height / 8)
        self.tile_duplicates = {}
        self.tileset_chunk = 0
        self.orginal_table = []
        
        for n in range(len(internal_file.chunks)):
            if internal_file.chunks[n].chunk_type == "Cel chunk":
                if internal_file.chunks[n].chunk_data.layer_index == layer_index:
                    self.cel_pos_y = int(internal_file.chunks[n].chunk_data.pos_y / 8)
                    self.cel_pos_x = int(internal_file.chunks[n].chunk_data.pos_x / 8)
                    self.cel_width = internal_file.chunks[n].chunk_data.width_tiles
                    self.cel_height = internal_file.chunks[n].chunk_data.height_tiles
                    for m in range(len(internal_file.chunks[n].chunk_data.nametable)):
                        self.orginal_table.append(int.from_bytes(internal_file.chunks[n].chunk_data.nametable[m], "little"))

        for n in range(len(internal_file.chunks)):
            if internal_file.chunks[n].chunk_type == "Tileset chunk":
                self.tile_duplicates = internal_file.chunks[n].chunk_data.tile_duplicates
                self.tileset_chunk = n

        self.remove_list = list(dict.keys(internal_file.chunks[self.tileset_chunk].chunk_data.tile_duplicates))
        temp_list = list((internal_file.chunks[self.tileset_chunk].chunk_data.tile_duplicates).values())
        self.keep_list = []
        for n in range(len(temp_list)):
            self.keep_list.append(temp_list[n][0])

        for n in range(self.cel_pos_y):
            line = []
            for k in range(self.cel_pos_x):
                line.append("0000")
            for m in range(self.cel_width):
                line.append("0000")
            for l in range(self.plane_width - self.cel_pos_x - self.cel_width):
                line.append("0000")
            self.nametable.append(line)

        for n in range(self.cel_height):
            line = []
            for k in range(self.cel_pos_x):
                line.append("0000")
            for m in range(self.cel_width):
                tile = self.orginal_table[(n*self.cel_width) + m]
                o_tile = tile
                flip = 0
                palette = 0
                removal = 0

                if tile in self.tile_duplicates:
                    #print(tile)
                    flip = self.tile_duplicates[tile][1]
                    tile = self.tile_duplicates[tile][0]

                for p in range(len(self.remove_list)):
                    if tile > self.remove_list[p]:
                        removal += 1

                palette = internal_file.chunks[self.tileset_chunk].chunk_data.tileset_mdformat.palette_list[o_tile]
                if palette != 0 and palette != 64 and palette != 128 and palette != 192:
                    print(f"found use of multiple palettes in tile {tile}, approximating")

                palette = int(palette/64) * 8192
                line.append(str('{0:0{1}X}'.format((tile + flip + palette - removal),4)))

            for l in range(self.plane_width - self.cel_pos_x - self.cel_width):
                line.append("0000")
            self.nametable.append(line)

        for n in range(self.plane_height - self.cel_pos_y - self.cel_height):
            line = []
            for k in range(self.cel_pos_x):
                line.append("0000")
            for m in range(self.cel_width):
                line.append("0000")
            for l in range(self.plane_width - self.cel_pos_x - self.cel_width):
                line.append("0000")
            self.nametable.append(line)


class MD_sprites:
    sprite_list = []

class Chunk:
    def __init__(self, asepritefile, seeker):
        asepritefile.seek(seeker)
        self.location = seeker
        self.chunk_size = int.from_bytes(asepritefile.read(4),"little")
        self.chunk_type = format((int.from_bytes(asepritefile.read(2),"little")),"04X")

        chunk_types = {"0004":"Old palette chunk",
                            "0011":"Old palette chunk",
                            "2004":"Layer chunk",
                            "2005":"Cel chunk",
                            "2006":"Cel extra chunk",
                            "2007":"Color profile chunk",
                            "2008":"External files chunk",
                            "2016":"Mask chunk",
                            "2017":"Path chunk",
                            "2018":"Tags chunk",
                            "2019":"Palette chunk",
                            "2020":"User data chunk",
                            "2022":"Slice chunk",
                            "2023":"Tileset chunk"}

        self.chunk_type = chunk_types[self.chunk_type]

        if self.chunk_type == "Palette chunk":
            self.chunk_data = Data_palette_chunk(asepritefile, self.location)
        elif self.chunk_type == "Layer chunk":
            self.chunk_data = Data_layer_chunk(asepritefile, self.location)
        elif self.chunk_type == "Tileset chunk":
            self.chunk_data = Data_tileset_chunk(asepritefile, self.location)
        elif self.chunk_type == "Cel chunk":
            self.chunk_data = Data_cel_chunk(asepritefile, self.location, self.chunk_size)


class Data_cel_chunk:   #
    def __init__(self, asepritefile, location, size):       # + orginal_tile_list
        asepritefile.seek(location+6)
        self.layer_index = int.from_bytes(asepritefile.read(2),"little")

        self.pos_x = int.from_bytes(asepritefile.read(2),"little")
        self.pos_y = int.from_bytes(asepritefile.read(2),"little")
        self.opacity_level = int.from_bytes(asepritefile.read(1),"little")
        self.cel_type = int.from_bytes(asepritefile.read(2),"little")
        self.for_future = int.from_bytes(asepritefile.read(7),"little")
        if self.cel_type == 0:
            pass
        if self.cel_type == 1:
            pass
        if self.cel_type == 2:
            pass
        if self.cel_type == 3:
            self.width_tiles = int.from_bytes(asepritefile.read(2),"little")
            self.height_tiles = int.from_bytes(asepritefile.read(2),"little")
            self.bits_pr_tile = int.from_bytes(asepritefile.read(2),"little")
            self.bitmask_tile_id = int.from_bytes(asepritefile.read(4),"little")
            self.bitmask_x_flip = int.from_bytes(asepritefile.read(4),"little")
            self.bitmask_y_flip = int.from_bytes(asepritefile.read(4),"little")
            self.bitmask_90_cw = int.from_bytes(asepritefile.read(4),"little")
            self.reserved = int.from_bytes(asepritefile.read(10),"little")
            self.tile_matrix_compressed = asepritefile.read(location-size-48)
            self.tile_matrix_decompressed = zlib.decompress(self.tile_matrix_compressed)
            self.nametable = []
            for n in range(int(len(self.tile_matrix_decompressed)/4)):
                self.nametable.append(self.tile_matrix_decompressed[n*4:(n*4)+4])


class Data_tileset_chunk: #$2023
    def __init__(self, asepritefile, location):
        asepritefile.seek(location+6)
        self.tileset_id = int.from_bytes(asepritefile.read(4),"little")
        self.tileset_flags = int.from_bytes(asepritefile.read(4),"little")
        self.no_tiles = int.from_bytes(asepritefile.read(4),"little")
        self.tile_width = int.from_bytes(asepritefile.read(2),"little")
        self.tile_height = int.from_bytes(asepritefile.read(2),"little")
        self.base_index = int.from_bytes(asepritefile.read(2),"little")
        self.reserved = int.from_bytes(asepritefile.read(14),"little")
        self.name_length = int.from_bytes(asepritefile.read(2),"little")
        self.name = asepritefile.read(self.name_length).decode("utf-8")
        if self.tileset_flags & 0b1:
            self.external_file_id = int.from_bytes(asepritefile.read(4),"little")
            self.external_tileset_id = int.from_bytes(asepritefile.read(4),"little")
        elif self.tileset_flags & 0b10:
            compressed_data_length = int.from_bytes(asepritefile.read(4),"little")
            compressed_tileset_image = asepritefile.read(compressed_data_length)
            self.decompressed_tileset_image = zlib.decompress(compressed_tileset_image)

            self.tile_duplicates = {}
            self.tile_list = []
            for n in range(0,len(self.decompressed_tileset_image),64):
                self.tile_list.append(self.decompressed_tileset_image[0+n:64+n])
            self.tileset_mdformat = Megadrive_tileset(self.tile_list)
            no_tiles = len(self.tileset_mdformat.tileset)
            self.clean_tileset(no_tiles)




    def clean_tileset(self, no_tiles):
        o = no_tiles
        count = 0
        for n in reversed(self.tile_list):
            o -= 1
            tile_n = list(n[0:8] + n[8:16] + n[16:24] + n[24:32] + n[32:40] + n[40:48] + n[48:56] + n[56:64])

            for m in range(len(tile_n)):
                tile_n[m] = tile_n[m] % 16
            tile_n = bytes(tile_n)

            tile_v = list(n[56:64] + n[48:56] + n[40:48] + n[32:40] + n[24:32] + n[16:24] + n[8:16] + n[0:8])

            for l in range(len(tile_v)):
                tile_v[l] = tile_v[l] % 16
            tile_v = bytes(tile_v)

            tile_h = list(n[7::-1] + n[15:7:-1] + n[23:15:-1] + n[31:23:-1] + n[39:31:-1] + n[47:39:-1] + n[55:47:-1] + n[63:55:-1])

            for k in range(len(tile_h)):
                tile_h[k] = tile_h[k] % 16
            tile_h = bytes(tile_h)

            tile_hv = list(n[64:55:-1] + n[55:47:-1] + n[47:39:-1] + n[39:31:-1] + n[31:23:-1] + n[23:15:-1] + n[15:7:-1] + n[7::-1])

            for j in range(len(tile_hv)):
                tile_hv[j] = tile_hv[j] % 16
            tile_hv = bytes(tile_hv)

            for m in range(len(self.tile_list)):
                if tile_n == self.tile_list[m]:
                    break
                elif tile_v == self.tile_list[m]:
                    self.tile_duplicates[o] = [m, 4096]
                    break
                elif tile_h == self.tile_list[m]:
                    self.tile_duplicates[o] = [m, 2048]
                    break
                elif tile_hv == self.tile_list[m]:
                    self.tile_duplicates[o] = [m, 6144]
                    break


class Megadrive_tileset:
    def __init__(self,tile_list):
        #print(tile_list[5])
        self.zero_check(tile_list)
        self.tileset = []
        self.palette_list = []
        for m in range(len(tile_list)):
            test = []
            palette = []
            for n in range(64):
                palette.append(math.floor(tile_list[m][n] / 16))
                test.append(str((tile_list[m][n]) % 16))
                if test[n] == "10":
                    test[n] = "A"
                elif test[n] == "11":
                    test[n] = "B"
                elif test[n] == "12":
                    test[n] = "C"
                elif test[n] == "13":
                    test[n] = "D"
                elif test[n] == "14":
                    test[n] = "E"
                elif test[n] == "15":
                    test[n] = "F"

            self.tileset.append(test)
            self.palette_list.append(sum(palette))


    def zero_check(self, tile_list):
        temp = []
        for n in range(len(tile_list)):
            ping = []
            for m in range(len(tile_list[n])):
                ping.append(int(tile_list[n][m] / 16))
            temp.append(ping)

        for n in range(len(temp)):
            if not self.check_equal(temp[n]):
                local_palette = 0
                for m in range(len(tile_list[n])):
                    if int(tile_list[n][m]) != 0:
                        local_palette = int(int(tile_list[n][m]) / 16)
                        break
                invalid = False
                for m in range(len(tile_list[n])):
                    if int(tile_list[n][m]) != 0 and int(int(tile_list[n][m]) / 16) != local_palette:
                        invalid = True

                if invalid == False:
                    replacement = []
                    for m in range(len(tile_list[n])):
                        if int(tile_list[n][m]) == 0:
                            replacement.append(int(16 * local_palette))
                        else:
                            replacement.append(int(tile_list[n][m]))
                    tile_list[n] = (bytes(replacement))

    def check_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == x for x in iterator)


class Data_layer_chunk:
    def __init__(self, asepritefile, location):
        asepritefile.seek(location + 6)
        self.flags = int.from_bytes(asepritefile.read(2),"little")
        self.layer_type = int.from_bytes(asepritefile.read(2),"little")
        self.child_level = int.from_bytes(asepritefile.read(2),"little")
        self.layer_px_width = int.from_bytes(asepritefile.read(2),"little")
        self.layer_px_height = int.from_bytes(asepritefile.read(2),"little")
        self.blend_mode = int.from_bytes(asepritefile.read(2),"little")
        self.opacity = int.from_bytes(asepritefile.read(1),"little")
        self.for_future = int.from_bytes(asepritefile.read(3),"little")
        if self.layer_type == 2:
            self.name_length = int.from_bytes(asepritefile.read(2),"little")
            self.name = asepritefile.read(self.name_length).decode("utf-8")
            self.tileset_index = int.from_bytes(asepritefile.read(4), "little")
        else:
            self.name_length = int.from_bytes(asepritefile.read(2),"little")
            self.name = asepritefile.read(self.name_length).decode("utf-8")


class Data_palette_chunk:
    def __init__(self, asepritefile, location):
        asepritefile.seek(location + 6)
        self.size = int.from_bytes(asepritefile.read(4),"little")
        self.first_color = int.from_bytes(asepritefile.read(4),"little")
        self.last_color = int.from_bytes(asepritefile.read(4),"little")
        self.for_future = int.from_bytes(asepritefile.read(8),"little")
        self.color_error_lists = {"red":[],"green":[],"blue":[]}
        self.palette = []
        for n in range(self.size):
            self.palette.append(New_palette_entry(asepritefile))

        self.check_colors(self.size, self.color_error_lists)
        self.fix_colors(self.color_error_lists)

    def check_colors(self, size, error_list):
        for n in range(size):
            if self.palette[n].red != 0 and self.palette[n].red != 52 and self.palette[n].red != 87 and self.palette[n].red != 116 and self.palette[n].red != 144 and self.palette[n].red != 172 and self.palette[n].red != 206 and self.palette[n].red != 255:
                error_list["red"].append(n)
            if self.palette[n].green != 0 and self.palette[n].green != 52 and self.palette[n].green != 87 and self.palette[n].green != 116 and self.palette[n].green != 144 and self.palette[n].green != 172 and self.palette[n].green != 206 and self.palette[n].green != 255:
                error_list["green"].append(n)
            if self.palette[n].blue != 0 and self.palette[n].blue != 52 and self.palette[n].blue != 87 and self.palette[n].blue != 116 and self.palette[n].blue != 144 and self.palette[n].blue != 172 and self.palette[n].blue != 206 and self.palette[n].blue != 255:
                error_list["blue"].append(n)

    def fix_colors(self,error_list):
        for n in range(len(self.color_error_lists["red"])):
            self.palette[error_list["red"][n]].red = self.find_closest_valid_color(self.palette[error_list["red"][n]].red)
        for n in range(len(self.color_error_lists["green"])):
            self.palette[error_list["green"][n]].green = self.find_closest_valid_color(self.palette[error_list["green"][n]].green)
        for n in range(len(self.color_error_lists["blue"])):
            self.palette[error_list["blue"][n]].blue = self.find_closest_valid_color(self.palette[error_list["blue"][n]].blue)

    def find_closest_valid_color(self,color_value):
        list1 = [0, 52, 87, 116, 144, 172, 206, 255]
        arr = np.asarray(list1)
        i = (np.abs(arr - color_value)).argmin()

        return(arr[i])

class New_palette_entry:
    def __init__(self,asepritefile):
        self.entry_flag = int.from_bytes(asepritefile.read(2),"little")
        self.red = int.from_bytes(asepritefile.read(1),"little")
        self.green = int.from_bytes(asepritefile.read(1),"little")
        self.blue = int.from_bytes(asepritefile.read(1),"little")
        self.alpha = int.from_bytes(asepritefile.read(1),"little")


class Aseprite_file_header:
    def __init__(self,asepritefile):
            self.file_size = int.from_bytes(asepritefile.read(4),"little")
            self.magic_number = (hex(int.from_bytes(asepritefile.read(2),"little"))).lstrip("0x").upper()
            self.frames = int.from_bytes(asepritefile.read(2),"little")
            self.width = int.from_bytes(asepritefile.read(2),"little")
            self.height = int.from_bytes(asepritefile.read(2),"little")
            self.color_depth = int.from_bytes(asepritefile.read(2),"little")
            self.flags = int.from_bytes(asepritefile.read(4),"little")
            self.speed = int.from_bytes(asepritefile.read(2),"little")
            self.setbe0 = int.from_bytes(asepritefile.read(4),"little")
            self.setbe1 = int.from_bytes(asepritefile.read(4),"little")
            self.trans_index = int.from_bytes(asepritefile.read(1),"little")
            self.ignore = int.from_bytes(asepritefile.read(3),"little")
            self.no_colors = int.from_bytes(asepritefile.read(2),"little")
            self.px_width = int.from_bytes(asepritefile.read(1),"little")
            self.px_height = int.from_bytes(asepritefile.read(1),"little")
            self.grid_x_pos = int.from_bytes(asepritefile.read(2),"little")
            self.grid_y_pos = int.from_bytes(asepritefile.read(2),"little")
            self.grid_width = int.from_bytes(asepritefile.read(2),"little")
            self.grid_height = int.from_bytes(asepritefile.read(2),"little")
            self.for_future = int.from_bytes(asepritefile.read(84),"little")

class Aseprite_file_frames:
    def __init__(self,asepritefile):
        self.frame_size = int.from_bytes(asepritefile.read(4),"little")
        self.magic_number = (hex(int.from_bytes(asepritefile.read(2),"little"))).lstrip("0x").upper()
        self.no_chunks_old = int.from_bytes(asepritefile.read(2),"little")
        self.frame_duration = int.from_bytes(asepritefile.read(2),"little")
        self.for_future = int.from_bytes(asepritefile.read(2),"little")
        self.no_chunks_new = int.from_bytes(asepritefile.read(4),"little")

class Deflemask_track:
    def __init__(self,track_data):
        type = int.from_bytes(track_data[17:18], "little")

        if type != 2:
            print("Deflemask file not MegaDrive")

        index = 18
        len = int.from_bytes(track_data[18:19], "little")
        index += 1
        self.title = (track_data[index:index+len]).decode("utf-8)")
        index += len
        len = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.author = (track_data[index:index+len]).decode("utf-8")
        index += len
        self.highlight_a = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.highlight_b = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.time_base = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.tick_time_1 = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.tick_time_2 = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.frames_mode = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.custom_hz = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.custom_hz_1 = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.custom_hz_2 = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.custom_hz_3 = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        self.total_rows_pr_pattern = int.from_bytes(track_data[index:index+4], "little")
        index += 4
        #print(self.total_rows_pr_pattern)
        self.total_rows_in_pattern_matrix = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        #print(self.total_rows_in_pattern_matrix)
        self.pattern_matrix_value = []
        for n in range(10): #number of channels in system; MegaDrive = 10
            for m in range(self.total_rows_in_pattern_matrix):
                self.pattern_matrix_value.append(int.from_bytes(track_data[index:index+1], "little"))
                index += 1
        #index += 10*self.total_rows_in_pattern_matrix
        self.total_instruments = int.from_bytes(track_data[index:index+1], "little")
        index += 1
        print(self.total_instruments)
        self.instruments = {}
        for n in range(self.total_instruments):
            len = int.from_bytes(track_data[index:index+1], "little")
            index += 1
            name = track_data[index+1:index+1+len].decode("utf-8")
            index += 1
            type = int.from_bytes(track_data[index:index+1], "little")
            index += 1

            if type == 1:
                pass
            elif type == 0:
                pass



            #self.instruments.update({track_data[index+1:index+1+len].decode("utf-8"):"b"})
            #index += 1+len




def print_header(file):
        file.write(';==============================================;   /`""-,__                         \n')
        file.write(";Exported with magasepryte                     ;   \/\)`   `'-.                     \n")
        file.write(";----------------------------------------------;  // \ .--.\   '.                   \n")
        file.write(";Made by DenTroge as a cs50python final project; //|-.  \_o `-.  \---._             \n")
        file.write(";==============================================; || \_o\  _.-.\`'-'    `-.          \n")
        file.write(";                                                || |\.-'`    |           `.        \n")
        file.write(";                                                || | \  \    |             `\      \n")
        file.write(";                                                \| /  \ ,\' /                \     \n")
        file.write(";                                                       `---'                  ;    \n")
        file.write(";                                                        `))          .-'      |    \n")
        file.write(";                                                     .-.// .-.     .'        ,;=D  \n")
        file.write(";                                                    /  // /   \  .'          ||    \n")
        file.write(";                                                    |..-' |     '-'          //    \n")
        file.write(";                                                    ((    \         .===. _,//     \n")
        file.write(";                                                     '`'--`'---''',--\_/-;-'`      \n")
        file.write(";                                                                   `~/^\`          \n")
        file.write(";                                                                    '==='          \n")

def write_test_scene_gamestate(file, scene_name):
    file.write("test:\n")
    file.write("\n")
    file.write("    move.w #$04, Gamestate\n")
    file.write("    waitvbi\n")
    file.write("    move.w #$2700, SR\n")
    file.write("    move.l #null, vbivector\n")
    file.write("\n")
    file.write("    lea.l Tempscreen, A0\n")
    file.write("    move.l #$00, D0\n")
    file.write("    move.w #$3FF, d1\n")
    file.write("@ClearLoop:\n")
    file.write("    move.l D0, (a0)+\n")
    file.write("    dbra d1, @ClearLoop\n")
    file.write("\n")
    file.write("    Lea.l Tempscreen, A0\n")
    file.write(f"    lea.l {scene_name}_nametable_plane_A, A1\n")
    file.write("    move.w #$1F, D0\n")
    file.write("    move.w D0, D1\n")
    file.write("@PlaneALoop:\n")
    file.write("    move.l (A1)+, (A0)+\n")
    file.write("    Dbra D0, @PlaneALoop\n")
    file.write(f"    add.w #((2*{scene_name}_nametable_plane_A_width)-$80), A1\n")
    file.write("    move.w #$1F, D0\n")
    file.write("    dbra D1, @PlaneALoop\n")
    file.write("\n")
    file.write("    DMADUMP Tempscreen,4096,PlaneA_NTBL\n")
    file.write("\n")
    file.write("    Lea.l Tempscreen, A0\n")
    file.write(f"    lea.l {scene_name}_nametable_plane_B, A1\n")
    file.write("    move.w #$1F, D0\n")
    file.write("    move.w D0, D1\n")
    file.write("@PlaneBLoop:\n")
    file.write("    move.l (A1)+, (A0)+\n")
    file.write("    Dbra D0, @PlaneBLoop\n")
    file.write(f"    add.w #((2*{scene_name}_nametable_plane_B_width)-$80), A1\n")
    file.write("    move.w #$1F, D0\n")
    file.write("    dbra D1, @PlaneBLoop\n")
    file.write("\n")
    file.write("    DMADUMP Tempscreen,4096,PlaneB_NTBL\n")
    file.write("")
    file.write(f"    DMADUMP {scene_name}_tileset, {scene_name}_tileset_size_b, $0000\n")
    file.write("")
    file.write(f"    lea.l {scene_name}_palette_0, A0\n")
    file.write("    BSR SETPAL1\n")
    file.write("\n")
    file.write(f"    lea.l {scene_name}_palette_1, A0\n")
    file.write("    BSR SETPAL2\n")
    file.write("\n")
    file.write(f"    lea.l {scene_name}_palette_2, A0\n")
    file.write("    BSR SETPAL3\n")
    file.write("\n")
    file.write(f"    lea.l {scene_name}_palette_3, A0\n")
    file.write("    BSR SETPAL4\n")
    file.write("\n")
    file.write("    jsr DUMPCOLS\n")
    file.write("\n")
    file.write("    move.l #megasepryte_testVBL, UserVBIvector\n")
    file.write("    move.l #MAINVBI,VBIVECTOR\n")
    file.write("    move #$2000, SR\n")
    file.write("\n")
    file.write("\n")
    file.write("gamestateLoop:\n")
    file.write("   waitvbi\n")
    file.write("\n")
    file.write("    BTST #J_Right, Joypad0\n")
    file.write("    bne @testleft\n")
    file.write("    sub.w #$02, planeb_x_pos\n")
    file.write("    jmp @no_scroll\n")
    file.write("\n")
    file.write("@testleft:\n")
    file.write("    BTST #J_Left, Joypad0\n")
    file.write("    bne @no_scroll\n")
    file.write("    add.w #$02, planeb_x_pos\n")
    file.write("@no_scroll:\n")
    file.write("\n")
    file.write("    BTST #J_A, Joypad0\n")
    file.write("    bne @test_B\n")
    file.write("    sub.w #$02, planea_x_pos\n")
    file.write("@test_B:\n")
    file.write("    BTST #J_C, Joypad0\n")
    file.write("    bne @no_a_scroll\n")
    file.write("    add.w #$02, planea_x_pos\n")
    file.write("@no_a_scroll:\n")
    file.write("    lea.l VDP_Data, A1\n")
    file.write("    lea.l VDP_Control, A2\n")
    file.write("    move.l #planeAHorizScroll0, (A2)\n")
    file.write("    move.w planea_x_pos, (A1)\n")    
    file.write("    lea.l VDP_Data, A1\n")
    file.write("    lea.l VDP_Control, A2\n")
    file.write("    move.l #planeBHorizScroll0, (A2)\n")
    file.write("    move.w planeb_x_pos, (A1)\n")
    file.write("\n")
    file.write("    jsr LevelStreaming\n")
    file.write("\n")
    file.write("    jmp gamestateLoop\n")
    file.write("\n")
    file.write("    jmp main\n")
    file.write("\n")
    file.write("megasepryte_testVBL:\n")
    file.write("\n")
    file.write("    DMADUMP Tempscreen,4096,PlaneB_NTBL\n")
    file.write("\n")
    file.write("    jmp ReturnVBIVector\n")
    file.write("LevelStreaming:\n")
    file.write(f"    lea {scene_name}_nametable_plane_B, A0\n")
    file.write("    add.w #$7c, A0\n")
    file.write("    lea Tempscreen, A1\n")
    file.write("    move.w planeb_x_pos, D0\n")
    file.write("    move.l D0, D2\n")
    file.write("    clr.l D1\n")
    file.write("    sub.w D0, D1\n")
    file.write("    and.l #$0000FFFF, D1\n")
    file.write("    lsr.w #$2, D1\n")
    file.write("    add.w D1, A0\n")
    file.write("    and.w #$000F, D2\n")
    file.write("    cmp.w #$00, D2\n")
    file.write("    bne @NoColumnUpdate\n")
    file.write("@IdentTempscreenPos:\n")
    file.write("    and #$7F, D1\n")
    file.write("    cmp.w #$00, D1\n")
    file.write("    beq @ZeroSpecialCase\n")
    file.write("    sub.w #$4, D1\n")
    file.write("    add.w D1, A1\n")
    file.write("    jmp @LevelStreamDump\n")
    file.write("@ZeroSpecialCase:\n")
    file.write("    add.w #$7c, A1\n")
    file.write("@LevelStreamDump:\n")
    file.write("    clr.l D0\n")
    file.write("    move.w #$1F, D0\n")
    file.write("@LevelStreamCopyLoop:\n")
    file.write("    move.l (A0), (A1)\n")
    file.write(f"    add.w #(2*{scene_name}_nametable_plane_B_width), A0\n")
    file.write("    add.w #$80, A1\n")
    file.write("    dbra D0, @LevelStreamCopyLoop\n")
    file.write("@NoColumnUpdate:\n")
    file.write("    rts\n")


def write_test_scene_main(file):
    file.write('    include "Framework\equates.asm"\n')
    file.write('	Include "FrameWork\Macros.asm"\n')
    file.write('	Include "FrameWork\SystemVariables.asm"\n')
    file.write('	Include "FrameWork\Header.asm"\n')
    file.write('	Include "FrameWork\System.asm"\n')
    file.write('	Include "Framework\Exceptions.asm"\n')
    file.write("\n")
    file.write("	RSSET	USERRAM\n")
    file.write("\n")
    file.write("UserVBIvector: 		rs.l 	1\n")
    file.write("TEMPSCREEN:	    	RS.B	4096\n")
    file.write("GameState: 	    	rs.W	1\n")
    file.write("GameClock:	    	rs.w	1\n")
    file.write("HandyloopCounter: 	rs.W	1\n")
    file.write("userlongword:		rs.l 	1\n")
    file.write("planeb_x_pos:		rs.W	1\n")
    file.write("planea_x_pos:       rs.w    1\n")
    file.write("\n")
    file.write("ENDVARS:	    RS.B	0\n")
    file.write("\n")
    file.write("__Start\n")
    file.write("\n")
    file.write("MAIN:		WAITVBI\n")
    file.write("\n")
    file.write("	jmp test\n")
    file.write("    jmp Main\n")
    file.write('	include "megasepryte/testbed/test.asm"\n')
    file.write('    include "megasepryte/testbed/palette.asm"\n')
    file.write('    include "megasepryte/testbed/tiles.asm"\n')
    file.write('    include "megasepryte/testbed/planeA.asm"\n')
    file.write('    include "megasepryte/testbed/planeB.asm"\n')
    file.write('    include "Framework\Audio\echo.asm"\n')
    file.write('    include "Framework\Audio\Instrumentlist.asm"\n')
    file.write("Size:\n")
    file.write("__End\n")

def write_buildtest(file,scene_name):
    file.write(f"asm68k /p /i /w /ov+ /oos+ /oop+ /oow+ /ooz+ /ooaq+ /oosq+ /oomq+ /ow+ {scene_name}_main.asm, megasepryte/testbed/{scene_name}_test.md")
