import subprograms.spreadsheet as sheets
import subprograms.file_edit as file
from mon_gen import empty, create_id_from_name

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
    
    def build_event(self, namespace: str, picture: str) -> str:
        MEAN_TIME = 6
        COOLDOWN = 365*10
        COOLDOWN_STAB_MULTIPLIER = 0.7
        COOLDOWN_UPGRADE_MULTIPLIER = 0.7
        PROV_FLAG = f"pf_mon_{self.monument['code']}_blessing_flag"
        COUNTRY_FLAG = f"pf_mon_{self.monument['code']}_recieved_blessing"
        
        output =  f"""province_event = {{ # Blessing of {self.name}\n"""
        output += f"""    id = {namespace}.{self.number}\n"""
        output += f"""    title = {namespace}.{self.number}.title\n"""
        output += f"""    desc = {namespace}.{self.number}.desc\n"""
        output += f"""    picture = {picture}\n"""
        output += f"""    goto = ROOT\n"""
        output += f"""    mean_time_to_happen = {{months = {MEAN_TIME}}} # This is in concurrence with the flag cooldown\n"""
        output += f"""    \n"""
        output += f"""    trigger = {{\n"""
        output += f"""        has_great_project = {{\n"""
        output += f"""            type = {self.monument['id']}\n"""
        output += f"""            tier = 1\n"""
        output += f"""        }}\n"""
        output += f"""        province_is_or_accepts_religion = {{religion = {self.religion}}}\n"""
        output += f"""        if = {{ # Reduced cooldown if the monument is tier 2\n"""
        output += f"""            limit = {{\n"""
        output += f"""                has_great_project = {{\n"""
        output += f"""                    type = {self.monument['id']}\n"""
        output += f"""                    tier = 2\n"""
        output += f"""                }}\n"""
        output += f"""            }}\n"""
        output += f"""            OR = {{\n"""
        output += f"""                NOT = {{has_province_flag = {PROV_FLAG}}}\n"""
        output += f"""                had_province_flag = {{\n"""
        output += f"""                    flag = {PROV_FLAG}\n"""
        output += f"""                    days = {int(COOLDOWN*COOLDOWN_UPGRADE_MULTIPLIER)}\n"""
        output += f"""                }}\n"""
        output += f"""                AND = {{ # Reduced cooldown if you have <0 stability\n"""
        output += f"""                    had_province_flag = {{\n"""
        output += f"""                        flag = {PROV_FLAG}\n"""
        output += f"""                        days = {int(COOLDOWN*COOLDOWN_STAB_MULTIPLIER*COOLDOWN_UPGRADE_MULTIPLIER)}\n"""
        output += f"""                    }}\n"""
        output += f"""                    NOT = {{owner = {{stability = 0}}}}\n"""
        output += f"""                }}\n"""
        output += f"""            }}\n"""
        output += f"""        }}\n"""
        output += f"""        else = {{\n"""
        output += f"""            OR = {{\n"""
        output += f"""                NOT = {{has_province_flag = {PROV_FLAG}}}\n"""
        output += f"""                had_province_flag = {{\n"""
        output += f"""                    flag = {PROV_FLAG}\n"""
        output += f"""                    days = {COOLDOWN}\n"""
        output += f"""                }}\n"""
        output += f"""                AND = {{ # Reduced cooldown if you have <0 stability\n"""
        output += f"""                    had_province_flag = {{\n"""
        output += f"""                        flag = {PROV_FLAG}\n"""
        output += f"""                        days = {int(COOLDOWN*COOLDOWN_STAB_MULTIPLIER)}\n"""
        output += f"""                    }}\n"""
        output += f"""                    NOT = {{owner = {{stability = 0}}}}\n"""
        output += f"""                }}\n"""
        output += f"""            }}\n"""
        output += f"""        }}\n"""
        output += f"""    }}\n\n"""
        # Options:
        for [requirements, effect, level] in [
            [
                [
                    f"""NOT = {{""", 
                    f"""    has_great_project = {{""", 
                    f"""        type = hall_of_pantheons""", 
                    f"""        tier = 3""", 
                    f"""    }}""", 
                    f"""}}"""
                ], 
                self.effect.replace("\r", "").split("\n"), 
                1
            ], 
            [
                [
                    f"""has_great_project = {{""", 
                    f"""    type = hall_of_pantheons""", 
                    f"""    tier = 3""", 
                    f"""}}"""
                ], 
                self.effect_upgraded.replace("\r", "").split("\n"), 
                1
            ]
        ]:
            #print("requirements", requirements)
            #print("effect", effect)
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
                output +=		f"""        set_province_flag = {PROV_FLAG}\n"""
                output +=		f"""        owner = {{\n"""
                output +=		f"""            set_country_flag = {COUNTRY_FLAG} # Used to track blessing in other places.\n"""
                output +=		f"""            if = {{\n"""
                output +=		f"""                limit = {{has_country_flag = pf_dda_blessing_money}}\n"""
                output +=		f"""                add_years_of_income = 0.25\n"""
                output +=		f"""            }}\n"""
                output +=		f"""        }}\n"""
                for i in effect:
                    output +=	f"""        {i}\n"""
                output = output.replace("<effect_level>", str(level))
                output +=		f"""    }}\n"""
        output +=				f"""}}\n"""
        for [text, replacement] in [
            ["<number>", str(self.number)], 
            ["<god>", self.name.lower()], 
        ]:
            output = output.replace(text, replacement)
        return output
    
    def build_loc(self, namespace: str) -> str:
        output = ""
        output += f" {namespace}.{self.number}.title:0 \"Blessing of {self.name}\"\n"
        output += f" {namespace}.{self.number}.desc:0 \"The {self.monument['name']} has attracted the favour of {self.name}, {self.desc}.\"\n"
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

def update_events(const_dict: dict) -> None:
    NAMESPACE = f"{const_dict['mod_id']}_mon_events"
    EVENT_SHEET_ID = "1STk5w69_RLVxANKPXOg9YSLmZvqtrF2sWsp9e-n2fm8"
    
    event_output = ""
    loc_output = ""
    event_count = 0
    
     # Events
    event_list, event_index =   sheets.retrieve_range_with_index(EVENT_SHEET_ID, "events",  const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    option_list, option_index = sheets.retrieve_range_with_index(EVENT_SHEET_ID, "options", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    for row in event_list[1:]:
        #print(event_index)
        if not empty(row[event_index["name"]]) and row[event_index["enable"]] == "TRUE":
            event_count += 1
             # Event
            event_output +=                 f"{row[event_index['type']]}_event = {{\n"
            event_output +=                 f"    id = {NAMESPACE}.{row[event_index['id']]}\n"
            event_output +=                 f"    title = {NAMESPACE}.{row[event_index['id']]}.title\n"
            event_output +=                 f"    desc = {NAMESPACE}.{row[event_index['id']]}.desc\n"
            if not empty(row[event_index["image"]]):
                event_output +=             f"    picture = {row[event_index['image']]}\n"
            else:
                event_output +=             f"    picture = BIG_BOOK_eventPicture\n"
            if empty(row[event_index['mtth']]):
                event_output +=             f"    is_triggered_only = yes\n"
            else:
                mtth = row[event_index["mtth"]].split("\n")
                event_output +=             f"    mean_time_to_happen = {{\n"
                for i in range(len(mtth)):
                    if not empty(mtth[i]):
                        event_output +=     f"        {mtth[i]}\n"
                event_output +=             f"    }}\n"
                event_output +=             f"    trigger = {{\n"
                for i in row[event_index["trigger"]].split("\n"):
                    if not empty(i):
                        event_output +=     f"        {i}\n"
                event_output +=             f"    }}\n"
             # loc
            loc_output += f" {NAMESPACE}.{row[event_index['id']]}.title:0 \"{row[event_index['name']]}\"\n"
            loc_output += f" {NAMESPACE}.{row[event_index['id']]}.desc:0 \"{row[event_index['desc']]}\"\n"
            tt = row[event_index["tooltip"]].split("\n")
            for i in range(len(tt)):
                if not empty(tt[i]):
                    loc_output += f" {NAMESPACE}.{row[event_index['id']]}.tt_e{event_count}_{i+1}:0 \"{tt[i]}\"\n"
            option_count = 0
            for option in option_list[1:]:
                if option[option_index["linked_event"]] == row[event_index["id"]] and not empty(option[option_index["name"]]):
                    option_count += 1
                     # Option event
                    event_output +=         f"    option = {{\n"
                    event_output +=         f"        name = {NAMESPACE}.{row[event_index['id']]}.o{option_count}\n"
                    event_output +=         f"        trigger = {{\n"
                    for i in option[option_index["trigger"]].split("\n"):
                        if not empty(i):
                            event_output += f"            {i}\n"
                    event_output +=         f"        }}\n"
                    event_output +=         f"        ai_chance = {{\n"
                    for i in option[option_index["ai"]].split("\n"):
                        if not empty(i):
                            event_output += f"            {i}\n"
                    event_output +=         f"        }}\n"
                    for i in option[option_index["effect"]].split("\n"):
                        if not empty(i):
                            event_output += f"        {i}\n"
                    event_output +=         f"    }}\n"
                     # Option loc
                    loc_output += f" {NAMESPACE}.{row[event_index['id']]}.o{option_count}:0 \"{option[option_index['name']]}\"\n"
                    tt = option[option_index["tooltip"]].split("\n")
                    for i in range(len(tt)):
                        if not empty(tt[i]):
                            loc_output += f" {NAMESPACE}.{row[event_index['id']]}.tt_o{option_count}_{i+1}:0 \"{tt[i]}\"\n"
                    for [text, replacement] in [
                        ["<o_tt>", f"{NAMESPACE}.{row[event_index['id']]}.tt_o{option_count}_"]
                    ]:
                        event_output = event_output.replace(text, replacement)
            for [text, replacement] in [
                ["<e_tt>", f"{NAMESPACE}.{row[event_index['id']]}.tt_e{event_count}_"]
            ]:
                event_output = event_output.replace(text, replacement)
            event_output +=                 f"}}\n"
    
    
    
     # Hall of Pantheons events
    hop_event_list = []
    hall_of_pantheons = hop(NAMESPACE)
    range_list, index = sheets.retrieve_range_with_index(const_dict['sheets_id'], "pantheon", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'])
    for row in range_list[1:]:
        if not empty(row[index["effect"]]) and row[index["enable"]] == "TRUE":
            for [name, desc, religion] in [
                ["hellenic_name", "hellenic_desc", "hellenic"], 
                ["punic_name", "punic_desc", "punic_religion"], 
                ["romana_name", "romana_desc", "romana"], 
                ["norse_name", "norse_desc", "norse_pagan_reformed"]
            ]:
                if not empty(row[index[name]]) and not empty(row[index[desc]]):
                    event_count += 1
                    god = hop_god(
                            row[index[name]], 
                            row[index[desc]], 
                            row[index["effect"]], 
                            row[index["effect2"]], 
                            row[index["tooltip"]], 
                            row[index["tooltip2"]], 
                            religion, 
                            event_count
                        )
                    hall_of_pantheons.append_to_god_list(god)
    hop_event_list.append(hall_of_pantheons)
    
    
     # Write events file
    events_scipt = f"namespace = {NAMESPACE}\n\n{event_output}"
    for event_id in range(len(hop_event_list)):
        events_scipt += hop_event_list[event_id].build_event()
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/events/{const_dict['mod_id']}_mon_events.txt", events_scipt)
    
     # Write loc file
    loc_script = f"l_english:\n{loc_output}"
    for event_id in range(len(hop_event_list)):
        loc_script += hop_event_list[event_id].build_loc()
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/localisation/{const_dict['mod_id']}_mon_events_l_english.yml", loc_script, "utf-8-sig")
    
    return

def update_modifiers(const_dict: dict) -> None:
    modifier_output = ""
    loc_output = "l_english:\n"
    
    range_list, index = sheets.retrieve_range_with_index(const_dict['sheets_id'], "modifiers", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'])
    #print("modifiers\n", range_list)
    for row in range_list[1:]:
        effects = row[index["effect"]].replace("\r", "").split("\n")
        if not empty(row[index["effect"]]) and row[index["enable"]] == "TRUE":
             # modifier_output
            modifier_output += f"{row[index['id']]} = {{\n"
            for effect in effects:
                #print("effect", effect)
                modifier_output += f"	{effect}\n"
            modifier_output += f"}}\n\n"
             # loc_output
            loc_output += f" {row[index['id']]}:0 \"{row[index['name']]}\"\n"
            if empty(row[index['description']]):
                loc_output += f" desc_{row[index['id']]}:0 \"\"\n"
            else:
                loc_output += f" desc_{row[index['id']]}:0 \"{row[index['description']]}\"\n"
    
    
    #print("m\n", modifier_output)
    #print("l\n", loc_output)
    #input()
     # Write modifier file
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/common/event_modifiers/{const_dict['mod_id']}_mon_modifiers.txt", modifier_output)
    
     # Write loc file
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/localisation/{const_dict['mod_id']}_mon_modifiers_l_english.yml", loc_output, "utf-8-sig")
    return

def update_missions(const_dict: dict) -> None:
    MISSION_SHEET_ID = "13sd1VM6ISk1hjoFNsIZOFICxRCNhMYt3xA3owOvwM5c"
    MISSION_CODE = f"{const_dict['mod_id']}_dda" # This should be unique to this mission tree
    mission_output = ""
    loc_output = "l_english:\n"
    
    branch_list, branch_index = sheets.retrieve_range_with_index(MISSION_SHEET_ID, "branch",          const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    trigger_list, _           = sheets.retrieve_range_with_index(MISSION_SHEET_ID, "mission_trigger", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    effect_list,  _           = sheets.retrieve_range_with_index(MISSION_SHEET_ID, "mission_effect",  const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    tt_list,      _           = sheets.retrieve_range_with_index(MISSION_SHEET_ID, "mission_tooltip", const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    other_list,   _           = sheets.retrieve_range_with_index(MISSION_SHEET_ID, "mission_other",   const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    name_list,    _           = sheets.retrieve_range_with_index(MISSION_SHEET_ID, "mission_name",    const_dict['scopes'], const_dict['token_location'], const_dict['credentials_location'], ["\r"])
    id_list = [["" for i in range(5)] for j in range(len(effect_list))]
    
     # branch/slot = column, position = row
    for slot in range(1, 5):
        potential_list = []
        mission_output += f"{MISSION_CODE}_{slot+1} = {{\n"
        for row in branch_list[1:]:
            if str(row[branch_index["branch"]]) in ["all", str(slot+1)]:
                for i in row[branch_index["other"]].split("\n"):
                    if not empty(i):
                        mission_output += f"    {i}\n"
                for i in row[branch_index["potential"]].split("\n"):
                    potential_list.append(i)
        mission_output += f"    potential = {{\n"
        for i in potential_list:
            if not empty(i):
                mission_output += f"        {i}\n"
        mission_output += f"    }}\n"
        for position in range(len(effect_list)):
            #print("name_list", name_list)
            print(position, slot)
            name_data = name_list[position][slot].split("\n")
            name, picture, desc = "", "mission_unknown_mission", [""]
            if len(name_data) == 1:   name                = name_data[0] # name
            elif len(name_data) == 2: name, picture       = name_data[0], name_data[1] # name, picture
            else:                     name, picture, desc = name_data[0], name_data[1], name_data[2:] # name, picture, description
            name_id = create_id_from_name(name)
            mission_id = f"{MISSION_CODE}_{name_id}"
            if empty(picture): picture = "mission_unknown_mission"
            #print("name_data", name_data)
            
            if not empty(name_id):
                id_list[position][slot] = mission_id
                #print("mission_id", mission_id, type(mission_id))
                #print("name", name)
                # mission_output
                mission_output += f"    {mission_id} = {{\n"
                mission_output += f"        position = {position+1}\n"
                mission_output += f"        icon = {picture}\n"
                for i in other_list[position][slot].split("\n"):
                    if not empty(i):
                        mission_output += f"        {i}\n"
                mission_output += f"        trigger = {{\n"
                for i in trigger_list[position][slot].split("\n"):
                    if not empty(i):
                        mission_output += f"            {i}\n"
                mission_output += f"        }}\n"
                mission_output += f"        effect = {{\n"
                for i in effect_list[position][slot].split("\n"):
                    if not empty(i):
                        mission_output += f"            {i}\n"
                mission_output += f"        }}\n"
                mission_output += f"    }}\n"
                
                # loc_output
                loc_output += f" {mission_id}_title:0 \"{name}\"\n"
                loc_output += f" {mission_id}_desc:0 \""
                for i in desc:
                    if not empty(i):
                        loc_output += f"{i}"
                loc_output += f"\"\n"
                #print("tt_list", tt_list)
                #print(position, slot)
                curr_tt = tt_list[position][slot].split("\n")
                #print("curr_tt", curr_tt)
                for i in range(len(curr_tt)):
                    if not empty(curr_tt[i]):
                        loc_output += f" {MISSION_CODE}_{mission_id}_tt{i+1}:0 \"{curr_tt[i]}\"\n"
                
                
                # Replace <> instances
                for [text, replacement] in [
                    ["<tooltip>", f"{MISSION_CODE}_{mission_id}_tt"]
                ]:
                    mission_output = mission_output.replace(text, replacement)
                    loc_output = loc_output.replace(text, replacement)
                    
        mission_output += f"}}\n"
        
    for i in id_list:
        print(i)
    for col in range(5):
        for row in range(len(effect_list)):
            print(col, row)
            mission_output = mission_output.replace(f"<m_{col+1}_{row+1}>", id_list[row][col])
    
    
    #print("\nmission_output\n", mission_output)
    #print("\nloc_output\n", loc_output)
    
     # Write mission file
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/missions/{MISSION_CODE}_missions.txt", mission_output)
    
     # Write loc file
    file.write(f"{const_dict['mod_files_location']}/{const_dict['mod_name']}/localisation/{MISSION_CODE}_missions_l_english.yml", loc_output, "utf-8-sig")
    return

def main() -> None:
     # Things to mess with:
    CONSTS = {
        "mod_name": "post_finem", 
        "mod_id": "pf", 
        "mod_files_location": "C:/Users/okthe/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod", 
        #"mod_files_location": "mod_files", 
        "scopes": ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"], 
        "token_location": f"subprograms/data/token.json", 
        "credentials_location": f"subprograms/data/credentials.json", 
        "sheets_id": "1jEof6L1EutUBgaS1NVqQaAPMekN0I3ogTC1ygvQTuiM"
    }
    
    
    
    update_events(CONSTS)
    update_modifiers(CONSTS)
    update_missions(CONSTS)
    return

if __name__ == "__main__":
    main()
