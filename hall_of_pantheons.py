import subprograms.image_generator as img_gen
import subprograms.spreadsheet as sheets
import subprograms.file_edit as file
from mon_gen import empty

class god:
    def __init__(self, name: str, desc: str, effect: str, tooltip: str, religion: str, god_no: int) -> None:
        self.name = name
        self.desc = desc
        self.effect = effect
        self.tooltip = tooltip.replace("\r", "").split("\n")
        self.religion = religion
        self.number = god_no
        self.monument = {
            "name": "Hall of Pantheons", 
            "id": "hall_of_pantheons", 
            "code": "hop"
        }
        return
    
    def build_event(self, namespace:str, picture: str = "NORSE_TEMPLE_eventPicture"):
        MEAN_TIME = 6
        COOLDOWN = 365*4
        COOLDOWN_REDUCED = 365*3
        FLAG = f"pf_mon_{self.monument['code']}_blessing_flag"
        
        output = f"""province_event = {{ # Blessing of {self.name}
    id = {namespace}.{self.number}
    title = {namespace}.{self.number}.title
    desc = {namespace}.{self.number}.desc
    picture = {picture}
    goto = ROOT

    mean_time_to_happen = {{ # This is in concurrence with the flag cooldown
        months = {MEAN_TIME}
    }}

    trigger = {{
        has_great_project = {{
            type = {self.monument['id']}
            tier = 1
        }}
        province_is_or_accepts_religion = {{
            religion = {self.religion}
        }}
        OR = {{
            NOT = {{
                has_province_flag = {FLAG}
            }}
            had_province_flag = {{
                flag = {FLAG}
                days = {COOLDOWN}
            }}
            AND = {{ # Reduced cooldown if you have <0 stability
                had_province_flag = {{
                    flag = {FLAG}
                    days = {COOLDOWN_REDUCED}
                }}
                NOT = {{
                    owner = {{
                        stability = 0
                    }}
                }}
            }}
        }}
    }}

    option = {{
        name = we_are_truly_blessed
        trigger = {{
        }}
        ai_chance = {{
            factor = 1
        }}
        set_province_flag = {FLAG}\n"""
        for i in self.effect.replace("\r", "").split("\n"):
            output += f"""        {i}\n"""
        #if not empty(self.tooltip):
        #    for i in range(len(self.tooltip)):
        #        output += f"""        custom_tooltip = {namespace}.{self.number}.tt{i+1}\n""" 
        output += f"""    }}
}}\n"""
        output = output.replace("<number>", str(self.number))
        return output
    
    def build_loc(self, namespace:str):
        output = f""" {namespace}.{self.number}.title:0 \"Blessing of {self.name}\"
 {namespace}.{self.number}.desc:0 \"The {self.monument['name']} has attracted the favour of {self.name}, {self.desc}.\"\n"""
        if not empty(self.tooltip):
            for i in range(len(self.tooltip)):
                output += f""" {namespace}.{self.number}.tt{i+1}:0 \"{self.tooltip[i]}\"\n"""
        return output

def main() -> None:
     # Things to mess with:
    MOD_NAME = "post_finem"
    MOD_ID = "pf"
    MOD_FILES_LOCATION = "C:/Users/Oliver Kirk/Documents/Paradox Interactive/Europa Universalis IV/mod"
    #MOD_FILES_LOCATION = "mod_files"
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"]
    TOKEN_LOCATION = f"subprograms/data/token.json"
    CREDENTIALS_LOCATION = f"subprograms/data/credentials.json"
    SHEETS_ID = "1jEof6L1EutUBgaS1NVqQaAPMekN0I3ogTC1ygvQTuiM"
    FILE_NAMES = {
        "events": f"{MOD_ID}_monuments_events.txt", 
        "localisation": f"{MOD_ID}_monuments_events_l_english.yml"
    }
    NAMESPACE = "{MOD_ID}_mon_events" # Changed namespace: pf_monuments -> pf_mon_events
    
    counter = 0
    god_list: list[god] = []
    range_list, index = sheets.retrieve_range_with_index(SHEETS_ID, "pantheon", SCOPES, TOKEN_LOCATION, CREDENTIALS_LOCATION)
    for row in range_list[1:]:
        if not empty(row[index["effect"]]):
            for [name, desc, religion] in [
                ["hellenic_name", "hellenic_desc", "hellenic"], 
                ["punic_name", "punic_desc", "punic_religion"], 
                ["romana_name", "romana_desc", "romana"], 
                ["norse_name", "norse_desc", "norse_pagan_reformed"]
            ]:
                if not empty(row[index[name]]) and not empty(row[index[desc]]):
                    counter += 1
                    god_list.append(god(
                        row[index[name]], 
                        row[index[desc]], 
                        row[index["effect"]], 
                        row[index["tooltips"]], 
                        religion, 
                        counter
                    ))
    #for i in god_list[0].build_event("pf_monuments", 1).split("\n"):
    #    print("|", i)
    
    
    events_scipt = f"namespace = {NAMESPACE}\n\n"
    for god_id in range(len(god_list)):
        events_scipt += god_list[god_id].build_event(NAMESPACE)
    file.write(f"{MOD_FILES_LOCATION}/{MOD_NAME}/events/{FILE_NAMES['events']}", events_scipt)
    
    loc_script = "l_english:\n we_are_truly_blessed:0 \"We are truly blessed!\"\n"
    for god_id in range(len(god_list)):
        loc_script += god_list[god_id].build_loc(NAMESPACE)
    file.write(f"{MOD_FILES_LOCATION}/{MOD_NAME}/localisation/{FILE_NAMES['localisation']}", loc_script, "utf-8-sig")
    
    return

if __name__ == "__main__":
    main()
