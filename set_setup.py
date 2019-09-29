import os, json
from colorama import Fore, Style

# This file will read "setup.json" for anything important
# Most likely the whole file will be important since it's the setup for "NewJson"

ALERTS = {}
reset_data = {}
TO_IGNORE = []
write_ = ""

class read_setup_file:
  def __init__(self,data_to_upd,data,db_data):
    self.data_to_upd = data_to_upd
    self.data = data
    self.db_data = db_data

  # NOTE: This function will not run if specific key data points are not found within setup.json
  def get_data_in_setup(self):
    global ALERTS
    global reset_data
    global write_
    global TO_IGNORE

    if '"ALERTS":{' in self.data:
      ALERTS.update({'info':self.data})

      if 'note_to_all_users' in ALERTS['info']['ALERTS'] or "'note_to_all_users':[" or "'note_to_all_users':{" in ALERTS['info']['ALERTS']:
        for i in ALERTS:
          if ALERTS[i] == ALERTS['info']:
            self.data_to_upd['WARNING(S)'].append(ALERTS['info']['ALERTS'])
        self.data.update({'ALERTS_DATA':self.data['ALERTS']})
    elif 'IGNORE_INFO' in self.data:
      GATHER = {'gath_data':self.data}
      if 'ignore' in GATHER['gath_data']['IGNORE_INFO']:
        if not 'store_in' in GATHER['gath_data']['IGNORE_INFO']['ignore']:
          GATHER['gath_data']['IGNORE_INFO']['ignore'].update({"store_in":"ignore_data.txt"})
        if not '.' in GATHER['gath_data']['IGNORE_INFO']['ignore']['store_in']:
          raise Exception("Must declare type of file: " + GATHER['gath_data']['IGNORE_INFO']['warn_info']['store_in'])
        if '.json' in GATHER['gath_data']['IGNORE_INFO']['ignore']['store_in']:
          raise Exception("cannot write to .json files")
        if 'REQUEST' in GATHER['gath_data']['IGNORE_INFO']['ignore']:
          write_ = GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST']
        if not 'from_file' in GATHER['gath_data']['IGNORE_INFO']['ignore']:
          raise Exception('Error: No "from_file" located within setup.json\nCannot locate ' + GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST'] + 'from file of ')
        if GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST'] in open(GATHER['gath_data']['IGNORE_INFO']['ignore']['from_file'], 'r').read():
          TO_IGNORE.append(GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST'])
          self.data_to_upd['IGNORED_DATA_INFO'].update({'status':'success'})
        else:
          self.data_to_upd['IGNORED_DATA_INFO'].update({'status':'failed'})
          TO_IGNORE.append('no_data')
        with open(GATHER['gath_data']['IGNORE_INFO']['ignore']['store_in'],'w') as file:
          if 'ignore' in GATHER['gath_data']['IGNORE_INFO']:
            file.write('Request Type: Ignore\n')
          file.write('Ignore Info Found In: ' + GATHER['gath_data']['IGNORE_INFO']['ignore']['from_file'])
          file.write("\nRequested to ignore: "+write_)
          if GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST'] == TO_IGNORE[0]:
            file.write("\nStatus: Success")
          else:
            file.write("\nStatus: Failed, info not found")
          file.close()
        self.data.update({'CREATED_FILE_DATA':self.data['IGNORE_INFO']})
    else:
      self.data.update({'EXTENDED_DATA':[{'CREATED_FILE_DATA':None,'ALERTS_DATA':None}]})
    # Reseting the file
    with open('setup.json','w') as file:
      to_json = json.dumps(reset_data,indent=2,sort_keys=False)
      file.write(to_json)
      file.close()
    
    self.data_to_upd['DEFAULT'].update({'to_ignore_in_all_files':TO_IGNORE})
    self.db_data['setup_file_info'].append({'IGNORE_DATA':{'request_to_ignore':TO_IGNORE,'found_in_file':GATHER['gath_data']['IGNORE_INFO']['ignore']['from_file'],'status':self.data_to_upd['IGNORED_DATA_INFO']['status']}})

    print(Fore.GREEN+Style.BRIGHT+"[+]" + Fore.WHITE + " Setup file check complete")

# Reads the "setup.json"
def get_data(d_t_u,f_d,db_data):
  r_s_f = read_setup_file(d_t_u,f_d,db_data)
  r_s_f.get_data_in_setup()
