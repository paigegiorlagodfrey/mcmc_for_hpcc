import pickle
import astropy.units as q		       				
import numpy as np
import wxversion
wxversion.select('2.8')
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt 
from pylab import *
import mcmc_fit as mc
import sys

## pull object from Tdwarf Sample file 								<---- NEEDS TO BE PUT ON HPCC
def get_spectrum(shortname):
	file=np.load('/synth_fit/spex_objects_J.txt')
	i = list(file[:,3]).index(shortname)
	wavelength = file[i][0][0]
	flux = file[i][0][1]
	unc = file[i][0][2]
	return [wavelength,flux,unc]

	
def fit_models(shortname, model_grid_name, model_grid_path, nwalkers, nsteps, param_lims=[('teff',400,1600,50),('logg',3.5,5.5,0.5)], fill_holes=False):
	wavelength,flux,unc = get_spectrum(shortname)
	##add quantities to object
	w = wavelength * q.um
	f = flux * q.erg/q.AA/q.cm**2/q.s
	u = unc * q.erg/q.AA/q.cm**2/q.s
		
  ## get models                                                           
	fb = open(model_grid_path,'rb')
  model_grid = pickle.load(fb)
	fb.close()
		
	## run mc.fit_spectrum and save result to file 				<---- NEEDS TO BE PUT ON HPCC
	bdsamp = mc.fit_spectrum([w,f,u], model_grid, model_grid_name, shortname, nwalkers, nsteps, object_name='{}'.format(shortname), log=False, plot=True, prnt=True, outfile=None)
 	## [array([w]),array([f])] of interp'd best fit model 
	best_fit_spectrum = bdsamp.best_fit_spectrum
	## array([[low,param,high],[]])
	params_with_unc = bdsamp.get_error_and_unc()
	fb = open('/synth_fit_results/{}_{}'.format(model_grid_name,shortname)+'_bdsamp.txt','wb')
	pickle.dump([bdsamp.all_params,bdsamp.all_quantiles.T[1],best_fit_spectrum,params_with_unc],fb)
	fb.close()
	print [bdsamp.all_params,bdsamp.all_quantiles.T[1],best_fit_spectrum,params_with_unc]
	figure(1)
	fig1 = plt.gcf()
	fig1.savefig('/synth_fit_results/{}_{}'.format(model_grid_name,shortname)+'_triangle.eps')
	fig1 = plt.clf()
	figure(2)
	fig2 = plt.gcf()
	fig2.savefig('/synth_fit_results/{}_{}'.format(model_grid_name,shortname)+'_chains.eps')
	fig2 = plt.clf()
if __name__=="__main__":
 	fit_models(shortname, model_grid_name, model_grid_path, nwalkers, nsteps, param_lims=[('teff',400,1600,50),('logg',3.5,5.5,0.5)], fill_holes=False)
 	shortname = '0722-0540'
 	model_grid_name = 'bt_settl_2013'
 	model_grid_path = './synth_fit/BTSettl_mcmc.pkl'
 	nwalkers = 1000
 	nsteps = 1000