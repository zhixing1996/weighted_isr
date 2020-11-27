#/usr/bin/env python
#-*- Coding: UTF-8 -*-

__author__ = "Lianjin WU <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING, Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import ROOT as root
import math

class xs_func():
    def __init__(self, nbin, lower, upper, mass1, mass2):
        """ bin, lower, upper limits for PHSP factor, three particle masses  """
        self._gr = root.TGraph()
        for ibin in range(nbin):
            m0 = lower + ibin*(upper - lower)/float(nbin)
            self._gr.SetPoint(ibin, lower + ibin*(upper - lower)/float(nbin), self.__getPHSPFactor(m0, mass1, mass2))

    ### three body PHSP factor calculation based on TF1
    ### m0 -> m1 + m2 + m3
    def __getPHSPFactor(self, m0, m1, m2):
        s = m0*m0
        denominator = 2*s
        if (s - (m1 + m2)**2)*(s - (m1 - m2)**2) < 0: return 0.0001
        numerator = math.sqrt((s - (m1 + m2)**2)*(s - (m1 - m2)**2))
        return numerator/denominator
    
    ### defined BW (PHSP factors are considered) 
    def getOneBreitWigner(self, xx, mass, width, eewidth, minMotherEnergy):
        """ minMotherEnergy = m1 + m2 + m3"""
        if mass < minMotherEnergy or xx < minMotherEnergy or width < 0.0 or eewidth < 0.0: 
            return complex(0.0, 0.0)
        
        right = math.sqrt(self._gr.Eval(xx)/self._gr.Eval(mass))
        numerator = math.sqrt(12.0*math.pi*width*eewidth)
        denominator = complex(xx*xx - mass*mass, mass*width)
        middle = numerator/denominator
        
        return middle*right
    
    ### defined correlated N BW (PHSP factors are included)
    def getCorrelatedBreitWigners(self, xx, resonances, minMotherEnergy):
        """ minMotherEnergy = m1 + m2 + m3 
                resonance: [mass, width, eewidth, phi] """
        bw = complex(0.0, 0.0)
        for resonance in resonances:
            mass, width, eewidth, phi = resonance
            bw = bw + self.getOneBreitWigner(xx, mass, width, eewidth, minMotherEnergy)*(complex(math.cos(phi), math.sin(phi)))
        return bw
