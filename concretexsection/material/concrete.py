# class for concrete material for Metric and US/Imperial units

import math

class aci_imperial:

    def __init__(self, fc_ksi, density_pcf=145, lightweight=False):
        '''

        ACI Concrete Material in Imperial Units
        
        '''
        self.fc_ksi = fc_ksi
        self.fc_psi = self.fc_ksi*1000.0
        self.Ec_psi = math.pow(density_pcf,1.5)*33*math.sqrt(self.fc_psi)
        self.Ec_ksi = self.Ec_psi/1000.0

        self.units = "Imperial/US"
