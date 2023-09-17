 # Designed to be a less specialised version of the program.
from unidecode import unidecode # pip install unidecode
import subprograms.image_generator as img_gen
import subprograms.spreadsheet as sheets
import subprograms.file_edit as file
import subprograms.drive as drive
from os import replace, remove

def create_id_from_name(name: str) -> str:
    name_id = unidecode(name).lower()
    for i in [" ", "-"]:
        name_id = name_id.replace(i, "_")
    for i in ["'", ".", "/", "\\", "\"", "\'"]:
        name_id = name_id.replace(i, "")
    return name_id

class monument:
    def __init__(self, info: list[str], index: dict[str, int]) -> None:
        for row in range(len(info)):
            info[row] = info[row].replace("\r", "")
        print("info", info)
        self.name = info[index["name"]]
        self.id = unidecode(info[index["name"]]).lower()
        for i in [" ", "-"]:
            self.id = self.id.replace(i, "_")
        for i in ["'", ".", "/", "\\", "\"", "\'"]:
            self.id = self.id.replace(i, "")
        self.code = info[index["code"]]
        print(self.name, self.id, self.code)
        self.province_id = info[index["prov_id"]]
        self.description = info[index["description"]].replace("\n", "\\n").replace("\"", "\\\"")
        self.artist = info[index["artist"]].replace("\n", "\\n").replace("\"", "\\\"")
        self.requirements = info[index["requirements"]].split("\n")
        self.starting_tier = info[index["starting_tier"]]
        #self.tooltip = info[index["tooltip"]].replace("\r", "").split("\n")
        
        if info[index["movable"]].lower() in ["yes", "no"]:
            self.movable = info[index["movable"]].lower()
        else:
            self.movable = "no"
        
        self.modifiers: dict[str, dict[str, list[str]]] = {
            1: {"province": [], "area": [], "region": [], "country": [], "upgrade": [], "conditional": [], "other": []}, 
            2: {"province": [], "area": [], "region": [], "country": [], "upgrade": [], "conditional": [], "other": []}, 
            3: {"province": [], "area": [], "region": [], "country": [], "upgrade": [], "conditional": [], "other": []}
        }
        for [tier, data] in [[1, info[index["tier_1"]]], [2, info[index["tier_2"]]], [3, info[index["tier_3"]]]]:
            tier: int
            data: str
            self.modifiers[tier]["province"] = data.replace("\r", "").split("\n")
            for i in range(len(self.modifiers[tier]["province"])): # Other - can be used for anything
                if "---other---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["other"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
            for i in range(len(self.modifiers[tier]["province"])): # Conditional Modifier
                if "---conditional---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["conditional"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
            for i in range(len(self.modifiers[tier]["province"])): # Upgrade
                if "---upgrade---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["upgrade"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
            for i in range(len(self.modifiers[tier]["province"])): # Country
                if "---country---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["country"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
            for i in range(len(self.modifiers[tier]["province"])): # Region
                if "---region---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["region"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
            for i in range(len(self.modifiers[tier]["province"])): # Area
                if "---area---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["area"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
        
        '''# Test modifiers:
        print("modifiers:")
        for i in self.modifiers:
            print(i)
            for j in self.modifiers[i]:
                print(" ", j, self.modifiers[i][j])
        input()'''
        
        return

    
    def get_name(self) -> str:
        return self.name
    def get_id(self) -> str:
        return self.id
    def get_location(self) -> str:
        return self.province_id
    def get_description(self) -> str:
        return self.description
    def get_artist(self) -> str:
        return self.artist
    def get_requirements(self) -> list[str]:
        return self.requirements
    
    def get_tier_data(self, tier: int, mod_type: str) -> list[str]:
        mod_type = mod_type.lower()
        modifier = self.modifiers[tier][mod_type]
        is_empty = True
        for row in modifier:
            if not empty(row):
                is_empty = False
        return modifier, is_empty

    def build_monument(self) -> str:
        output  =           f"""{self.id} = {{ # {self.code}\n"""
        output +=           f"""	start = {self.province_id}\n"""
        output +=           f"""	date = 1.01.01\n"""
        output +=           f"""	time = {{\n"""
        output +=           f"""		months = 0\n"""
        output +=           f"""	}}\n"""
        output +=           f"""	build_cost = 0\n"""
        output +=       f"""	can_be_moved = {self.movable}\n"""
        output +=           f"""	move_days_per_unit_distance = 10\n"""
        output +=       f"""	starting_tier = {self.starting_tier}\n"""        
        output +=           f"""	type = monument\n"""
        
        
        output +=       f"""	build_trigger = {{\n"""
        for i in self.requirements:
            if not empty(i):
                output +=   f"""		{i}\n"""
        output +=       f"""	}}\n"""
        
        output +=           f"""	on_built = {{}}\n"""
        output +=           f"""	on_destroyed = {{}}\n"""
        
        output +=       f"""	can_use_modifiers_trigger = {{\n"""
        for i in self.requirements:
            if not empty(i):
                output +=   f"""		{i}\n"""
        output +=       f"""	}}\n"""
        
        output +=       f"""	can_upgrade_trigger = {{\n"""
        for i in self.requirements:
            if not empty(i):
                output +=   f"""		{i}\n"""
        output +=       f"""	}}\n"""
        
        output +=           f"""	keep_trigger = {{}}\n"""
        
        
        output +=           f"""	tier_0 = {{\n"""
        output +=           f"""		upgrade_time = {{\n"""
        output +=           f"""			months = 0\n"""
        output +=           f"""		}}\n"""
        output +=           f"""		cost_to_upgrade = {{\n"""
        output +=           f"""			factor = 0\n"""
        output +=           f"""		}}\n"""
        output +=           f"""		province_modifiers = {{}}\n"""
        output +=           f"""		area_modifier = {{}}\n"""
        output +=           f"""		country_modifiers = {{}}\n"""
        output +=           f"""		on_upgraded = {{}}\n"""
        output +=           f"""	}}\n"""
        
        for [tier, time, cost] in [[1, 120, 1000], [2, 240, 2500], [3, 480, 5000]]:
            output +=           f"""	tier_{tier} = {{\n"""
            output +=           f"""		upgrade_time = {{\n"""
            output +=           f"""			months = {time}\n"""
            output +=           f"""		}}\n"""
            output +=           f"""		cost_to_upgrade = {{\n"""
            output +=           f"""			factor = {cost}\n"""
            output +=           f"""		}}\n"""
            
            for [category, modifier, force_show] in [
                ["province",    "province_modifiers"  , True ], 
                ["area",        "area_modifier"       , True ], 
                ["region",      "region_modifier"     , False], 
                ["country",     "country_modifiers"   , True ], 
                ["upgrade",     "on_upgraded"         , False], 
                ["conditional", "conditional_modifier", False]
            ]:
                tier_data, is_empty = self.get_tier_data(tier, category)
                if force_show or not is_empty:
                    output +=       f"""		{modifier} = {{\n"""
                    #print("tier", tier_data)
                    for row in tier_data:
                        if not empty(row):
                            #print("row", row)
                            output +=   f"""			{row}\n"""
                    output +=       f"""		}}\n"""
            
            tier_data, is_empty = self.get_tier_data(tier, "other")
            if not is_empty:
                for row in tier_data:
                        if not empty(row):
                            output +=   f"""		{row}\n"""
            
            output +=           f"""	}}\n"""
                
        output +=           f"""}}\n"""
        return output

    def build_localisation(self):
         # Name
        output = f" {self.id}:0 \"{self.name}\"\n"
         # Description
        has_desc = not empty(self.description) 
        has_artist = not empty(self.artist)
        if has_desc or has_artist:
            output += f" {self.id}_desc:0 \""
            if has_desc:
                output += f"--------------\\n{self.description}"
                if has_artist:
                    output += "\\n"
            if has_artist:
                output += f"--------------\\nArt by {self.artist}"
            output += "\"\n"
         # Tooltips
        #if not empty(self.tooltip):
        #    for tt_number in range(len(self.tooltip)):
        #        output += f" {self.id}_tt{tt_number}:0 \"{self.tooltip[tt_number]}\"\n"
        return output

def empty(a: str|list) -> bool:
    if type(a) == list:
        if len(a) == 0:
            return True
        elif len(a) == 1:
            a = a[0]
        else:
            for i in a:
                if not empty(i):
                    return False
            return True
    elif a == None:
        return False
    return len(a) == 0 or a in ["-", "0", " ", ".", "_"]

def batch_copy(source_folder: str, dest_folder: str, files: str|list) -> None:
    if type(files) == str:
        files = [files]
    for f in files:
        #print(f)
        file.copy(f"{source_folder}/{f}", f"{dest_folder}/{f}")
    return

def main() -> None:
     # Things to mess with:
    MOD_NAME = "post_finem" # Please avoid spaces, punctuation, special characters, etc. as they could lead to unexpected results.
    MOD_ID = "pf" # as above
    MOD_FILES_LOCATION = "C:/Users/Oliver Kirk/Documents/Paradox Interactive/Europa Universalis IV/mod"
    #MOD_FILES_LOCATION = "mod_files"
    SOURCE_FILES_LOCATION = "source_files"
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
    TOKEN_LOCATION = f"subprograms/data/token.json"
    CREDENTIALS_LOCATION = f"subprograms/data/credentials.json"
    SHEETS_ID = "1jEof6L1EutUBgaS1NVqQaAPMekN0I3ogTC1ygvQTuiM"
    IMAGE_FOLDER_ID = "1BgC2T2LIXUMP2By_sCdBH1MeLlnfUOcs"

     # Don't mess with these:
    IMAGE_DEST_LOCATION = "temp"
    FILE_NAMES = {
        "common": f"{MOD_ID}_mon_monuments.txt", 
        "localisation": f"{MOD_ID}_mon_l_english.yml", 
        "interface": f"{MOD_ID}_mon_monuments.gfx"
    }
    
    mon_list: list[monument] = []
    range_list, index = sheets.retrieve_range_with_index(SHEETS_ID, "monument_list", SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION) # Process monuments
    for i in range_list[1:]:
        mon_list.append(monument(i, index))

    print(f"common/great_projects/{FILE_NAMES['common']}")
    config = ""
    for mon in mon_list:
        config += mon.build_monument()
    print("write to", f"{MOD_FILES_LOCATION}/{MOD_NAME}/common/great_projects/{FILE_NAMES['common']}")
    file.write(f"{MOD_FILES_LOCATION}/{MOD_NAME}/common/great_projects/{FILE_NAMES['common']}", config, "cp1252")
    
    print(f"localisation/{FILE_NAMES['localisation']}")
    localisation = "l_english:\n"
    for mon in mon_list:
        localisation += mon.build_localisation()
    file.write(f"{MOD_FILES_LOCATION}/{MOD_NAME}/localisation/{FILE_NAMES['localisation']}", localisation, "utf-8-sig")
    
    print("gfx/interface/great_projects   image files")
    input("Press enter to continue")
    file.test_folder(IMAGE_DEST_LOCATION, False)
    #file.delete_contents(IMAGE_DEST_LOCATION)
    drive.download_contents(IMAGE_FOLDER_ID, IMAGE_DEST_LOCATION, SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION)
    image_file_type = "dds"
    img_gen.main(
        IMAGE_DEST_LOCATION, 
        f"{MOD_FILES_LOCATION}/{MOD_NAME}/gfx/interface/great_projects", 
        "subprograms/data", image_file_type
    )
    
    print(f"interface/{FILE_NAMES['interface']}")
    gfx_str = "spriteTypes = {\n"
    prov_list = []
    for i in img_gen.listdir(f"{MOD_FILES_LOCATION}/{MOD_NAME}/gfx/interface/great_projects"):
        prov_list.append(i)
        prov_id = i.split(".")[0]
        found_monument = False
        for j in mon_list:
            if j.get_location() == prov_id:
                found_monument = True
                replace(
                    f"{MOD_FILES_LOCATION}/{MOD_NAME}/gfx/interface/great_projects/{i}", 
                    f"{MOD_FILES_LOCATION}/{MOD_NAME}/gfx/interface/great_projects/great_project_{j.get_id()}.{image_file_type}"
                )
                gfx_str += f"""	spriteType = {{\n"""
                gfx_str += f"""		name = "GFX_great_project_{j.get_id()}"\n"""
                gfx_str += f"""		texturefile = "gfx//interface//great_projects//great_project_{j.get_id()}.{image_file_type}"\n"""
                gfx_str += f"""	}}\n"""
        if not found_monument and i[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]: # Second part is to prevent already valid images from being removed.
            remove(f"{MOD_FILES_LOCATION}/{MOD_NAME}/gfx/interface/great_projects/{i}")
            #print("MONUMENT REMOVED", f"{MOD_FILES_LOCATION}/{MOD_NAME}/gfx/interface/great_projects/{i}")
    gfx_str += "}"
    file.write(f"{MOD_FILES_LOCATION}/{MOD_NAME}/interface/{FILE_NAMES['interface']}", gfx_str)
    file.delete(IMAGE_DEST_LOCATION)
    return
    
if __name__ == "__main__":
    main()
