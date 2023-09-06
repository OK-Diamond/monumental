 # Designed to be a less specialised version of the program.
from unidecode import unidecode # pip install unidecode
import subprograms.image_generator as img_gen
import subprograms.spreadsheet as sheets
import subprograms.file_edit as file
import subprograms.drive as drive
from os import replace, remove

class monument:
    def __init__(self, info: list[str], index: dict[str, int]) -> None:
        print("info", info)
        self.name = info[index["name"]]
        self.id = unidecode(info[index["name"]]).lower()
        for i in [" ", "-"]:
            self.id = self.id.replace(i, "_")
        for i in ["'", ".", "/", "\\", "\"", "\'"]:
            self.id = self.id.replace(i, "")
        print(self.name, self.id)
        self.province_id = info[index["prov_id"]]
        self.description = info[index["description"]].replace("\n", "\\n").replace("\"", "\\\"")
        self.artist = info[index["artist"]].replace("\n", "\\n").replace("\"", "\\\"")
        self.requirements = info[index["requirements"]].split("\n")
        self.starting_tier = info[index["starting_tier"]]
        
        if info[index["movable"]].lower() in ["yes", "no"]:
            self.movable = info[index["movable"]].lower()
        else:
            self.movable = "no"
        
        self.modifiers: dict[str, dict[str, list[str]]] = {
            1: {"province": [], "area": [], "country": [], "upgrade": [], "conditional": [], "other": []}, 
            2: {"province": [], "area": [], "country": [], "upgrade": [], "conditional": [], "other": []}, 
            3: {"province": [], "area": [], "country": [], "upgrade": [], "conditional": [], "other": []}
        }
        for [tier, data] in [[1, info[index["tier_1"]]], [2, info[index["tier_2"]]], [3, info[index["tier_3"]]]]:
            tier: int
            data: str
            self.modifiers[tier]["province"] = data.split("\n")
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
            for i in range(len(self.modifiers[tier]["province"])): # Area
                if "---area---" in self.modifiers[tier]["province"][i]:
                    self.modifiers[tier]["area"] = self.modifiers[tier]["province"][i+1:]
                    self.modifiers[tier]["province"] = self.modifiers[tier]["province"][:i]
                    break
        
        
        '''self.t1_modifiers: dict[str, list[str]] = {"province": [], "area": [], "country": [], "upgrade": [], "conditional": []}
        self.t2_modifiers: dict[str, list[str]] = {"province": [], "area": [], "country": [], "upgrade": [], "conditional": []}
        self.t3_modifiers: dict[str, list[str]] = {"province": [], "area": [], "country": [], "upgrade": [], "conditional": []}
        
        self.t1_modifiers["province"] = info[index["tier_1"]].split("\n") # Province
        for i in range(len(self.t1_modifiers["province"])): # Conditional Modifier
            if "---conditional---" in self.t1_modifiers["province"][i]:
                self.t1_modifiers["conditional"] = self.t1_modifiers["province"][i+1:]
                self.t1_modifiers["province"] = self.t1_modifiers["province"][:i]
                break
        for i in range(len(self.t1_modifiers["province"])): # Upgrade
            if "---upgrade---" in self.t1_modifiers["province"][i]:
                self.t1_modifiers["upgrade"] = self.t1_modifiers["province"][i+1:]
                self.t1_modifiers["province"] = self.t1_modifiers["province"][:i]
                break
        for i in range(len(self.t1_modifiers["province"])): # Country
            if "---country---" in self.t1_modifiers["province"][i]:
                self.t1_modifiers["country"] = self.t1_modifiers["province"][i+1:]
                self.t1_modifiers["province"] = self.t1_modifiers["province"][:i]
                break
        for i in range(len(self.t1_modifiers["province"])): # Area
            if "---area---" in self.t1_modifiers["province"][i]:
                self.t1_modifiers["area"] = self.t1_modifiers["province"][i+1:]
                self.t1_modifiers["province"] = self.t1_modifiers["province"][:i]
                break
        
        self.t2_modifiers["province"] = info[index["tier_2"]].split("\n") # Province
        for i in range(len(self.t2_modifiers["province"])): # Conditional Modifier
            if "---conditional---" in self.t2_modifiers["province"][i]:
                self.t2_modifiers["conditional"] = self.t2_modifiers["province"][i+1:]
                self.t2_modifiers["province"] = self.t2_modifiers["province"][:i]
                break
        for i in range(len(self.t2_modifiers["province"])): # Upgrade
            if "---upgrade---" in self.t2_modifiers["province"][i]:
                self.t2_modifiers["upgrade"] = self.t2_modifiers["province"][i+1:]
                self.t2_modifiers["province"] = self.t2_modifiers["province"][:i]
                break
        for i in range(len(self.t2_modifiers["province"])): # Country
            if "---country---" in self.t2_modifiers["province"][i]:
                self.t2_modifiers["country"] = self.t2_modifiers["province"][i+1:]
                self.t2_modifiers["province"] = self.t2_modifiers["province"][:i]
                break
        for i in range(len(self.t2_modifiers["province"])): # Area
            if "---area---" in self.t2_modifiers["province"][i]:
                self.t2_modifiers["area"] = self.t2_modifiers["province"][i+1:]
                self.t2_modifiers["province"] = self.t2_modifiers["province"][:i]
                break
        print("t2", self.t2_modifiers)
        
        self.t3_modifiers["province"] = info[index["tier_3"]].split("\n") # Province
        for i in range(len(self.t3_modifiers["province"])): # Conditional Modifier
            if "---conditional---" in self.t3_modifiers["province"][i]:
                self.t3_modifiers["conditional"] = self.t3_modifiers["province"][i+1:]
                self.t3_modifiers["province"] = self.t3_modifiers["province"][:i]
                break
        for i in range(len(self.t3_modifiers["province"])): # Upgrade
            if "---upgrade---" in self.t3_modifiers["province"][i]:
                self.t3_modifiers["upgrade"] = self.t3_modifiers["province"][i+1:]
                self.t3_modifiers["province"] = self.t3_modifiers["province"][:i]
                break
        for i in range(len(self.t3_modifiers["province"])): # Country
            if "---country---" in self.t3_modifiers["province"][i]:
                self.t3_modifiers["country"] = self.t3_modifiers["province"][i+1:]
                self.t3_modifiers["province"] = self.t3_modifiers["province"][:i]
                break
        for i in range(len(self.t3_modifiers["province"])): # Area
            if "---area---" in self.t3_modifiers["province"][i]:
                self.t3_modifiers["area"] = self.t3_modifiers["province"][i+1:]
                self.t3_modifiers["province"] = self.t3_modifiers["province"][:i]
                break'''
        
        
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
        return self.modifiers[tier][mod_type]

         # Old code - missing conditional
        '''if tier == 1:
            if mod_type in ["prov", "province"]:
                return self.t1_modifiers["province"]
            elif mod_type in ["area"]:
                return self.t1_modifiers["area"]
            elif mod_type in ["country"]:
                return self.t1_modifiers["country"]
            elif mod_type in ["upgr", "upgrade"]:
                return self.t1_modifiers["upgrade"]
        elif tier == 2:
            if mod_type in ["prov", "province"]:
                return self.t2_modifiers["province"]
            elif mod_type in ["area"]:
                return self.t2_modifiers["area"]
            elif mod_type in ["country"]:
                return self.t2_modifiers["country"]
            elif mod_type in ["upgr", "upgrade"]:
                return self.t2_modifiers["upgrade"]
        elif tier == 3:
            if mod_type in ["prov", "province"]:
                return self.t3_modifiers["province"]
            elif mod_type in ["area"]:
                return self.t3_modifiers["area"]
            elif mod_type in ["country"]:
                return self.t3_modifiers["country"]
            elif mod_type in ["upgr", "upgrade"]:
                return self.t3_modifiers["upgrade"]
        else:
            raise Exception(f"get_tier_data bad input: {tier}")'''

    def build_config(self) -> str:
        output  =           f"""{self.id} = {{\n"""
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
            
            for [category, modifier] in [
                ["province", "province_modifiers"], 
                ["area", "area_modifier"], 
                ["country", "country_modifiers"], 
                ["upgrade", "on_upgraded"], 
                ["conditional", "conditional_modifier"]
            ]:
                output +=       f"""		{modifier} = {{\n"""
                for row in self.get_tier_data(tier, category):
                    if not empty(row):
                        output +=   f"""			{row}\n"""
                output +=       f"""		}}\n"""
                
            for row in self.get_tier_data(tier, "other"):
                    if not empty(row):
                        output +=   f"""		{row}\n"""
                
            output +=           f"""	}}\n"""
        
        
        '''output +=           f"""	tier_2 = {{\n"""
        output +=           f"""		upgrade_time = {{\n"""
        output +=           f"""			months = 24\n"""
        output +=           f"""		}}\n"""
        output +=           f"""		cost_to_upgrade = {{\n"""
        output +=           f"""			factor = 250\n"""
        output +=           f"""		}}\n"""
        
        
        output +=       f"""		province_modifiers = {{\n"""
        for i in self.get_tier_data(2, "province"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=       f"""		area_modifier = {{\n"""
        for i in self.get_tier_data(2, "area"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""

        output +=       f"""		country_modifiers = {{\n"""
        for i in self.get_tier_data(2, "country"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=       f"""		on_upgraded = {{\n"""
        for i in self.get_tier_data(2, "upgrade"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=           f"""	}}\n"""
        
        
        output +=           f"""	tier_3 = {{\n"""
        output +=           f"""		upgrade_time = {{\n"""
        output +=           f"""			months = 48\n"""
        output +=           f"""		}}\n"""
        output +=           f"""		cost_to_upgrade = {{\n"""
        output +=           f"""			factor = 500\n"""
        output +=           f"""		}}\n"""
        
        
        output +=       f"""		province_modifiers = {{\n"""
        for i in self.get_tier_data(3, "province"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=       f"""		area_modifier = {{\n"""
        for i in self.get_tier_data(3, "area"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""

        output +=       f"""		country_modifiers = {{\n"""
        for i in self.get_tier_data(3, "country"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=       f"""		on_upgraded = {{\n"""
        for i in self.get_tier_data(3, "upgrade"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=           f"""	}}\n"""'''
        
        output +=           f"""}}\n"""
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
    return len(a) == 0 or a in ["-", "0", " ", "."]

def batch_copy(source_folder: str, dest_folder: str, files: str|list) -> None:
    if type(files) == str:
        files = [files]
    for f in files:
        print(f)
        file.copy(f"{source_folder}/{f}", f"{dest_folder}/{f}")
    return

def main() -> None:
     # Things to mess with:
    MOD_NAME = "post_finem" # Please avoid spaces, punctuation, special characters, etc. as they could lead to unexpected results.
    MOD_ID = "pf" # as above
    MOD_FILES_LOCATION = "mod_files"
    SOURCE_FILES_LOCATION = "source_files"
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
    TOKEN_LOCATION = f"subprograms/data/token.json"
    CREDENTIALS_LOCATION = f"subprograms/data/credentials.json"
    SHEETS_ID = "1jEof6L1EutUBgaS1NVqQaAPMekN0I3ogTC1ygvQTuiM"
    IMAGE_FOLDER_ID = "15xGaE1d6v9yxBXo8Fl1haA2f1MY-ttIE"

     # Don't mess with these:
    IMAGE_DEST_LOCATION = "temp"
    FILE_NAMES = {
        "common": f"{MOD_ID}_monuments.txt", 
        "localisation": f"{MOD_ID}_monuments_l_english.yml", 
        "interface": f"{MOD_ID}_monuments.gfx"
    }
    
    mon_list: list[monument] = []
    range_list, index = sheets.retrieve_range_with_index(SHEETS_ID, "monument_list", SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION) # Process monuments
    for i in range_list[1:]:
        mon_list.append(monument(i, index))

    print(f"common/great_projects/{FILE_NAMES['common']}")
    config = ""
    for i in mon_list:
        config += i.build_config()
    file.write(f"{MOD_FILES_LOCATION}/{MOD_NAME}/common/great_projects/{FILE_NAMES['common']}", config, "cp1252")
    
    print(f"localisation/{FILE_NAMES['localisation']}")
    localisation = "l_english:\n"
    for i in range(len(mon_list)): # Remove vanilla monuments
        has_desc = not empty(mon_list[i].get_description()) 
        has_artist = not empty(mon_list[i].get_artist())
        localisation += f" {mon_list[i].get_id()}:0 \"{mon_list[i].get_name()}\"\n"
        if has_desc or has_artist:
            localisation += f" {mon_list[i].get_id()}_desc:0 \""
            if has_desc:
                localisation += f"--------------\\n{mon_list[i].get_description()}"
                if has_artist:
                    localisation += "\\n"
            if has_artist:
                localisation += f"--------------\\nArt by {mon_list[i].get_artist()}"
            localisation += "\"\n"
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
