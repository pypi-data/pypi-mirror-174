#@title Inverters class { display-mode: "form" }
class Inverters():
    def __init__(self, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'):
      self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'

    def inverter(self,name):
      """
      Select the inverter from a provided list.
      To access the list, please use the method:
        list_inverters()

      Parameters
      ----------
      name : str
          The name of the inverter, as listed on the list.
      """
      import pandas as pd
      inverters = pd.read_csv(self.url).replace(" ", "")

      return inverters.loc[inverters['Name'] == name]

    def list_inverters(self,vac:int=None, pmax:int=None):
      """
      List of inverters provided by CEC.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'
          Url to the list of inverters. Can also be a .csv file.
      """
      import pandas as pd
      inverters = pd.read_csv(self.url).replace(" ", "")

      if vac != None:
        inverters = inverters.loc[inverters['Vac'] == int(vac)]
      if pmax != None:
        inverters = inverters.loc[inverters['Paco'] == int(pmax)]
      from tabulate import tabulate
      if inverters.shape[0] > 1000:
        step = 1000
      else:
        step = inverters.shape[0]
      for rows in range(0,inverters.shape[0],step-1):
        print(tabulate(inverters.head(rows), headers='keys', tablefmt='psql'))

      return inverters
