import sys, os, json, time

# Getting the users directory
USERS_DIR = str(sys.path[0])
USERS_DIR = os.path.join(USERS_DIR,"")
FILE_NAME = ""
DEFAULT_DATA = {"WARNING":"DO NOT DELETE ANY INFORMATION IN THIS FILE AFTER YOU'VE ALREADY HAD THE PROGRAM IMPLEMENT DATA INTO IT","DEFAULT":{"return_types":["true","false"]}}
FILE_DIR = []

def connect_to_your_file(file_name):
  global FILE_NAME
  global FILE_DIR
  FILE_NAME = file_name
  if FILE_NAME == 'setup.json':
    if os.path.exists(USERS_DIR+file_name):
      FILE_DIR = [USERS_DIR+file_name]
      return FILE_DIR
    else:
      raise NotADirectoryError('Error at line 9 in main.py\nNo such directory: ' + USERS_DIR+file_name)
  else:
    raise NameError("setup.json name expected, got " + FILE_NAME)

def inject_default_setting():
  global FILE_DIR
  global DEFAULT_DATA
  global USERS_DIR

  if not os.path.exists(USERS_DIR+'db.json'):
    print("There was an error finding " + USERS_DIR+'db.json' + "\nRE-INSTALLING..\n\n")
    time.sleep(4)
    os.system('cd && rm -rf NewJson && ls')
  if not os.path.exists(USERS_DIR+'setup.json'):
    print("There was an error finding " + USERS_DIR+'setup.json' + "\nRE-INSTALLING..\n\n")
    time.sleep(4)
    os.system('cd && rm -rf NewJson && ls')

  opened_db_file = open('db.json','r').read()
  DB_JSON_DATA = json.loads(opened_db_file)

  if DB_JSON_DATA['setup_file_info'] == [] or DB_JSON_DATA['setup_file_info'] == ["error"]:
    file_name = input('.json File Name: ')
    PATH_OF_FILE = os.path.abspath(file_name)
    # We don't want db.json to be vulnerable to being connected to
    if file_name == 'db.json':
      time.sleep(4)
      raise Exception("Error @ line 29: Cannot connect to " + PATH_OF_FILE +"\nIs db file")
    if not os.path.exists(PATH_OF_FILE):
      raise FileNotFoundError("Error: " + PATH_OF_FILE + " not a directory")
    elif file_name == 'setup.json' and os.path.exists(PATH_OF_FILE):
      FILE_DIR = [USERS_DIR+file_name]
      DEFAULT_DATA.update({"original_file_data":json.loads(open(FILE_DIR[0],'r').read())})
    else:
      raise NameError("setup.json name expected, got " + file_name)
    if not 'DEFAULT' in open(FILE_DIR[0],'r').read() or not '"original_file_data"' in open(FILE_DIR[0],'r').read():
      try:
        connect_to_your_file(file_name)
        while FILE_DIR[0] == USERS_DIR+FILE_NAME:
          with open(FILE_DIR[0],'w') as file:
            to_json = json.dumps(DEFAULT_DATA,indent=2,sort_keys=False)
            file.write(to_json)
            file.close()
          time.sleep(4)
          break
      except NameError as n_e:
        print(n_e)
    if 'WARNING' in DEFAULT_DATA['original_file_data']:
      with open(FILE_DIR[0],'w') as file:
        REPLACE = {}
        to_json = json.dumps(REPLACE)
        file.write(to_json)
        file.close()
      raise Exception("\n\nCannot execute due to transparent data being same as injection:\n"+str(DEFAULT_DATA['original_file_data'])+"\n\n"+FILE_DIR[0]+" (or setup.json) has been rendered back to {}. please go back to github and edit the file. \n\nHINT: delete the pre-existing setup.json on github, make sure to copy pre-json-code that you had typed, make a new setup.json, and paste the pre-existing code.")
    DB_JSON_DATA['setup_file_info'].append({"default_setup_file_name":f'{file_name}',"valid":True,"setup.json::-->FILE_INFO":DEFAULT_DATA['original_file_data']})

    op = open('db.json','w')
    to_json = json.dumps(DB_JSON_DATA,indent=2,sort_keys=False)
    op.write(to_json)
    op.close()
      
  else:
    pass

inject_default_setting()
