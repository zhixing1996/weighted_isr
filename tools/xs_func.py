#/usr/bin/env python
#-*- Coding: UTF-8 -*-

__author__ = "Lianjin WU <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import ROOT as root
import math

class xs_func():
	def __init__(self, nbin, lower, upper, mass0 = 0.54786, mass1 = 0.54786, mass2 = 3.0969):
		""" bin, lower, upper limits for PHSP factor, three particle masses  """
		self._gr = root.TGraph()
		for ibin in range(nbin):
			m0 = lower + ibin*(upper - lower)/float(nbin)
			self._gr.SetPoint(ibin, lower + ibin*(upper - lower)/float(nbin), self.__getPHSPFactor(m0, mass0, mass1, mass2))

	### three body PHSP function for TF1
	def __integralPHSPFunc(self, x, par):
		xx = x[0]
		e2star = (xx-par[1]*par[1]+par[2]*par[2])/(2*math.sqrt(xx))
		e3star = (par[0]*par[0]-xx-par[3]*par[3])/(2*math.sqrt(xx))
		func1 = math.sqrt(e2star*e2star-par[2]*par[2])
		func2 = math.sqrt(e3star*e3star-par[3]*par[3])
		fmax = -(func1-func2)*(func1-func2)
		fmin = -(func1+func2)*(func1+func2)
		func = fmax-fmin
		return func

	### three body PHSP factor calculation based on TF1
	### m0 -> m1 + m2 + m3
	def __getPHSPFactor(self, m0, m1, m2, m3):
		xmin = (m1+m2)*(m1+m2)
		xmax = (m0-m3)*(m0-m3);
		locals()["f1%s"%(str(m0).replace(".", ""))] = root.TF1("f1%s"%(str(m0).replace(".", "")), self.__integralPHSPFunc, xmin, xmax, 4)
		locals()["f1%s"%(str(m0).replace(".", ""))].SetParameters(m0, m1, m2, m3)
		return locals()["f1%s"%(str(m0).replace(".", ""))].Integral(xmin, xmax)

	### PHSP facor Graph
	def getPHSPFactorGraph(self):
		return self._gr

	### PHSP factor
	def getPHSPFactor(self, energy):
		return self._gr.Eval(energy)

	### defined BW (PHSP factors are considered) 
	def getOneBreitWigner(self, xx, mass, width, eewidth, minMotherEnergy):
		""" minMotherEnergy = m1 + m2 + m3"""
		if mass < minMotherEnergy or xx < minMotherEnergy or width < 0.0 or eewidth < 0.0: 
			return complex(0.0, 0.0)

		left = mass / xx
		right = math.sqrt(self._gr.Eval(xx) / self._gr.Eval(mass))
		numerator = math.sqrt(12.0*math.pi*width*eewidth)
		denominator = complex(xx*xx-mass*mass, mass*width)
		middle = numerator/denominator

		return left*middle*right

	### defined correlated N BW (PHSP factors are included)
	def getCorrelatedBreitWigners(self, xx, resonances, minMotherEnergy):
		""" minMotherEnergy = m1 + m2 + m3 
				resonance: [mass, width, eewidth, phi] """
		bw = complex(0.0, 0.0)
		for resonance in resonances:
			mass, width, eewidth, phi = resonance
			bw = bw + self.getOneBreitWigner(xx, mass, width, eewidth, minMotherEnergy)*(complex(math.cos(phi), math.sin(phi)))
		return bw

	### defined exp(i*phi) = cos(phi) + i*sin(phi)
	def getExpIPhi(self, phi):
		""" exp(i*phi) = cos(phi) + i*sin(phi) """
		return complex(math.cos(phi), math.sin(phi))
