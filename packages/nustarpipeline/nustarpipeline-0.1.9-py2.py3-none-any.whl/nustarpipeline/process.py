#!/usr/bin/env python
#

import sys
import os
from time import gmtime, strftime
import glob

import argparse

import logging
from subprocess import Popen, PIPE, STDOUT

file_handler = logging.FileHandler(filename='nustar_utils_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler, file_handler]

logging.basicConfig(level=logging.INFO, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}
logger = logging.getLogger()

def log_subprocess_output(pipe):
	for line in iter(pipe.readline, b''): # b'\n'-separated lines
		logging.info(line.decode()[0:-1])

def get_latest_file(path, *paths):
	'''
	Returns the name of the latest (most recent) file
	of the joined path(s)
	'''
	fullpath = os.path.join(path, *paths)
	files = glob.glob(fullpath)  # You may use iglob in Python3
	if not files:                # I prefer using the negation
		return None                      # because it behaves like a shortcut
	latest_file = max(files, key=os.path.getctime)
	_, filename = os.path.split(latest_file)
	return filename

def get_channel(e):
	'''
	gets the PI channel from energy scale
	http://heasarc.gsfc.nasa.gov/docs/nustar/nustar_faq.html#pi_to_energy
	'''

	return int((e-1.6)/0.04)

def prepare_outdir(outdir):

	'''
	:param outdir:
	:return:
	Creates outdir and pfiles directory
	sets pfiles in there
	'''

	if (not os.path.isdir(outdir)):
		os.makedirs(outdir)

	if (not os.path.isdir(os.path.join(outdir, "pfiles"))):
		os.makedirs(os.path.join(outdir, "pfiles"))

	old_pfiles=os.environ["PFILES"]
	tmp=old_pfiles.split(";")
	sys_pfiles=tmp[-1]

	os.environ["PFILES"]=os.path.join(os.getcwd(),os.path.join(outdir, "pfiles"))+";"+sys_pfiles
	logger.info("PFILES = "+os.environ["PFILES"])
	return
	# time_stamp=strftime("%Y-%m-%dT%H:%M:%S", gmtime())
	# return outdir+"/logfile_"+time_stamp+".txt"

def run(command):
	#source $CALDB/software/tools/caldbinit.sh;
	true_command = 'export HEADASNOQUERY="";export HEADASPROMPT=/dev/nul;' + \
		command
	logger.info("------------------------------------------------------------------------------------------------\n")
	logger.info("**** running %s ****\n" % command)
	#out=subprocess.call(cmd, stdout=logger, stderr=logger, shell=True)
	process = Popen(true_command, stdout=PIPE, stderr=STDOUT, shell=True)
	with process.stdout:
		log_subprocess_output(process.stdout)
	ret_value = process.wait()  # 0 means success
	logger.info("------------------------------------------------------------------------------------------------\n")
	logger.info("Command '%s' finished with exit value %d" % (command, ret_value))
	return ret_value

def get_data(obsid):
	cmd="wget -q -nH --no-check-certificate --cut-dirs=6 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/nustar/data/obs/"+obsid[1:3]+"/"+obsid[0]+"/"+obsid+"/"
	return run(cmd)

def write_region(fname, ra, dec, src_flag, ra_back=-1, dec_back=-1, radius=120):
	ff = open(fname, 'w')
	ff.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nfk5\n")
	if src_flag:
		ff.write("circle(%.4f,%.4f,%.0f\")" % (ra, dec, radius))
	else:
		#The default is just a guess
		if ra_back == -1:
			ra_deg = float(ra)-0.14
		else:
			ra_deg = float(ra_back)
		if dec_back == -1:
			dec_deg = float(dec)-0.08
		else:
			dec_deg = float(dec_back)

		ff.write("circle(%.4f,%.4f,%.4f\")" % (ra_deg, dec_deg, float(radius)))
	ff.close()


def get_src_from_obsid(obsid, repository_path=os.environ['HOME'] + '/NUSTAR/Repository'):
	from astropy.io import fits as pf
	search_str = repository_path + '/' + obsid + '/event_cl/nu*A*_cl.evt.gz'
	logger.debug(search_str)
	eventsA = glob(search_str)
	if len(eventsA) == 0:
		logger.warning('no event data for ' + obsid + '? Reurning none')
		return None
	with pf.open(eventsA[0]) as ff:
		src = ff[1].header['OBJECT']
	logger.debug('Found source ' + src)
	return src

def wrap_process(obsid, ra_src, dec_src, outdir_base, pipeline_flag=False, region_flag=False,
				 spec_flag=False, lc_flag=False,
				 no_ds9_flag=False, ra_back=-1, dec_back=-1, radius=120, write_baryevtfile_flag=False,
				 filter_evt_flag=False, user_gti_file='none',
				 repository_location=os.environ['HOME'] + '/NUSTAR/Repository', t_bin=100., e_min=3., e_max=30.,
				 J_A=None, J_B=None):
	'''

	:param obsid: the observation ID
	:param ra_src: RA of the source
	:param dec_src: Dec of the source
	:param outdir_base: the basename for products
	:param pipeline_flag: it tuns the pipeline
	:param region_flag: it writes region (if not existent) and allows the user to check them
	:param spec_flag: it extracts spectra
	:param lc_flag: extracts light crves (set also t_bin e_min and e_max
	:param no_ds9_flag: this is relevant just if region_flag is true, if set to True, it will use JS9, with the diplays
						for FPMA and FPMB provided by the caller
	:param ra_back: optional RA of the center of background region (otherise offset from the source)
	:param dec_back: optional Dec of the center of background region (otherise offset from the source)
	:param radius: the radius for source regions )defaults to 120
	:param write_baryevtfile_flag: to be used with lightcurve to extract barycentric corrected event files
	:param filter_evt_flag: This is to be used when lightcurves are extracted to extract barycentric corrected
							event files for the source and backgroud for FPMA and FPMB
	:param user_gti_file: if this is provided
	:param repository_location: the location of the repository of raw data
	:param t_bin: time bin for light curves
	:param e_min: Minimum energy for lightcurve
	:param e_max: Maximium energy for lightcurve
	:param J_A:  handler for the JS9 display for FPMA
	:param J_B:  handler for the JS9 display for FPMA
	:return: zero
	'''
	if (not os.path.isdir(repository_location + "/" + obsid)):
		logger.error("The obsid you specified (" + obsid + ") does not exist in the repository " + repository_location)
		return 1

	logger.info("Processing OBSID %s for RA=%f Dec=%f with outdir base %s" % (obsid, ra_src, dec_src, outdir_base))
	logger.info("Pipeline flag %r" % (pipeline_flag))
	logger.info("Spectrum flag %r" % (spec_flag))
	logger.info("Lightcurve flag %r" % (lc_flag))

	outdir_pipeline = outdir_base + "_pipeline"
	logger.info("The output of standard pipelines are in " + outdir_pipeline)

	if pipeline_flag:

		# logfile_name =
		prepare_outdir(outdir_pipeline)
		# logfile = open(logfile_name, 'w')
		#print("writing output to log file: %s" % logfile_name)

		cmd = "nupipeline indir=" + repository_location + "/" + obsid + " steminputs=nu" + obsid + " obsmode=Science outdir=" + outdir_pipeline

		return run(cmd)
		# logfile.close()

	if region_flag:
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before spectral extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_spec"
		outdir_pipeline = outdir_base + "_pipeline"
		prepare_outdir(outdir)

		logger.info("We store regions in the spectral extraction folder '%s'" % outdir)

		src_regionA = outdir + "/sourceA.reg"
		if (not os.path.isfile(src_regionA)):
			write_region(src_regionA, ra_src, dec_src, True)
		src_regionB = outdir + "/sourceB.reg"
		if (not os.path.isfile(src_regionB)):
			write_region(src_regionB, ra_src, dec_src, True)
		bkg_regionA = outdir + "/backgroundA.reg"
		if (not os.path.isfile(bkg_regionA)):
			write_region(bkg_regionA, ra_src, dec_src, False, ra_back=ra_back, dec_back=dec_back, radius=radius)
		bkg_regionB = outdir + "/backgroundB.reg"
		if (not os.path.isfile(bkg_regionB)):
			write_region(bkg_regionB, ra_src, dec_src, False, ra_back=ra_back, dec_back=dec_back, radius=radius)


		if no_ds9_flag==False:
			logger.info("Please check the regions for FPMA")
			cmd = "ds9 -scale log " + outdir_pipeline + "/nu" + obsid + "A01_cl.evt -regions " + src_regionA + " -regions " + bkg_regionA
			run(cmd)
			logger.info("Please check the regions for FPMB")
			cmd = "ds9 -scale log " + outdir_pipeline + "/nu" + obsid + "B01_cl.evt -regions " + src_regionB + " -regions " + bkg_regionB
			run(cmd)

			#logger.info("Have you checked properly the region files?(y/Y will continue the processing any other key stop it)")
			logger.warning("We ask to rerun the analysis disabling the ds9 iteractive command with which you have checked the region files")
			# ans = input("Please enter the key: ...")
			# if (not (ans == 'y')) and (not (ans == 'Y')):
			# 	print("Exit processing")
			return 0
		else:
			# JS9 does not load event files, I need to create an image first

			xsel_cmd = '''dummy
			read eve
			./ 
			nu%s%s01_cl.evt 
			yes 
			extra ima
			save ima ima%s.fits




			quit





			'''
			os.chdir(outdir_pipeline)
			for unit in ['A', 'B']:
				with open('xsel_%s.txt' % unit, 'w') as ff:
					ff.write(xsel_cmd % (obsid, unit, unit))
				cmd = 'xselect < ' + 'xsel_%s.txt' % (unit)
				run(cmd)
			os.chdir('..')

			logger.warning("Please check the regions for FPMA")

			if J_A is None or J_B is None:
				raise RuntimeError('We need a JS9 display for FPMA and FPMB to check regions and events, leave ds9_flag=False to use ds9')
			J_A.Load(outdir_pipeline + "/imaA.fits")
			J_A.LoadRegions(src_regionA)
			J_A.LoadRegions(bkg_regionA)
			J_A.send({'cmd': 'SetScale', 'args': ['log']})
			J_A.SetColormap('red')

			logger.warning("Please check the regions for FPMB")

			J_B.Load(outdir_pipeline + "/imaB.fits")
			J_B.LoadRegions(src_regionB)
			J_B.LoadRegions(bkg_regionB)
			J_B.send({'cmd': 'SetScale', 'args': ['log']})
			J_B.SetColormap('red')
			return 0

	if lc_flag:

		import shutil
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before light curve extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_lc"
		# logfile_name = \
		prepare_outdir(outdir)
		# logfile = open(logfile_name, 'w')
		# logger.info("writing output to log file: %s" % logfile_name)

		##searh clock file
		latest_clock = get_latest_file(repository_location + "/clock/*")

		ch_min = get_channel(e_min)
		ch_max = get_channel(e_max)
		logger.info("Energy scale E = Channel Number * 0.04 keV + 1.6 keV\n")
		logger.info("E_min=%f E_max=%f t_bin=%f ch_min=%d ch_max=%d\n" % (e_min, e_max, t_bin, ch_min, ch_max))


		if ((not os.path.isfile(outdir_base + "_spec/sourceA.reg")) or \
				(not os.path.isfile(outdir_base + "_spec/sourceB.reg")) or \
				(not os.path.isfile(outdir_base + "_spec/backgroundA.reg")) or \
				(not os.path.isfile(outdir_base + "_spec/backgroundB.reg")) ):
			raise RuntimeError('You need to have region files in %s_spec make them with the option region_flag' % outdir_base)

		src_region = outdir + "/sourceA.reg"
		if (not os.path.isfile(src_region)):
			spec_src = outdir_base + "_spec/sourceA.reg"
			shutil.copy(spec_src, src_region)

		bkg_region = outdir + "/backgroundA.reg"
		if (not os.path.isfile(bkg_region)):
			spec_bkg = outdir_base + "_spec/backgroundA.reg"
			shutil.copy(spec_bkg, bkg_region)

		cmd = "nuproducts indir=" + outdir_pipeline + " instrument=FPMA steminputs=nu" + obsid + " stemout=FPMA_%.1f_%.1f outdir=" % (
		e_min, e_max) + outdir
		cmd += " srcregionfile=" + src_region + " bkgextract=yes runbackscale=no binsize=%f pilow=%d pihigh=%d barycorr=yes" % (
		t_bin, ch_min, ch_max)
		cmd += " orbitfile=" + repository_location + "/" + obsid + "/auxil/nu" + obsid + "_orb.fits.gz cleanup=no srcra_barycorr=%f" % (
			ra_src)
		cmd += " srcdec_barycorr=%f" % (
			dec_src) + " bkglcfile=DEFAULT bkgregionfile=" + bkg_region + " runmkarf=no runmkrmf=no phafile=NONE imagefile=NONE"
		if write_baryevtfile_flag:
			cmd += " write_baryevtfile=yes"

		# print("My latest clock is " + latest_clock)
		if latest_clock != None:
			cmd += " clockfile=\"" + repository_location + "/clock/" + latest_clock + "\""

		if user_gti_file != 'none':
			cmd += " usrgtifile=" + user_gti_file + " usrgtibarycorr=yes"

		run(cmd)

		src_region = outdir + "/sourceB.reg"
		if (not os.path.isfile(src_region)):
			spec_src = outdir_base + "_spec/sourceB.reg"
			shutil.copy(spec_src, src_region)

		bkg_region = outdir + "/backgroundB.reg"
		if (not os.path.isfile(bkg_region)):
			spec_bkg = outdir_base + "_spec/backgroundB.reg"
			shutil.copy(spec_bkg, bkg_region)

		cmd = "nuproducts indir=" + outdir_pipeline + " instrument=FPMB steminputs=nu" + obsid + " stemout=FPMB_%.1f_%.1f outdir=" % (
		e_min, e_max) + outdir
		cmd += " srcregionfile=" + src_region + " bkgextract=yes runbackscale=no binsize=%f pilow=%d pihigh=%d barycorr=yes" % (
		t_bin, ch_min, ch_max)
		cmd += " orbitfile=" + repository_location + "/" + obsid + "/auxil/nu" + obsid + "_orb.fits.gz cleanup=no srcra_barycorr=%f" % (
			ra_src)
		cmd += " srcdec_barycorr=%f" % (
			dec_src) + " bkglcfile=DEFAULT bkgregionfile=" + bkg_region + " runmkarf=no runmkrmf=no phafile=NONE imagefile=NONE"
		if write_baryevtfile_flag:
			cmd += " write_baryevtfile=yes"

		if latest_clock != None:
			cmd += " clockfile=\"" + repository_location + "/clock/" + latest_clock + "\""

		if user_gti_file != 'none':
			cmd += " usrgtifile=" + user_gti_file + " usrgtibarycorr=yes"

		run(cmd)

		if filter_evt_flag:
			xsel_cmd = '''dummy
	read eve
	./ 
	FPM%s_%.1f_%.1f_cl_barycorr.evt 
	yes 
	filter reg %s%s.reg 
	extra eve
	save eve %s%s.evt




	quit





	'''
			os.chdir(outdir_base + '_lc')
			for unit in ['A', 'B']:
				for reg in ['source', 'background']:
					with open('xsel_%s_%s.txt' % (reg, unit), 'w') as ff:
						ff.write(xsel_cmd % (unit, e_min, e_max, reg, unit, reg, unit))
					cmd = 'xselect < ' + 'xsel_%s_%s.txt' % (reg, unit)
					run(cmd)
			os.chdir('..')
		# logfile.close()

	if spec_flag:
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before spectral extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_spec"
		#logfile_name = \
		prepare_outdir(outdir)

		src_regionA = outdir + "/sourceA.reg"
		src_regionB = outdir + "/sourceB.reg"
		bkg_regionA = outdir + "/backgroundA.reg"
		bkg_regionB = outdir + "/backgroundB.reg"

		if ((not os.path.isfile(src_regionA)) or \
				(not os.path.isfile(src_regionB)) or \
				(not os.path.isfile(bkg_regionA)) or \
				(not os.path.isfile(bkg_regionB))):
			raise RuntimeError('You need to have region files in %s make them with the option region_flag' % outdir)

		cmd = "cd " + outdir + ";nuproducts indir=../" + outdir_pipeline + " instrument=FPMA steminputs=nu" + obsid + " stemout=FPMA outdir=."  # +outdir
		cmd += " srcregionfile=../" + src_regionA + " bkgregionfile=../" + bkg_regionA + " bkgextract=yes runbackscale=yes cleanup=yes "
		cmd += " lcfile=NONE bkglcfile=NONE runmkarf=yes runmkrmf=yes imagefile=NONE clobber=yes"

		if user_gti_file != 'none':
			cmd += " usrgtifile=../" + user_gti_file + " usrgtibarycorr=no"

		cmd += ";cd .."
		run(cmd)

		cmd = "cd " + outdir + ";nuproducts indir=../" + outdir_pipeline + " instrument=FPMB steminputs=nu" + obsid + " stemout=FPMB outdir=."  # +outdir
		cmd += " srcregionfile=../" + src_regionB + " bkgregionfile=../" + bkg_regionB + " bkgextract=yes runbackscale=yes cleanup=yes "
		cmd += " lcfile=NONE bkglcfile=NONE runmkarf=yes runmkrmf=yes imagefile=NONE clobber=yes"

		if user_gti_file != 'none':
			cmd += " usrgtifile=../" + user_gti_file + " usrgtibarycorr=no"

		cmd += ";cd .."

		run(cmd)

		cmd = "optimal_binning.py " + outdir + "/FPMA_sr.pha -b " + outdir + "/FPMA_bk.pha -r " + outdir + "/FPMA_sr.rmf -a " + outdir + "/FPMA_sr.arf -e 3 -E 78"
		run(cmd)

		cmd = "optimal_binning.py " + outdir + "/FPMB_sr.pha -b " + outdir + "/FPMB_bk.pha -r " + outdir + "/FPMB_sr.rmf -a " + outdir + "/FPMB_sr.arf -e 3 -E 78"
		run(cmd)

		#logfile.close()
	return 0


def process():
	help = sys.argv[0] + '\n'
	help += '\n'
	help += 'Process Nustar repository and extracts only LC and image or also spectrum with background\n'

	parser = argparse.ArgumentParser(description='Process Nustar Data',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('OBSID', metavar='obsid', type=str, nargs=1, help='OBSID in the Repository folder')
	parser.add_argument("RA", metavar='ra', nargs=1, help="RA of the source", type=float)
	parser.add_argument("Dec", metavar='dec', nargs=1, help="Dec of the source", type=float)
	parser.add_argument('outdir', metavar='outdir', type=str, nargs=1,
						help='output folder base name (to be appended with _pipeline, _lc, or _spec')
	parser.add_argument("--regions", help="Writes (if not present) and checks regions with ds9 (no js9)",
						action='store_true')
	parser.add_argument("--pipeline", help="Run pipeline", action='store_true')
	parser.add_argument("--spec", help="Run spectral extraction", action='store_true')
	parser.add_argument("--lightcurve", help="Run light curve extraction", action='store_true')
	parser.add_argument("--filter_evt", help="Extract events for region files", action='store_true')

	parser.add_argument("--no-ds9", help="Avoid ds9 display", action='store_true')

	parser.add_argument("--usergti", help="User defined GTIs", type=str, default='none')

	parser.add_argument("--timebin", help="timebin for LC (s)", type=float, default=100)

	parser.add_argument("--eMin", help="minimum energy (keV) for LC", type=float, default=3)
	parser.add_argument("--eMax", help="maximum energy (keV) for LC", type=float, default=30)

	parser.add_argument("--ra_back", help="RA center of background region", type=float, default=-1)
	parser.add_argument("--dec_back", help="Dec center of background region", type=float, default=-1)
	parser.add_argument("--radius", help="radius of regions", type=float, default=120)

	parser.add_argument("--write_baryevtfile", help="write barycentric corrected event files (in lightcurve)",
						action='store_true')

	parser.add_argument("--repository", help='Location of the repository', type=str,
						default=os.environ['HOME']+'/NuSTAR/Repository')

	if len(sys.argv) == 1:
		parser.print_help()
		print(help)
		sys.exit(1)

	args = parser.parse_args()

	#repository_location='/gpfs0/ferrigno/NuSTAR/Repository'
	repository_location = args.repository
	if (not os.path.isdir(repository_location)):
		logger.error("The repository location you specified does not exist "+repository_location)
		sys.exit(1)

	PID = os.getpid()
	logger.info("------------------------------------------------------------------------------------------------")
	logger.info(" PID of the process %d" % PID)
	logger.info(" kill -9 -%d  to kill current proc and children" % PID)
	logger.info("------------------------------------------------------------------------------------------------")

	obsid = args.OBSID[0]
	outdir_base = args.outdir[0]
	ra_src = args.RA[0]
	dec_src = args.Dec[0]
	pipeline_flag = args.pipeline
	region_flag = args.regions
	lc_flag = args.lightcurve
	spec_flag = args.spec
	ds9_flag = args.no_ds9
	ra_back = args.ra_back
	dec_back = args.dec_back
	radius = args.radius
	write_baryevtfile_flag = args.write_baryevtfile
	filter_evt_flag = args.filter_evt
	t_bin = args.timebin
	e_min = args.eMin
	e_max = args.eMax
	user_gti_file = args.usergti

	out = wrap_process(obsid, ra_src, dec_src, outdir_base, pipeline_flag, region_flag, spec_flag, lc_flag,
				 ds9_flag, ra_back, dec_back, radius, write_baryevtfile_flag, filter_evt_flag,
				 user_gti_file, repository_location, t_bin, e_min, e_max)

	if out != 0:
		sys.exit(out)

def script_data():
	help = "get_data.py OBSID\n"

	if len(sys.argv) < 2:
		print(help)
		sys.exit(1)

	obsid = sys.argv[1]

	from nustarpipeline import process

	process.get_data(obsid)

def standard_processing_after_regions():
	# Not a completely general tool, specific for a project
	# Usable calling this file
	help = sys.argv[0] + '\n'
	help += '\n'
	help += 'Process Nustar repository and extracts standard products for the HMXB project\n'

	parser = argparse.ArgumentParser(description='Standard Process Nustar Data for the HMXB project',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('mypath', metavar='mypath', type=str, nargs=1,
						help='Path whenre you process data , e.g. Her_X1/10202002002 ')

	parser.add_argument('--outdir', type=str, default='obs',
						help='output folder base name (to be appended with _pipeline, _lc, or _spec')

	parser.add_argument("--timebin", help="timebin for LC (s)", type=float, default=0.1)

	parser.add_argument("--eMin", help="minimum energy (keV) for LC", type=float, default=3)
	parser.add_argument("--eMed", help="medium energy (keV) for LC", type=float, default=7)
	parser.add_argument("--eMax", help="maximum energy (keV) for LC", type=float, default=30)
	parser.add_argument("--repository", help='Location of the repository', type=str,
						default=os.environ['HOME']+'/NUSTAR/Repository')
	parser.add_argument("--clean", help="Cleans products before extracting", action='store_true')

	if len(sys.argv) == 1:
		parser.print_help()
		print(help)
		sys.exit(1)

	args = parser.parse_args()
	my_path = args.mypath[0]
	outdir_base = args.outdir

	t_bin = args.timebin
	e_min = args.eMin
	e_med = args.eMed
	e_max = args.eMax
	repository = args.repository
	clean = args.clean

	print("Path is %s" % my_path)

	try:
		os.chdir(my_path)
	except:
		raise FileExistsError("The folder %s does not exist" % my_path)

	import yaml

	try:
		with open('observation.yml', 'r') as outfile:
			src_dict = yaml.load(outfile, Loader=yaml.FullLoader)
	except:
		raise FileExistsError("The file observation.yams does not exist in  %s" % my_path)

	print(src_dict)

	from nustarpipeline import process, utils

	obsid = src_dict['OBSID']
	ra_src = src_dict['RA']
	dec_src = src_dict['DEC']

	if ((not os.path.isfile(outdir_base + "_spec/sourceA.reg")) or \
			(not os.path.isfile(outdir_base + "_spec/sourceB.reg")) or \
			(not os.path.isfile(outdir_base + "_spec/backgroundA.reg")) or \
			(not os.path.isfile(outdir_base + "_spec/backgroundB.reg"))):
		raise FileExistsError(
			'You need to have region files in %s_spec make them with the option region_flag' % outdir_base)

	if clean:
		extensions_spec = ['pha', 'pi', 'arf', 'rmf', 'gif']
		cmd = 'rm -f'
		for ee in extensions_spec:
			cmd += ' %s_spec/*.%s' % (outdir_base, ee)
		process.run(cmd)

		extensions_lc = ['pha', 'evt', 'lc', 'pco', 'xco', 'reg', 'txt']
		cmd = 'rm -f'
		for ee in extensions_lc:
			cmd += ' %s_lc/*.%s' % (outdir_base, ee)
		process.run(cmd)

	process.wrap_process(obsid, ra_src, dec_src, outdir_base,  spec_flag=True, repository_location=repository)

	process.wrap_process(obsid, ra_src, dec_src, outdir_base, lc_flag=True, t_bin=t_bin, e_min=e_min, e_max=e_med,
						 repository_location=repository)

	process.wrap_process(obsid, ra_src, dec_src, outdir_base, lc_flag=True, t_bin=t_bin, e_min=e_med,
						 e_max=e_max, write_baryevtfile_flag=True, filter_evt_flag=True,
						 repository_location=repository)

	os.chdir(outdir_base+'_spec/')
	utils.make_basic_fit()
	os.chdir('..')

if __name__ == "__main__":
	standard_processing_after_regions()

