import os, json

# This file will read "setup.json" for anything important
# Most likely the whole file will be important since it's the setup for "NewJson"

ALERTS = {}
reset_data = {}

class read_setup_file:
  def __init__(self,data_to_upd,file_dir):
    self.data_to_upd = data_to_upd
    self.file_dir = file_dir

  # @NOTE: If there are no "ALERTS" in "setup.json" this file will run, yet not do anything
  def get_alerts_in_setup(self):
    global ALERTS
    global reset_data

    opened_file = open(self.file_dir,'r').read()
    opened_file = json.loads(opened_file)

    if '"ALERTS":{' in open(self.file_dir,'r').read():
      ALERTS.update({'info':opened_file})

      for i in ALERTS:
        if ALERTS[i] == ALERTS['info']:
          self.data_to_upd['WARNING(S)'].append(ALERTS['info'])

    # Reseting the file
    with open(self.file_dir,'w') as file:
      to_json = json.dumps(reset_data)
      file.write(to_json)
      file.close()

# Reads the "setup.json"
def get_alerts(d_t_u,f_d):
  r_s_f = read_setup_file(d_t_u,f_d)
  r_s_f.get_alerts_in_setup()
