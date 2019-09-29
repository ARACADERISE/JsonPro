import os, json

# This file will read "setup.json" for anything important
# Most likely the whole file will be important since it's the setup for "NewJson"

ALERTS = {}
reset_data = {}
TO_IGNORE = []
write_ = ""

class read_setup_file:
  def __init__(self,data_to_upd,data):
    self.data_to_upd = data_to_upd
    self.data = data

  # @NOTE: If there are no "ALERTS" in "setup.json" this class-function will run, yet not do anything
  def get_alerts_in_setup(self):
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
        if GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST'] in open(GATHER['gath_data']['IGNORE_INFO']['ignore']['from_file'], 'r').read():
          TO_IGNORE.append(GATHER['gath_data']['IGNORE_INFO']['ignore']['REQUEST'])
          self.data_to_upd['IGNORED_DATA_INFO'].update({'return_status':'success'})
        else:
          self.data_to_upd['IGNORED_DATA_INFO'].update({'return_status':'failed'})
        with open(GATHER['gath_data']['IGNORE_INFO']['ignore']['store_in'],'w') as file:
          file.write('Request Type: Ignore\n')
          file.write('Ignore Info Found In: ' + GATHER['gath_data']['IGNORE_INFO']['ignore']['from_file'])
          file.write("\nRequested to ignore: "+write_)
          if len(TO_IGNORE) > 0:
            file.write("\nReturn Status: Success")
          else:
            file.write("\nReturn Status: Failed, info not found")
          file.close()
        self.data.update({'CREATED_FILE_DATA':self.data['IGNORE_INFO']})
    else:
      self.data.update({'EXTENDED_DATA':[{'CREATED_FILE_DATA':None,'ALERTS_DATA':None}]})
    # Reseting the file
    with open('setup.json','w') as file:
      to_json = json.dumps(reset_data,indent=2,sort_keys=False)
      file.write(to_json)
      file.close()
    
    self.data_to_upd.update({'to_ignore_in_all_files':TO_IGNORE})

# Reads the "setup.json"
def get_alerts(d_t_u,f_d):
  r_s_f = read_setup_file(d_t_u,f_d)
  r_s_f.get_alerts_in_setup()
