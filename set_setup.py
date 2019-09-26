import os, json

# This file will read "setup.json" for anything important
# Most likely the whole file will be important since it's the setup for "NewJson"

ALERTS = {}
reset_data = {}
write_ = ""

class read_setup_file:
  def __init__(self,data_to_upd,data):
    self.data_to_upd = data_to_upd
    self.data = data

  # @NOTE: If there are no "ALERTS" in "setup.json" this class-function will run, yet not do anything
  def get_alerts_in_setup(self):
    global ALERTS
    #global reset_data
    global write_

    if '"ALERTS":{' in self.data:
      ALERTS.update({'info':self.data})

      if 'note_to_all_users' in ALERTS['info']['ALERTS'] or "'note_to_all_users':[" or "'note_to_all_users':{" in ALERTS['info']['ALERTS']:
        for i in ALERTS:
          if ALERTS[i] == ALERTS['info']:
            self.data_to_upd['WARNING(S)'].append(ALERTS['info']['ALERTS'])
        self.data.update({'ALERTS_DATA':self.data['ALERTS']})
    elif 'CREATE' in self.data:
      GATHER = {'gath_data':self.data}
      if 'warn_file' in GATHER['gath_data']['CREATE']:
        if not 'title' in GATHER['gath_data']['CREATE']['warn_file']:
          GATHER['gath_data']['CREATE']['warn_file'].update({"title":"warn_file.txt"})
        if not '.' in GATHER['gath_data']['CREATE']['warn_file']['title']:
          raise Exception("Must declare type of file: " + GATHER['gath_data']['CREATE']['warn_info']['title'])
        if '.json' in GATHER['gath_data']['CREATE']['warn_file']['write']:
          raise Exception("cannot write to .json files")
        if 'write' in GATHER['gath_data']['CREATE']['warn_file']:
          write_ = GATHER['gath_data']['CREATE']['warn_file']['write']
        with open(GATHER['gath_data']['CREATE']['warn_file']['title'],'w') as file:
            file.write(write_)
            file.close()
        self.data.update({'CREATED_FILE_DATA':self.data['CREATE']})
    else:
      self.data.update({'EXTENDED_DATA':[{'CREATED_FILE_DATA':None,'ALERTS_DATA':None}]})
    # Reseting the file
    with open('setup.json','w') as file:
      to_json = json.dumps(self.data,indent=2,sort_keys=False)
      file.write(to_json)
      file.close()

# Reads the "setup.json"
def get_alerts(d_t_u,f_d):
  r_s_f = read_setup_file(d_t_u,f_d)
  r_s_f.get_alerts_in_setup()
