import os, json

# This file will read "setup.json" for anything important
# Most likely the whole file will be important since it's the setup for "NewJson"
# @NOTE: If there are no "ALERTS" in "setup.json" this file will run, yet not do anything

note_to_all_users = {}
reset_data = {}

def get_notes_in_setup(data_to_upd,file_dir):
  global note_to_all_users
  global reset_data

  opened_file = open(file_dir,'r').read()
  opened_file = json.loads(opened_file)

  if '"ALERTS":{' in open(file_dir,'r').read():
    note_to_all_users.update({'info':opened_file})

    for i in note_to_all_users:
      if note_to_all_users[i] == note_to_all_users['info']:
        data_to_upd['WARNING(S)'].append(note_to_all_users['info'])

  # Reseting the file
  with open(file_dir,'w') as file:
    to_json = json.dumps(reset_data)
    file.write(to_json)
    file.close()
