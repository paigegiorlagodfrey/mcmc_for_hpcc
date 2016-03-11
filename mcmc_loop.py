## START HERE FOR MCMC LOOP OVER LIST OF OBJECTS

from mcmc_fit import mcmc_fit as mc
import numpy as np 
import astropy.units as U
from matplotlib import pylab as plt
import modules as m
import cPickle

def run_loop(band):
	output = np.load('/Users/paigegiorla/Code/Python/BDNYC/t_dwarfs/model_fits/spex_objects.txt')
	'''output = [object,source,spectype,shortname]'''
	redchisq_results = np.load('/Users/paigegiorla/Code/Python/BDNYC/t_dwarfs/model_fits/Btsettl2013/model_fitting_bestfit_spectrum_{}'.format(band)+'.txt')
	'''redchisq_results = {'object_params':[spectype,shortname], 'object_spectrum':[object[0],object[1],object[2]], 'model_params':[model_binned[top1][1],model_binned[top1][2]], 'model_spectrum':[model_binned[top1][3],model_binned[top1][4]]}
	'''
 	L = cPickle.load(open('/Users/paigegiorla/Code/Python/BDNYC/mcmc_fit_results/mcmc_loop_dump','rb'))

	not_working, done = [], []
	
	for i,obj in enumerate(output):		
		[w,f,u] = m.wavelength_band(band, obj[0])
 		w = w*(U.um)
		f = f*(U.erg/U.AA/U.cm**2/U.s)
		u = u*(U.erg/U.AA/U.cm**2/U.s)
		
		mg = mc.make_model_db('bt_settl_2013','/Users/paigegiorla/Code/Python/BDNYC/model_atmospheres.db',param_lims=[('teff',redchisq_results[i]['model_params'][0]-300,redchisq_results[i]['model_params'][0]+300,50),('logg',3.0,5.5,0.5)])
		try: 
			fit = mc.fit_spectrum([w,f,u],mg,10,20)
			ax = plt.gca()
			ax = plt.savefig('/Users/paigegiorla/Code/Python/BDNYC/mcmc_fit_results/triangle_plots/{}_{}'.format(obj[2],obj[1])+'.eps')
			done.append(obj[1])
			fit_data = fit.get_error_and_unc()
			L = {'object_params':[obj[1],obj[2],obj[3]],'fit_data_and_unc':fit_data}
 			cPickle.dump(L, open('/Users/paigegiorla/Code/Python/BDNYC/mcmc_fit_results/mcmc_loop_dump','wb'))
			print i

		except: 
			not_working.append(obj[1])	
	
	return not_working, done
	
	
	
	

