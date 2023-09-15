import subprograms.spreadsheet as sheets
import subprograms.file_edit as file
from mon_gen import empty

class hop_god:
    def __init__(self, name: str, desc: str, effect: str, effect_upgraded: str, tooltip: str, tooltip_upgraded: str, religion: str, god_no: int) -> None:
        self.name = name
        self.desc = desc
        self.effect = effect
        self.effect_upgraded = effect_upgraded
        self.tooltip = tooltip.replace("\r", "").split("\n")
        self.tooltip_upgraded = tooltip_upgraded.replace("\r", "").split("\n")
        self.religion = religion
        self.number = god_no
        self.monument = {
            "name": "Hall of Pantheons", 
            "id": "hall_of_pantheons", 
            "code": "hop"
        }
        return
    
    def build_event(self, namespace: str, picture: str = "NORSE_TEMPLE_eventPicture") -> str:
        MEAN_TIME = 6
        COOLDOWN = 365*4
        COOLDOWN_REDUCED = 365*3
        FLAG = f"pf_mon_{self.monument['code']}_blessing_flag"
        
        output =  f"""province_event = {{ # Blessing of {self.name}\n"""
        output += f"""    id = {namespace}.{self.number}\n"""
        output += f"""    title = {namespace}.{self.number}.title\n"""
        output += f"""    desc = {namespace}.{self.number}.desc\n"""
        output += f"""    picture = {picture}\n"""
        output += f"""    goto = ROOT\n"""
        output += f"""\n"""
        output += f"""    mean_time_to_happen = {{ # This is in concurrence with the flag cooldown\n"""
        output += f"""        months = {MEAN_TIME}\n"""
        output += f"""    }}\n"""
        output += f"""\n"""
        output += f"""    trigger = {{\n"""
        output += f"""        has_great_project = {{\n"""
        output += f"""            type = {self.monument['id']}\n"""
        output += f"""            tier = 1\n"""
        output += f"""        }}\n"""
        output += f"""        province_is_or_accepts_religion = {{\n"""
        output += f"""            religion = {self.religion}\n"""
        output += f"""        }}\n"""
        output += f"""        OR = {{\n"""
        output += f"""            NOT = {{\n"""
        output += f"""                has_province_flag = {FLAG}\n"""
        output += f"""            }}\n"""
        output += f"""            had_province_flag = {{\n"""
        output += f"""                flag = {FLAG}\n"""
        output += f"""                days = {COOLDOWN}\n"""
        output += f"""            }}\n"""
        output += f"""            AND = {{ # Reduced cooldown if you have <0 stability\n"""
        output += f"""                had_province_flag = {{\n"""
        output += f"""                    flag = {FLAG}\n"""
        output += f"""                    days = {COOLDOWN_REDUCED}\n"""
        output += f"""                }}\n"""
        output += f"""                NOT = {{\n"""
        output += f"""                    owner = {{\n"""
        output += f"""                        stability = 0\n"""
        output += f"""                    }}\n"""
        output += f"""                }}\n"""
        output += f"""            }}\n"""
        output += f"""        }}\n"""
        output += f"""    }}\n\n"""
        for [requirements, effect] in [
            [
                [
                    f"""NOT = {{""", 
                    f"""    has_great_project = {{""", 
                    f"""        type = hall_of_pantheons""", 
                    f"""        tier = 3""", 
                    f"""    }}""", 
                    f"""}}"""
                ], 
                self.effect.replace("\r", "").split("\n")
            ], 
            [
                [
                    f"""has_great_project = {{""", 
                    f"""    type = hall_of_pantheons""", 
                    f"""    tier = 3""", 
                    f"""}}"""
                ], 
                self.effect_upgraded.replace("\r", "").split("\n")
            ]
        ]:
            print("requirements", requirements)
            print("effect", effect)
            if not empty(effect):
                output +=		f"""    option = {{\n"""
                output +=		f"""        name = pf_mon_events_we_are_truly_blessed\n"""
                output +=		f"""        trigger = {{\n"""
                for i in requirements:
                    output +=	f"""            {i}\n"""
                output +=		f"""        }}\n"""
                output +=		f"""        ai_chance = {{\n"""
                output +=		f"""            factor = 1\n"""
                output +=		f"""        }}\n"""
                output +=		f"""        set_province_flag = {FLAG}\n"""
                for i in effect:
                    output +=	f"""        {i}\n"""
        output +=				f"""    }}\n"""
        output +=				f"""}}\n"""
        for [text, replacement] in [["<effect_level>", 1]]:
            pass
        output = output.replace("<number>", str(self.number)).replace("<god>", self.name.lower())
        return output
    
    def build_loc(self, namespace: str) -> str:
        output = f""" {namespace}.{self.number}.title:0 \"Blessing of {self.name}\"
 {namespace}.{self.number}.desc:0 \"The {self.monument['name']} has attracted the favour of {self.name}, {self.desc}.\"\n"""
        if not empty(self.tooltip):
            for i in range(len(self.tooltip)):
                output += f""" {namespace}.{self.number}.tt{i+1}_1:0 \"{self.tooltip[i]}\"\n"""
        if not empty(self.tooltip_upgraded):
            for i in range(len(self.tooltip_upgraded)):
                output += f""" {namespace}.{self.number}.tt{i+1}_2:0 \"{self.tooltip_upgraded[i]}\"\n"""
        #print("god loc", output)
        return output

class hop:
    def __init__(self, namespace: str) -> None:
        self.god_list: list[hop_god] = []
        self.namespace = namespace
        return
    def append_to_god_list(self, god: hop_god) -> None:
        self.god_list.append(god)
        return
    def build_event(self, picture: str = "NORSE_TEMPLE_eventPicture") -> str:
        output = ""
        for god in self.god_list:
            output += f"{god.build_event(self.namespace, picture)}"
        #print("event", output)
        return output
    def build_loc(self) -> str:
        output = " pf_mon_events_we_are_truly_blessed:0 \"We are truly blessed!\"\n"
        for god in self.god_list:
            output += f"{god.build_loc(self.namespace)}"
        #print("loc", output)
        return output

class mnd:
    def __init__(self) -> None:
        return

def update_events(const_dict: dict) -> None:
    NAMESPACE = f"{const_dict['mod_id']}_mon_events"
    
    event_list = []
    
     # Hall of Pantheons events
    hall_of_pantheons = hop(NAMESPACE)
    god_counter = 0
    range_list, index = sheets.retrieve_range_with_index(const_dict['sheets_id'], "pantheon", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'])
    for row in range_list[1:]:
        if not empty(row[index["effect"]]) and row[index["enabled"]] == "y":
            for [name, desc, religion] in [
                ["hellenic_name", "hellenic_desc", "hellenic"], 
                ["punic_name", "punic_desc", "punic_religion"], 
                ["romana_name", "romana_desc", "romana"], 
                ["norse_name", "norse_desc", "norse_pagan_reformed"]
            ]:
                if not empty(row[index[name]]) and not empty(row[index[desc]]):
                    god_counter += 1
                    god = hop_god(
                            row[index[name]], 
                            row[index[desc]], 
                            row[index["effect"]], 
                            row[index["effect2"]], 
                            row[index["tooltip"]], 
                            row[index["tooltip2"]], 
                            religion, 
                            god_counter
                        )
                    hall_of_pantheons.append_to_god_list(god)
    event_list.append(hall_of_pantheons)
    
    
     # Write events file
    events_scipt = f"namespace = {NAMESPACE}\n\n"
    for event_id in range(len(event_list)):
        events_scipt += event_list[event_id].build_event()
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/events/{const_dict['mod_id']}_mon_events.txt", events_scipt)
    
     # Write loc file
    loc_script = "l_english:\n"
    for event_id in range(len(event_list)):
        loc_script += event_list[event_id].build_loc()
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/localisation/{const_dict['mod_id']}_mon_events_l_english.yml", loc_script, "utf-8-sig")
    
    return

def update_modifiers(const_dict: dict) -> None:
    modifier_output = ""
    loc_output = "l_english:\n"
    
    range_list, index = sheets.retrieve_range_with_index(const_dict['sheets_id'], "modifiers", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'])
    #print("modifiers\n", range_list)
    for row in range_list[1:]:
        effects = row[index["effect"]].replace("\r", "").split("\n")
        if not empty(row[index["effect"]]) and row[index["enabled"]] == "TRUE":
             # modifier_output
            modifier_output += f"{row[index['id']]} = {{\n"
            for effect in effects:
                #print("effect", effect)
                modifier_output += f" {effect}\n"
            modifier_output += f"}}\n"
             # loc_output
            loc_output += f" {row[index['id']]}:0 \"{row[index['name']]}\"\n"
            loc_output += f" desc_{row[index['id']]}:0 \"{row[index['description']]}\"\n"
    
    
    #print("m\n", modifier_output)
    #print("l\n", loc_output)
    #input()
     # Write modifier file
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/common/event_modifiers/{const_dict['mod_id']}_mon_modifiers.txt", modifier_output)
    
     # Write loc file
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/localisation/{const_dict['mod_id']}_mon_modifiers_l_english.yml", loc_output, "utf-8-sig")
    
    return

def main() -> None:
     # Things to mess with:
    CONSTS = {
        "mod_name": "post_finem", 
        "mod_id": "pf", 
        "mod_files_location": "C:/Users/Oliver Kirk/Documents/Paradox Interactive/Europa Universalis IV/mod", 
        #"mod_files_location": "mod_files", 
        "scopes": ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"], 
        "token_location": f"subprograms/data/token.json", 
        "credentials_location": f"subprograms/data/credentials.json", 
        "sheets_id": "1jEof6L1EutUBgaS1NVqQaAPMekN0I3ogTC1ygvQTuiM"
    }
    
    
    
    update_events(CONSTS)
    update_modifiers(CONSTS)
    return

if __name__ == "__main__":
    main()
