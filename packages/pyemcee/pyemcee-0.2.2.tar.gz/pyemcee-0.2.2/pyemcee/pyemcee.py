# -*- coding: utf-8 -*-

"""
This module contains functions for  the affine-invariant Markov 
chain Monte Carlo (MCMC) ensemble sampler proposed by 
Goodman & Weare (2010).
"""

# A. Danehkar
#
# Version 0.2.0, 07/09/2020
# First Release
#

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

__all__ = ["hammer","find_errors"]

def initialize(fcn, param, param_err_m, param_err_p, walk_num, output_num, use_gaussian, functargs=None):
   """
        This function returne the initialized walkers for each free parameter.

       For example::
   
        >> x_walk=initialize(fcn, input, input_err, walk_num, 
        >>                   output_num, use_gaussian))
   

    :return: This function returns the initialized walker.
    :rtype: arrays

    :param functargs: the function arguments (not used for MCMC).
    :type functargs: parameter, optional
        
    :param fcn: the calling function name.
    :type fcn: str               
   
    :param param: the input parameters array used by the calling function.
    :type param: arrays   
    
    :param param_err_m: the lower limit uncertainty array of the parameters for the calling function.
    :type param_err_m: arrays   

    :param param_err_p: the upper limit uncertainty array of the parameters for the calling function.
    :type param_err_p: arrays   
    
    :param walk_num: the number of the random walkers.
    :type walk_num: int   
    
    :param output_num: the number of the output array returned by the calling function.
    :type output_num: int 

    :param use_gaussian: if sets to 1, the walkers are initialized as a gaussian over the specified range between the min and max values of each free parameter, otherwise, the walkers are initialized uniformly over the specified range between the min and max values of each free parameter.              
    :type use_gaussian: boolean 
   
   """
   
#    History:
#        15/03/2017, A. Danehkar, IDL code written
#                    Adopted from emcee() of sl_emcee
#                    by M.A. Nowak included in isisscripts  
#        01/05/2020, A. Danehkar, function arguments added
#        05/09/2020, A. Danehkar, Transferred from IDL to Python


   #fcnargs = functargs
   
   param_num = len(param)
   x_point = np.zeros(param_num)
   x_low = np.zeros(param_num)
   x_high = np.zeros(param_num)
   x_start = np.zeros((param_num, walk_num * param_num))
   x_out = np.zeros((walk_num * param_num, output_num))
   for i in range(0,param_num):
      x_point[i] = param[i]
      x_low[i] = param[i] + param_err_m[i]
      x_high[i] = param[i] + param_err_p[i]
      #x_low[i]   = param[i]-param_err[i]
      #x_high[i]  = param[i]+param_err[i]
   if use_gaussian == 1:   
      scale1 = 1. / 3.
   else:   
      scale1 = 1.
   for j in range(0,walk_num * param_num ):
      for i in range(0, param_num):
         if use_gaussian == 1:   
            sigma1 = np.random.uniform() #randomn(seed)
            if sigma1 < 0:   
               x_start[i,j] = x_point[i] + sigma1 * scale1 * (x_point[i] - x_low[i])
            else:   
               x_start[i,j] = x_point[i] + sigma1 * scale1 * (x_high[i] - x_point[i])
         else:   
            sigma1 = np.random.uniform() #randomu(seed)
            x_start[i,j] = (1 - scale1) * x_point[i] + scale1 * (x_low[i] + (x_high[i] - x_low[i]) * sigma1)
         if x_start[i,j] < x_low[i]:
            x_start[i,j] = x_low[i]#
         if x_start[i,j] > x_high[i]:
            x_start[i,j] = x_high[i]#
      #x_out[j,:] = call_function(fcn, x_start[:,j])
   return x_start

def inv_tot_dist(z, z_a, z_b):
   """
        This function returne the inverse Cumulative Distribution Function: 1/sqrt(z)
        if the random number generator z is between 1/z_a and z_b, is used
        to generate for a 1/sqrt(z) probability distribution.

       For example::
   
        >> z = inv_tot_dist(random_num, adjust_scale_low, adjust_scale_high);
        
    :return: This function returns the lower and higher linear histogram grids (hist_lo, hist_hi).
    :rtype: arrays       
   
    :param z: the a random number generator for the probability distribution 1/sqrt(z).
    :type z: float
    
    :param z_a: the inverse lower limit for the random number generator z: 1/z_a <= z.
    :type z_a: float
                   
    :param z_b: the higher limit for the random number generator z: z <= b.
    :type z_b: float
   
   """
   
#    History:
#        15/03/2017, A. Danehkar, IDL code written
#                    Adopted from icdf() of sl_emcee
#                    by M.A. Nowak included in isisscripts
#        05/09/2020, A. Danehkar, Transferred from IDL to Python

   x1 = 1. / (np.sqrt(z_a * z_b) - 1.)
   x2 = 1. / x1 ** 2. / z_a
   return x2 * (z + x1) ** 2

def linear_grid(x_min, x_max, nbins):
   """
        This procedure generates a linear grid of histogram bins.

       For example::
   
        >> x_min=1
        >> x_max=20
        >> nbins=1000
        >> lo, hi = linear_grid(x_min, x_max, nbins)
        
    :param x_min: the lower limit.
    :type x_min: float
    
    :param x_max: the higher limit.
    :type x_max: float
    
    :param nbins: the bins number.
    :type nbins: float
    
    :param hist_lo: returns the lower linear histogram grid.
    :type hist_lo: arrays
    
    :param hist_hi: returns the higher linear histogram grid.
    :type hist_hi: arrays

   """
   
#    History:
#        15/03/2017, A. Danehkar, IDL code written
#                    Adopted from the S-Lang function linear_grid() in isis
#        05/09/2020, A. Danehkar, Transferred from IDL to Python

   step = (float(x_max) - float(x_min)) /float(nbins)
   hist_lo = np.arange(int(nbins)) * step + x_min
   hist_hi = np.arange(int(nbins) + 1.) * step + x_min
   
   return (hist_lo, hist_hi)


# Call user function or procedure, with _EXTRA or not, with
# derivatives or not.
#def call_function(fcn, x_chosen, functkw, fjac=None):
def call_function(fcn, x_chosen, functargs=None):
   if functargs is None:
      output= fcn(x_chosen)
   else:
      output = fcn(x_chosen, functargs=functargs)
   return output


def update_walk(fcn, random_num, x_a, x_b, functargs=None):
   """
        This function creates the trial walker, examines
        whether it is acceptable, and returns the updated walker.
   
       For example::
   
        >> x_output[j,:]=update_walk(fcn,a_random[random_num[j],:],
        >>                           array_xwalk,x_walk[:,b_walk])
        
    :return: This function returns the updated walker.
    :rtype: arrays
   
    :param functargs: the function arguments.
    :type functargs: parameter, optional
    
    :param fcn: the calling function name.
    :type fcn: str
    
    :param random_num: the random number.
    :type random_num: int

    :param x_a: the vector of the parameters for a specific walker.
    :type x_a: arrays
                      
    :param x_b: the array of the walker parameters.
    :type x_b: arrays                    
   
   """
   
#    History:
#        15/03/2017, A. Danehkar, IDL code written
#                    Adopted from update_walker() of sl_emcee
#                    by M.A. Nowak included in isisscripts 
#        01/05/2020, A. Danehkar, function arguments added
#        05/09/2020, A. Danehkar, Transferred from IDL to Python

   fcnargs = functargs
   
   adjust_scale_low = 2.0
   adjust_scale_high = 2.0
   par_num = len(x_b)
   b_num = len(x_b[0])
   x_chosen = x_b[:,int(random_num[0] * b_num)]
   # print, long(random_num[0]*b_num)
   z = inv_tot_dist(random_num[1], adjust_scale_low, adjust_scale_high)
   x_chosen = x_chosen + z * (x_a - x_chosen)
   if (fcnargs is not None):   
      x_output = call_function(fcn, x_chosen, functargs=fcnargs)
   else:   
      x_output = call_function(fcn, x_chosen)
   return x_output


def hammer(fcn, input, input_err_m, input_err_p, output, walk_num, iteration_num, use_gaussian, functargs=None):
   """
        This function runs the affine-invariant MCMC Hammer,
        and returns the MCMC simulations

       For example::
   
        >> mcmc_sim=pyemcee.hammer(myfunc, input, input_err, output, 
        >>                         walk_num, iteration_num, use_gaussian)
           
    :return: This function returns the results of the MCMC simulations.
    :rtype: arrays

    :param functargs: the function arguments (not used for MCMC).
    :type functargs: parameter, optional
        
    :param fcn: the calling function name.
    :type fcn: str               
   
    :param input: the input parameters array used by the calling function.
    :type input: float   
    
    :param input_err_m: the lower limit uncertainty array of the parameters for the calling function.
    :type input_err_m: float   

    :param input_err_p: the upper limit uncertainty array of the parameters for the calling function.
    :type input_err_p: float   

    :param output: the output array returned by the calling function.
    :type output: arrays   
    
    :param walk_num: the number of the random walkers.
    :type walk_num: int   
    
    :param iteration_num: the number of the MCMC iteration.
    :type iteration_num: int 

    :param use_gaussian: if sets to 1, the walkers are initialized as a gaussian over the specified range between the min and max values of each free parameter, otherwise, the walkers are initialized uniformly over the specified range between the min and max values of each free parameter.              
    :type use_gaussian: boolean 

   """
   
#    History:
#        15/03/2017, A. Danehkar, IDL code written
#                    Adopted from emcee() of sl_emcee
#                    by M.A. Nowak included in isisscripts
#        01/05/2020, A. Danehkar, function arguments added
#        05/09/2020, A. Danehkar, Transferred from IDL to Python

   fcnargs = functargs
   
   output_num = len(output)
   x_walk = initialize(fcn, input, input_err_m, input_err_p,
                             walk_num, output_num, use_gaussian,
                             functargs=fcnargs)
   input_num = len(input)
   
   total_walk_num = walk_num * input_num
   a_walk = np.arange(int(total_walk_num / 2 + (total_walk_num % 2))) * 2
   b_walk = np.arange(int(total_walk_num / 2)) * 2 + 1
   
   a_num = len(a_walk)
   b_num = len(b_walk)
   
   array_xwalk = np.zeros(input_num)
   x_output = np.zeros((max([a_num, b_num]), output_num))
   
   a_random = np.zeros((iteration_num * a_num, 3))
   b_random = np.zeros((iteration_num * b_num, 3))
   for i in range(0, iteration_num * a_num):
      a_random[i,0] = np.random.uniform()#randomu(seed)
      a_random[i,1] = np.random.uniform()
      a_random[i,2] = np.random.uniform()
   for i in range(0, iteration_num * b_num):
      b_random[i,0] = np.random.uniform()
      b_random[i,1] = np.random.uniform()
      b_random[i,2] = np.random.uniform()
   x_out = np.zeros((a_num + b_num, output_num))
   mcmc_sim = np.zeros((iteration_num, a_num + b_num, output_num))
   #sim1=np.zeros(iteration_num,a_num+b_num)
   for i in range(0, iteration_num):
   # first half of walkers
      random_num = i * a_num + np.arange(a_num)
      for j in range(0, a_num):
         array_xwalk = x_walk[:,a_walk[j]]
         x_output[j,:] = update_walk(fcn, a_random[random_num[j],:],
                                           array_xwalk, x_walk[:,b_walk],
                                           functargs=fcnargs)
      for j in range(0, a_num ):
         x_out[a_walk[j],:] = x_output[j,:]#
      # second half of walkers
      random_num = i * b_num + np.arange(b_num)
      for j in range(0, b_num):
         array_xwalk = x_walk[:,b_walk[j]]
         x_output[j,:] = update_walk(fcn, b_random[random_num[j],:],
                                           array_xwalk, x_walk[:,a_walk],
                                           functargs=fcnargs)
      for j in range(0, b_num):
         x_out[b_walk[j],:] = x_output[j,:]#
      for j in range(0, output_num):
         mcmc_sim[i,:,j] = x_out[:,j]
      print('Sim loop:', i)
   return mcmc_sim


def find_errors(output, mcmc_sim, clevel, do_plot=None, image_output_path=None):
   """
        This function returns the uncertainties of the function outputs
        based on the confidence level.

       For example::

        >> output_error=pyemcee.find_erros(output, mcmc_sim, clevel)
        
    :return: This function returns uncertainties.
    :rtype: arrays

    :param do_plot: set to plot a normalized histogram of the MCMC chain.
    :type do_plot: boolean  
    
    :param image_output_path: the image output path.
    :type image_output_path: str                                

    :param output: the output array returned by the calling function.
    :type output: arrays  

    :param mcmc_sim: the results of the MCMC simulations from hammer().
    :type mcmc_sim: arrays  

    :param clevel: the confidence level for the the lower and upper limits. clevel=0.38292492 (0.5-sigma); clevel=0.68268949 (1.0-sigma); clevel=0.86638560 (1.5-sigma); clevel=0.90 (1.645-sigma); clevel=0.95 (1.960-sigma); clevel=0.95449974 (2.0-sigma); clevel=0.98758067 (2.5-sigma); clevel=0.99 (2.575-sigma); clevel=0.99730020 (3.0-sigma); clevel=0.99953474 (3.5-sigma); clevel=0.99993666 (4.0-sigma); clevel=0.99999320 (4.5-sigma); clevel=0.99999943 (5.0-sigma); clevel=0.99999996 (5.5-sigma); clevel=0.999999998(6.0-sigma).
    :type clevel: float  
                    
   """
   
#    History:
#        15/03/2017, A. Danehkar, IDL code written
#                    Adopted from chain_hist() of sl_emcee
#                    by M.A. Nowak included in isisscripts
#        05/09/2020, A. Danehkar, Transferred from IDL to Python

   nbins = 50.
   output_num = len(output)
   output_error = np.zeros((output_num, 2))
#   if finite(output, infinity=True):
#      return output_error
#   if finite(output, nan=True):
#      return output_error
   for j in range(0, output_num):
      if (np.isnan(output[j]) | np.isinf(output[j])):
         output_error[j, 0] = 0
         output_error[j, 1] = 0
      else:
         sim1 = mcmc_sim[:, :,j]
         sim1_min = np.amin(sim1.ravel())
         sim1_max = np.amax(sim1.ravel())
         x_min = sim1_min
         x_max = sim1_max
         if x_min != x_max:
            lo, hi=linear_grid(x_min, x_max, nbins)
            lo_fine, hi_fine=linear_grid(sim1_min, sim1_max, 4. * nbins)
            hist, bin_edges = np.histogram(sim1.ravel(), density=True, bins=lo)
                              #binsize=lo[1] - lo[0])  # BINSIZE = float(bin), locations=xbin,)
            hist_fine, bin_edges_fine = np.histogram(sim1.ravel(), density=True, bins=lo_fine)
                              #binsize=lo_fine[1] - lo_fine[0])  # BINSIZE = float(bin), locations=xbin)
            bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
            pdf_n  = stats.norm.pdf(bin_centers)
            bin_centers_fine = 0.5 * (bin_edges_fine[1:] + bin_edges_fine[:-1])
            pdf_n_fine = stats.norm.pdf(bin_centers_fine)
            cdf_n = np.cumsum(hist * np.diff(bin_edges))
            #cdf_n = np.cumsum(pdf_n) / len(sim1) #nelements()
            cdf_n_fine = np.cumsum(hist_fine * np.diff(bin_edges_fine))
            #cdf_n_fine = np.cumsum(pdf_n_fine) / len(sim1) #nelements()

            result = output[j]

            clevel_start = min(np.where((cdf_n >= (1. - clevel) / 2.))[0])
            clevel_end = min(np.where((cdf_n > (1. + clevel) / 2.))[0])
            if clevel_start == 50:
               clevel_start = clevel_start - 1
            if clevel_end == 50:
               clevel_end = clevel_end - 1
            sim1_lo = lo[clevel_start]
            sim1_hi = hi[clevel_end]
            # print, result, sim1_lo-result, sim1_hi-result
            # plothist, sim1, bin=lo[1]-lo[0]

            clevel_start = np.amin(np.where((cdf_n_fine >= (1. - clevel) / 2.))[0])
            clevel_end = np.amin(np.where((cdf_n_fine > (1. + clevel) / 2.))[0])
            if clevel_start == 200:
               clevel_start = clevel_start - 1
            if clevel_end == 200:
               clevel_end = clevel_end - 1
            sim1_lo = lo_fine[clevel_start]
            sim1_hi = hi_fine[clevel_end]
            bin_fine = lo_fine[1] - lo_fine[0]
            # temp=size(pdf_n_fine,/DIMENSIONS)
            # ntot=double(temp[0])
            output_error[j, 0] = sim1_lo - result
            output_error[j, 1] = sim1_hi - result
            # print, result, sim1_lo-result, sim1_hi-result
            # pdf_normalize=pdf_n_fine/bin_fine/ntot
            # plot,lo_fine,pdf_normalize/max(pdf_normalize)
            if (do_plot is not None):
               fig = plt.figure(figsize=(6, 6))
               plt.hist(sim1.ravel(), bins=lo_fine, density=True, facecolor='b', alpha=0.75)
               plt.show()
               if (image_output_path is not None) == 1:
                  filename = image_output_path + '/histogram' + str(j) + '.png'
                  fig = plt.figure(figsize=(6, 6))
                  plt.hist(sim1.ravel(), bins=lo_fine, density=True, facecolor='b', alpha=0.75)
                  fig.savefig(filename)
         else:
            output_error[j, 0] = 0
            output_error[j, 1] = 0
   return output_error

