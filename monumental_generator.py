from unidecode import unidecode # pip install unidecode
import subprograms.image_generator as img_gen
import subprograms.spreadsheet as sheets
import subprograms.file_edit as file
import subprograms.drive as drive
from os import replace, remove
from pyttsx3 import init as tts_init # pip install pyttsx3 - For TTS

class monument_type:
    def __init__(self, info: list[str], index: dict[str, int]) -> None:
        self.name = info[index["group"]]
        self.t1_province_modifiers, self.t1_area_modifiers, self.t1_on_upgrade = [], [], []
        self.t2_province_modifiers, self.t2_area_modifiers, self.t2_on_upgrade = [], [], []
        self.t3_province_modifiers, self.t3_area_modifiers, self.t3_on_upgrade = [], [], []
        #print()
        #print("name", info[index["group"]])
        #print("tier 1", info[index["tier_1"]])
        self.t1_province_modifiers = info[index["tier_1"]].split("\n")#[1:]
        #print("aaa", self.t1_province_modifiers)
        for i in range(len(self.t1_province_modifiers)):
            if "---upgrade---" in self.t1_province_modifiers[i]:
                self.t1_on_upgrade = self.t1_province_modifiers[i+1:]
                self.t1_province_modifiers = self.t1_province_modifiers[:i]
                break
        for i in range(len(self.t1_province_modifiers)):
            if "---area---" in self.t1_province_modifiers[i]:
                self.t1_area_modifiers = self.t1_province_modifiers[i+1:]
                self.t1_province_modifiers = self.t1_province_modifiers[:i]
                break
        #print("t1_province_modifiers", self.t1_province_modifiers)
        #print("t1_on_upgrade", self.t1_on_upgrade)
        #print("t1_area_modifiers", self.t1_area_modifiers)
        
        self.t2_province_modifiers = info[index["tier_2"]].split("\n")#[1:]
        for i in range(len(self.t2_province_modifiers)):
            if "---upgrade---" in self.t2_province_modifiers[i]:
                self.t2_on_upgrade = self.t2_province_modifiers[i+1:]
                self.t2_province_modifiers = self.t2_province_modifiers[:i]
                break
        for i in range(len(self.t2_province_modifiers)):
            if "---area---" in self.t2_province_modifiers[i]:
                self.t2_area_modifiers = self.t2_province_modifiers[i+1:]
                self.t2_province_modifiers = self.t2_province_modifiers[:i]
                break
        
        self.t3_province_modifiers = info[index["tier_3"]].split("\n")#[1:]
        for i in range(len(self.t3_province_modifiers)):
            if "---upgrade---" in self.t3_province_modifiers[i]:
                self.t3_on_upgrade = self.t3_province_modifiers[i+1:]
                self.t3_province_modifiers = self.t3_province_modifiers[:i]
                break
        for i in range(len(self.t3_province_modifiers)):
            if "---area---" in self.t3_province_modifiers[i]:
                self.t3_area_modifiers = self.t3_province_modifiers[i+1:]
                self.t3_province_modifiers = self.t3_province_modifiers[:i]
                break
        
        self.requirements = info[index["requirements"]].split("\n")#[1:]
        self.other = info[index["other"]].split("\n")#[1:]
        self.count = info[index["count"]]
    def get_name(self) -> str:
        return self.name
    def get_t1_province_modifiers(self) -> str:
        return self.t1_province_modifiers
    def get_t1_area_modifiers(self) -> str:
        return self.t1_area_modifiers
    def get_t1_on_upgrade(self) -> str:
        return self.t1_on_upgrade
    def get_t2_province_modifiers(self) -> str:
        return self.t2_province_modifiers
    def get_t2_area_modifiers(self) -> str:
        return self.t2_area_modifiers
    def get_t2_on_upgrade(self) -> str:
        return self.t2_on_upgrade
    def get_t3_province_modifiers(self) -> str:
        return self.t3_province_modifiers
    def get_t3_area_modifiers(self) -> str:
        return self.t3_area_modifiers
    def get_t3_on_upgrade(self) -> str:
        return self.t3_on_upgrade
    def get_requirements(self) -> str:
        return self.requirements
    def get_other(self) -> str:
        return self.other

class monument:
    def __init__(self, info: list[str], mon_index: dict[str, int], type_list: list[monument_type], type_index: dict[str, int]) -> None:
        #print("Monument", info)
        self.name = info[mon_index["name"]]
        #print("\nM name:", self.name)
        #print(info[0])
        self.id = unidecode(info[mon_index["name"]])
        #print(self.id)
        self.id = self.id.lower()
        for i in [" ", "-"]:
            self.id = self.id.replace(i, "_")
        for i in ["'", ".", "/", "/", "\"", "\'"]:
            self.id = self.id.replace(i, "")
        #print("M id:", self.id)
        self.province_id = info[mon_index["prov_id"]]
        #print(self.province_id, self.id)
        #print("M province_id:", self.province_id)
        self.type = "" #monument_type(["","","","","","",""], type_index)
        self.requirements = info[mon_index["requirements"]].split("\n")#[1:]
        self.unique_effects = info[mon_index["unique_effects"]].split("\n")#[1:]
        for i in type_list:
            if i.name == info[mon_index["type"]]:
                self.type = i
                for j in i.get_other():
                    self.unique_effects.append(j)
                for j in i.get_requirements():
                    self.requirements.append(j)
        self.description = info[mon_index["description"]].replace("\n", "\\n")
        self.suggested_by = info[mon_index["suggested_by"]]
        if self.type == "":
            input(f"Type not found: {info[mon_index['type']]}")
        return

    def find_key(self, key: str) -> bool:
        if key in self.unique_effects:
            return True
        else:
            return False
    
    def get_name(self) -> str:
        return self.name
    def get_id(self) -> str:
        return self.id
    def get_location(self) -> str:
        return self.province_id
    def get_type_data(self) -> monument_type:
        return self.type
    def get_description(self) -> str:
        return self.description
    def get_suggested_by(self) -> str:
        return self.suggested_by
    def get_unique_effects(self) -> list[str]:
        return self.unique_effects
    def get_requirements(self) -> list[str]:
        return self.requirements
    
    def get_tier_data(self, tier: int, mod_type: str) -> list[str]:
        mod_type = mod_type.lower()
        modifier_list = []
        if tier == 1:
            if mod_type in ["prov", "province"]:
                for i in self.type.get_t1_province_modifiers():
                    modifier_list.append(i)
            elif mod_type in ["area"]:
                for i in self.type.get_t1_area_modifiers():
                    modifier_list.append(i)
            elif mod_type in ["upgr", "upgrade"]:
                for i in self.type.get_t1_on_upgrade():
                    modifier_list.append(i)
        elif tier == 2:
            if mod_type in ["prov", "province"]:
                for i in self.type.get_t2_province_modifiers():
                    modifier_list.append(i)
            elif mod_type in ["area"]:
                for i in self.type.get_t2_area_modifiers():
                    modifier_list.append(i)
            elif mod_type in ["upgr", "upgrade"]:
                for i in self.type.get_t2_on_upgrade():
                    modifier_list.append(i)
        elif tier == 3:
            if mod_type in ["prov", "province"]:
                for i in self.type.get_t3_province_modifiers():
                    modifier_list.append(i)
            elif mod_type in ["area"]:
                for i in self.type.get_t3_area_modifiers():
                    modifier_list.append(i)
            elif mod_type in ["upgr", "upgrade"]:
                for i in self.type.get_t3_on_upgrade():
                    modifier_list.append(i)
        else:
            input()
        return modifier_list

    def build_config(self) -> str:
        output  =           f"""{self.id} = {{\n"""
        output +=           f"""	start = {self.province_id}\n"""
        output +=           f"""	date = 1.01.01\n"""
        output +=           f"""	time = {{\n"""
        output +=           f"""		months = 0\n"""
        output +=           f"""	}}\n"""
        output +=           f"""	build_cost = 0\n"""
        
        if self.find_key("movable"):
            output +=       f"""	can_be_moved = yes\n"""
        else:
            output +=       f"""	can_be_moved = no\n"""
        
        output +=           f"""	move_days_per_unit_distance = 10\n"""
        
        if self.find_key("starts at tier 1"):
            output +=       f"""	starting_tier = 1\n"""
        elif self.find_key("starts at tier 2"):
            output +=       f"""	starting_tier = 2\n"""
        elif self.find_key("starts at tier 3"):
            output +=       f"""	starting_tier = 3\n"""
        else:
            output +=       f"""	starting_tier = 0\n"""
        
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
        
        
        output +=           f"""	tier_1 = {{\n"""
        output +=           f"""		upgrade_time = {{\n"""
        output +=           f"""			months = 12\n"""
        output +=           f"""		}}\n"""
        output +=           f"""		cost_to_upgrade = {{\n"""
        output +=           f"""			factor = 100\n"""
        output +=           f"""		}}\n"""
        
        output +=       f"""		province_modifiers = {{\n"""
        for i in self.get_tier_data(1, "province"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=       f"""		area_modifier = {{\n"""
        for i in self.get_tier_data(1, "area"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""

        output +=           f"""		country_modifiers = {{}}\n"""
        
        output +=       f"""		on_upgraded = {{\n"""
        for i in self.get_tier_data(1, "upgrade"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=           f"""	}}\n"""
        
        
        output +=           f"""	tier_2 = {{\n"""
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

        output +=           f"""		country_modifiers = {{}}\n"""
        
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

        output +=           f"""		country_modifiers = {{}}\n"""
        
        output +=       f"""		on_upgraded = {{\n"""
        for i in self.get_tier_data(3, "upgrade"):
            if not empty(i):
                output +=   f"""			{i}\n"""
        output +=       f"""		}}\n"""
        
        output +=           f"""	}}\n"""
        
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

def tts(text: str) -> None:
    engine = tts_init()
    engine.setProperty('rate', 125)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    return

def batch_copy(source_folder: str, dest_folder: str, files: str|list) -> None:
    if type(files) == str:
        files = [files]
    for f in files:
        print(f)
        file.copy(f"{source_folder}/{f}", f"{dest_folder}/{f}")
    return

def main() -> None:
    PROGRAM_LOCATION = "monumental"
    MOD_FILES_LOCATION = f"{PROGRAM_LOCATION}/mod_files"
    SOURCE_FILES_LOCATION = f"{PROGRAM_LOCATION}/source_files"
    
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
    TOKEN_LOCATION = f"{PROGRAM_LOCATION}/monumental/subprograms/data/token.json"
    CREDENTIALS_LOCATION = f"{PROGRAM_LOCATION}/monumental/subprograms/data/credentials.json"
    SHEETS_ID = "1C1mt8cOGRljZgc5gwC9uRpVlL-XjPQ84Di4g08tNEuo"
    IMAGE_FOLDER_ID = "1Z1m4YpNDJfXeMwQCWEuHRK1p8On-Qr09"
    IMAGE_DEST_LOCATION = f"{PROGRAM_LOCATION}/temp"
    
    batch_copy(SOURCE_FILES_LOCATION, f"{MOD_FILES_LOCATION}/monumental", ["descriptor.mod", "thumbnail.png"])
    
    print("monumental.mod")
    mod_file_data = file.read(f"{SOURCE_FILES_LOCATION}/descriptor.mod", split=False)
    mod_file_data += "\npath=\"C:/Users/Oliver Kirk/Documents/Paradox Interactive/Europa Universalis IV/mod/monumental\""
    file.write(f"{MOD_FILES_LOCATION}/monumental.mod", mod_file_data)
    
    type_list: list[monument_type] = []
    range_list, type_index = sheets.retrieve_range_with_index(SHEETS_ID, "monument_type", SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION) # Process monument types
    for i in range_list[1:]:
        type_list.append(monument_type(i, type_index))
    
    #print(type_index)
    #for i in type_list:
    #    print(i.get_name(), i.get_t1_province_modifiers())
    
    mon_list: list[monument] = []
    range_list, mon_index = sheets.retrieve_range_with_index(SHEETS_ID, "monument_list", SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION) # Process monuments
    for i in range_list[1:]:
        mon_list.append(monument(i, mon_index, type_list, type_index))
    for i in range(len(mon_list)-1, -1, -1): # Remove vanilla monuments
        if mon_list[i].get_type_data().get_name() == "Vanilla":
            mon_list.pop(i)

    print("common/great_projects/monumental_monuments.txt")
    config = ""
    for i in mon_list:
        config += i.build_config()
    file.write(f"{MOD_FILES_LOCATION}/monumental/common/great_projects/monumental_monuments.txt", config, "cp1252")
    
    print("localisation/monumental_l_english.yml")
    localisation = "l_english:\n"
    for i in range(len(mon_list)): # Remove vanilla monuments
        has_desc = not empty(mon_list[i].get_description())
        has_credit = not empty(mon_list[i].get_suggested_by())
        localisation += f" {mon_list[i].get_id()}:0 \"{mon_list[i].get_name()}\"\n"
        if has_desc or has_credit:
            localisation += f" {mon_list[i].get_id()}_desc:0 \""
            if has_desc:
                localisation += f"--------------\\n{mon_list[i].get_description()}"
                if has_credit:
                    localisation += "\\n"
            if has_credit:
                localisation += f"--------------\\nSuggested by {mon_list[i].get_suggested_by()}"
            localisation += "\"\n"
    file.write(f"{MOD_FILES_LOCATION}/monumental/localisation/monumental_l_english.yml", localisation, "utf-8-sig")
    
    print("gfx/interface/great_projects   image files")
    #input("Press enter to continue")
    file.delete_contents(IMAGE_DEST_LOCATION)
    drive.download_contents(IMAGE_FOLDER_ID, IMAGE_DEST_LOCATION, SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION)
    image_file_type = "dds"
    img_gen.main(IMAGE_DEST_LOCATION, f"{MOD_FILES_LOCATION}/monumental/gfx/interface/great_projects", f"{PROGRAM_LOCATION}/subprograms/data", image_file_type)
    
    print("interface/monumental_great_project.gfx")
    gfx_str = "spriteTypes = {\n"
    prov_list = []
    for i in img_gen.listdir(f"{MOD_FILES_LOCATION}/monumental/gfx/interface/great_projects"):
        prov_list.append(i)
        prov_id = i.split(".")[0]
        found_monument = False
        for j in mon_list:
            if j.get_location() == prov_id:
                found_monument = True
                replace(f"{MOD_FILES_LOCATION}/monumental/gfx/interface/great_projects/{i}", f"{MOD_FILES_LOCATION}/monumental/gfx/interface/great_projects/great_project_{j.get_id()}.{image_file_type}")
                gfx_str += f"""	spriteType = {{\n"""
                gfx_str += f"""		name = "GFX_great_project_{j.get_id()}"\n"""
                gfx_str += f"""		texturefile = "gfx//interface//great_projects//great_project_{j.get_id()}.{image_file_type}"\n"""
                gfx_str += f"""	}}\n"""
        if not found_monument and i[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]: # Second part is to prevent already valid images from being removed.
            remove(f"{MOD_FILES_LOCATION}/monumental/gfx/interface/great_projects/{i}")
            #print("MONUMENT REMOVED", f"{MOD_FILES_LOCATION}/monumental/gfx/interface/great_projects/{i}")
    gfx_str += "}"
    file.write(f"{MOD_FILES_LOCATION}/monumental/interface/monumental_great_project.gfx", gfx_str)
    file.delete_contents(IMAGE_DEST_LOCATION)
    
    tts("Ding ding ding!") # TTS to grab my attention:
    
    return
    
if __name__ == "__main__":
    main()
