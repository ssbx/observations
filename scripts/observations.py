#!/usr/bin/env python 
""" 
Observations blablabla 

Herve Bouy

"""

import astropy.units 		as u
import cgi
import json
import matplotlib.pyplot 	as plt
import numpy 				as np
import os
import plotly.offline 		as py
import plotly.graph_objs 	as go
import sys

from astropy.coordinates 	import SkyCoord, EarthLocation, AltAz
from astropy.coordinates 	import get_sun, get_moon
from astropy.time 			import Time
from astropy.visualization 	import astropy_mpl_style
from astropy.coordinates import EarthLocation

#sites = EarthLocation.get_site_names()
#print "sites = {"
#for i in sites:
#	sss = EarthLocation.of_site(i)
#	print  "\t'" + i + "'" + ': EarthLocation.from_geocentric(' + str(float(sss.x * u.m)) + ' * u.m, ' + str(float(sss.y * u.m)) + ' * u.m ,' + str(float(sss.z * u.m)) + ' * u.m),'
#print '}'
#

# Sites hard coded
sites = {
	'ALMA': EarthLocation.from_geocentric(2225015.30883  * u.m, -5440016.418  * u.m ,-2481631.27428  * u.m),
	'Anglo-Australian Observatory': EarthLocation.from_geocentric(-4680888.60272  * u.m, 2805218.44653  * u.m ,-3292788.08045  * u.m),
	'Apache Point': EarthLocation.from_geocentric(-1463969.30185  * u.m, -5166673.34223  * u.m ,3434985.71205  * u.m),
	'Apache Point Observatory': EarthLocation.from_geocentric(-1463969.30185  * u.m, -5166673.34223  * u.m ,3434985.71205  * u.m),
	'Atacama Large Millimeter Array': EarthLocation.from_geocentric(2225015.30883  * u.m, -5440016.418  * u.m ,-2481631.27428  * u.m),
	'BAO': EarthLocation.from_geocentric(-2252166.14637  * u.m, 4312578.59125  * u.m ,4111961.65084  * u.m),
	'Beijing XingLong Observatory': EarthLocation.from_geocentric(-2252166.14637  * u.m, 4312578.59125  * u.m ,4111961.65084  * u.m),
	'Black Moshannon Observatory': EarthLocation.from_geocentric(1003146.79952  * u.m, -4721460.60432  * u.m ,4156337.369  * u.m),
	'CHARA': EarthLocation.from_geocentric(-2484228.60291  * u.m, -4660044.46722  * u.m ,3567867.96114  * u.m),
	'Canada-France-Hawaii Telescope': EarthLocation.from_geocentric(-5464301.77135  * u.m, -2493489.87304  * u.m ,2151085.16951  * u.m),
	'Catalina Observatory': EarthLocation.from_geocentric(-1908564.56758  * u.m, -5042439.42892  * u.m ,3400871.12089  * u.m),
	'Cerro Pachon': EarthLocation.from_geocentric(1820193.06845  * u.m, -5208343.03428  * u.m ,-3194842.50048  * u.m),
	'Cerro Paranal': EarthLocation.from_geocentric(1946618.26103  * u.m, -5467645.09055  * u.m ,-2642488.44771  * u.m),
	'Cerro Tololo': EarthLocation.from_geocentric(1814303.74554  * u.m, -5214365.74362  * u.m ,-3187340.56599  * u.m),
	'Cerro Tololo Interamerican Observatory': EarthLocation.from_geocentric(1814303.74554  * u.m, -5214365.74362  * u.m ,-3187340.56599  * u.m),
	'DCT': EarthLocation.from_geocentric(-1916999.85012  * u.m, -4885954.53343  * u.m ,3615926.2181  * u.m),
	'Discovery Channel Telescope': EarthLocation.from_geocentric(-1916999.85012  * u.m, -4885954.53343  * u.m ,3615926.2181  * u.m),
	'Dominion Astrophysical Observatory': EarthLocation.from_geocentric(-2330984.75142  * u.m, -3532887.32577  * u.m ,4755665.32996  * u.m),
	'GBT': EarthLocation.from_geocentric(882598.251319  * u.m, -4924862.65979  * u.m ,3943712.65334  * u.m),
	'Gemini South': EarthLocation.from_geocentric(1820193.06845  * u.m, -5208343.03428  * u.m ,-3194842.50048  * u.m),
	'Green Bank Telescope': EarthLocation.from_geocentric(882598.251319  * u.m, -4924862.65979  * u.m ,3943712.65334  * u.m),
	'Hale Telescope': EarthLocation.from_geocentric(-2410346.78218  * u.m, -4758666.82504  * u.m ,3487942.97502  * u.m),
	'Haleakala Observatories': EarthLocation.from_geocentric(-5462038.8937  * u.m, -2412577.15927  * u.m ,2243040.99444  * u.m),
	'Happy Jack': EarthLocation.from_geocentric(-1916999.85012  * u.m, -4885954.53343  * u.m ,3615926.2181  * u.m),
	'JCMT': EarthLocation.from_geocentric(-5464588.77123  * u.m, -2493006.27658  * u.m ,2150651.61738  * u.m),
	'James Clerk Maxwell Telescope': EarthLocation.from_geocentric(-5464588.77123  * u.m, -2493006.27658  * u.m ,2150651.61738  * u.m),
	'Jansky Very Large Array': EarthLocation.from_geocentric(-1601184.40192  * u.m, -5041989.95569  * u.m ,3554875.07686  * u.m),
	'Keck Observatory': EarthLocation.from_geocentric(-5464487.8176  * u.m, -2492806.59109  * u.m ,2151240.19452  * u.m),
	'Kitt Peak': EarthLocation.from_geocentric(-1994502.60431  * u.m, -5037538.54233  * u.m ,3358104.9969  * u.m),
	'Kitt Peak National Observatory': EarthLocation.from_geocentric(-1994502.60431  * u.m, -5037538.54233  * u.m ,3358104.9969  * u.m),
	'La Silla Observatory': EarthLocation.from_geocentric(1838554.958  * u.m, -5258914.42492  * u.m ,-3099898.78073  * u.m),
	'Large Binocular Telescope': EarthLocation.from_geocentric(-1827016.38224  * u.m, -5054821.44254  * u.m ,3427725.46996  * u.m),
	'Las Campanas Observatory': EarthLocation.from_geocentric(1845655.49905  * u.m, -5270856.29472  * u.m ,-3075330.77761  * u.m),
	'Lick Observatory': EarthLocation.from_geocentric(-2663565.85954  * u.m, -4323362.65807  * u.m ,3848537.52539  * u.m),
	'Lowell Observatory': EarthLocation.from_geocentric(-1918329.73705  * u.m, -4861253.21396  * u.m ,3647910.33905  * u.m),
	'Manastash Ridge Observatory': EarthLocation.from_geocentric(-2228982.31312  * u.m, -3749888.25304  * u.m ,4639060.08647  * u.m),
	'McDonald Observatory': EarthLocation.from_geocentric(-1330755.33952  * u.m, -5328782.75909  * u.m ,3235696.53477  * u.m),
	'Medicina': EarthLocation.from_geocentric(4461340.48314  * u.m, 919588.070091  * u.m ,4449530.22144  * u.m),
	'Medicina Dish': EarthLocation.from_geocentric(4461340.48314  * u.m, 919588.070091  * u.m ,4449530.22144  * u.m),
	'Michigan-Dartmouth-MIT Observatory': EarthLocation.from_geocentric(-1996199.36483  * u.m, -5037542.31817  * u.m ,3356753.85283  * u.m),
	'Mount Graham International Observatory': EarthLocation.from_geocentric(-1827016.38224  * u.m, -5054821.44254  * u.m ,3427725.46996  * u.m),
	'Mt Graham': EarthLocation.from_geocentric(-1827016.38224  * u.m, -5054821.44254  * u.m ,3427725.46996  * u.m),
	'Mt. Ekar 182 cm. Telescope': EarthLocation.from_geocentric(4360770.74995  * u.m, 893641.338736  * u.m ,4554554.75996  * u.m),
	'Mt. Stromlo Observatory': EarthLocation.from_geocentric(-4467466.8037  * u.m, 2681743.2134  * u.m ,-3667393.64946  * u.m),
	'Multiple Mirror Telescope': EarthLocation.from_geocentric(-1937367.38349  * u.m, -5077451.89231  * u.m ,3332444.16131  * u.m),
	'NOV': EarthLocation.from_geocentric(2067324.12839  * u.m, -5958861.85296  * u.m ,968767.080682  * u.m),
	'National Observatory of Venezuela': EarthLocation.from_geocentric(2067324.12839  * u.m, -5958861.85296  * u.m ,968767.080682  * u.m),
	'Noto': EarthLocation.from_geocentric(4934491.88371  * u.m, 1321168.5664  * u.m ,3806398.80386  * u.m),
	'Observatorio Astronomico Nacional, San Pedro Martir': EarthLocation.from_geocentric(-2354953.99638  * u.m, -4940160.36364  * u.m ,3270123.70696  * u.m),
	'Observatorio Astronomico Nacional, Tonantzintla': EarthLocation.from_geocentric(-872146.41921  * u.m, -5968217.95849  * u.m ,2066779.69943  * u.m),
	'Palomar': EarthLocation.from_geocentric(-2410346.78218  * u.m, -4758666.82504  * u.m ,3487942.97502  * u.m),
	'Paranal Observatory': EarthLocation.from_geocentric(1946618.26103  * u.m, -5467645.09055  * u.m ,-2642488.44771  * u.m),
	'Roque de los Muchachos': EarthLocation.from_geocentric(5327448.99578  * u.m, -1718665.7387  * u.m ,3051566.90295  * u.m),
	'SAAO': EarthLocation.from_geocentric(5041505.52268  * u.m, 1916176.60697  * u.m ,-3396663.97487  * u.m),
	'SALT': EarthLocation.from_geocentric(5041505.52268  * u.m, 1916176.60697  * u.m ,-3396663.97487  * u.m),
	'SRT': EarthLocation.from_geocentric(4865168.39956  * u.m, 791921.113677  * u.m ,4035120.6192  * u.m),
	'Siding Spring Observatory': EarthLocation.from_geocentric(-4680819.69849  * u.m, 2805720.33556  * u.m ,-3292431.71483  * u.m),
	'Southern African Large Telescope': EarthLocation.from_geocentric(5041505.52268  * u.m, 1916176.60697  * u.m ,-3396663.97487  * u.m),
	'Subaru': EarthLocation.from_geocentric(-5464468.10972  * u.m, -2493053.65045  * u.m ,2150943.60508  * u.m),
	'Subaru Telescope': EarthLocation.from_geocentric(-5464468.10972  * u.m, -2493053.65045  * u.m ,2150943.60508  * u.m),
	'Sutherland': EarthLocation.from_geocentric(5041505.52268  * u.m, 1916176.60697  * u.m ,-3396663.97487  * u.m),
	'TUG': EarthLocation.from_geocentric(4413555.87255  * u.m, 2582749.21567  * u.m ,3803289.51172  * u.m),
	'UKIRT': EarthLocation.from_geocentric(-5464374.16997  * u.m, -2493677.16726  * u.m ,2150638.13115  * u.m),
	'United Kingdom Infrared Telescope': EarthLocation.from_geocentric(-5464374.16997  * u.m, -2493677.16726  * u.m ,2150638.13115  * u.m),
	'Vainu Bappu Observatory': EarthLocation.from_geocentric(1206621.15671  * u.m, 6108765.37778  * u.m ,1379891.3544  * u.m),
	'Very Large Array': EarthLocation.from_geocentric(-1601184.40192  * u.m, -5041989.95569  * u.m ,3554875.07686  * u.m),
	'W. M. Keck Observatory': EarthLocation.from_geocentric(-5464487.8176  * u.m, -2492806.59109  * u.m ,2151240.19452  * u.m),
	'Whipple': EarthLocation.from_geocentric(-1936768.80809  * u.m, -5077878.69513  * u.m ,3331595.44464  * u.m),
	'Whipple Observatory': EarthLocation.from_geocentric(-1936768.80809  * u.m, -5077878.69513  * u.m ,3331595.44464  * u.m),
	'aao': EarthLocation.from_geocentric(-4680888.60272  * u.m, 2805218.44653  * u.m ,-3292788.08045  * u.m),
	'alma': EarthLocation.from_geocentric(2225015.30883  * u.m, -5440016.418  * u.m ,-2481631.27428  * u.m),
	'apo': EarthLocation.from_geocentric(-1463969.30185  * u.m, -5166673.34223  * u.m ,3434985.71205  * u.m),
	'bmo': EarthLocation.from_geocentric(1003146.79952  * u.m, -4721460.60432  * u.m ,4156337.369  * u.m),
	'cfht': EarthLocation.from_geocentric(-5464301.77135  * u.m, -2493489.87304  * u.m ,2151085.16951  * u.m),
	'ctio': EarthLocation.from_geocentric(1814303.74554  * u.m, -5214365.74362  * u.m ,-3187340.56599  * u.m),
	'dao': EarthLocation.from_geocentric(-2330984.75142  * u.m, -3532887.32577  * u.m ,4755665.32996  * u.m),
	'dct': EarthLocation.from_geocentric(-1916999.85012  * u.m, -4885954.53343  * u.m ,3615926.2181  * u.m),
	'ekar': EarthLocation.from_geocentric(4360770.74995  * u.m, 893641.338736  * u.m ,4554554.75996  * u.m),
	'example_site': EarthLocation.from_geocentric(3980608.90247  * u.m, -102.475229106  * u.m ,4966861.2731  * u.m),
	'flwo': EarthLocation.from_geocentric(-1936768.80809  * u.m, -5077878.69513  * u.m ,3331595.44464  * u.m),
	'gbt': EarthLocation.from_geocentric(882598.251319  * u.m, -4924862.65979  * u.m ,3943712.65334  * u.m),
	'gemini_north': EarthLocation.from_geocentric(-5464283.96573  * u.m, -2493783.6435  * u.m ,2150785.90624  * u.m),
	'gemini_south': EarthLocation.from_geocentric(1820193.06845  * u.m, -5208343.03428  * u.m ,-3194842.50048  * u.m),
	'gemn': EarthLocation.from_geocentric(-5464283.96573  * u.m, -2493783.6435  * u.m ,2150785.90624  * u.m),
	'gems': EarthLocation.from_geocentric(1820193.06845  * u.m, -5208343.03428  * u.m ,-3194842.50048  * u.m),
	'greenwich': EarthLocation.from_geocentric(3980608.90247  * u.m, -102.475229106  * u.m ,4966861.2731  * u.m),
	'haleakala': EarthLocation.from_geocentric(-5462038.8937  * u.m, -2412577.15927  * u.m ,2243040.99444  * u.m),
	'irtf': EarthLocation.from_geocentric(-5464291.32619  * u.m, -2493446.8367  * u.m ,2151022.50631  * u.m),
	'jcmt': EarthLocation.from_geocentric(-5464588.77123  * u.m, -2493006.27658  * u.m ,2150651.61738  * u.m),
	'keck': EarthLocation.from_geocentric(-5464487.8176  * u.m, -2492806.59109  * u.m ,2151240.19452  * u.m),
	'kpno': EarthLocation.from_geocentric(-1994502.60431  * u.m, -5037538.54233  * u.m ,3358104.9969  * u.m),
	'lapalma': EarthLocation.from_geocentric(5327448.99578  * u.m, -1718665.7387  * u.m ,3051566.90295  * u.m),
	'lasilla': EarthLocation.from_geocentric(1838554.958  * u.m, -5258914.42492  * u.m ,-3099898.78073  * u.m),
	'lbt': EarthLocation.from_geocentric(-1827016.38224  * u.m, -5054821.44254  * u.m ,3427725.46996  * u.m),
	'lco': EarthLocation.from_geocentric(1845655.49905  * u.m, -5270856.29472  * u.m ,-3075330.77761  * u.m),
	'lick': EarthLocation.from_geocentric(-2663565.85954  * u.m, -4323362.65807  * u.m ,3848537.52539  * u.m),
	'lowell': EarthLocation.from_geocentric(-1918329.73705  * u.m, -4861253.21396  * u.m ,3647910.33905  * u.m),
	'mcdonald': EarthLocation.from_geocentric(-1330755.33952  * u.m, -5328782.75909  * u.m ,3235696.53477  * u.m),
	'mdm': EarthLocation.from_geocentric(-1996199.36483  * u.m, -5037542.31817  * u.m ,3356753.85283  * u.m),
	'medicina': EarthLocation.from_geocentric(4461340.48314  * u.m, 919588.070091  * u.m ,4449530.22144  * u.m),
	'mmt': EarthLocation.from_geocentric(-1937367.38349  * u.m, -5077451.89231  * u.m ,3332444.16131  * u.m),
	'mro': EarthLocation.from_geocentric(-2228982.31312  * u.m, -3749888.25304  * u.m ,4639060.08647  * u.m),
	'mso': EarthLocation.from_geocentric(-4467466.8037  * u.m, 2681743.2134  * u.m ,-3667393.64946  * u.m),
	'mtbigelow': EarthLocation.from_geocentric(-1908564.56758  * u.m, -5042439.42892  * u.m ,3400871.12089  * u.m),
	'mwo': EarthLocation.from_geocentric(-2484228.60291  * u.m, -4660044.46722  * u.m ,3567867.96114  * u.m),
	'noto': EarthLocation.from_geocentric(4934491.88371  * u.m, 1321168.5664  * u.m ,3806398.80386  * u.m),
	'ohp': EarthLocation.from_geocentric(4578422.55526  * u.m, 458063.411305  * u.m ,4403011.07237  * u.m),
	'paranal': EarthLocation.from_geocentric(1946618.26103  * u.m, -5467645.09055  * u.m ,-2642488.44771  * u.m),
	'salt': EarthLocation.from_geocentric(5041505.52268  * u.m, 1916176.60697  * u.m ,-3396663.97487  * u.m),
	'sirene': EarthLocation.from_geocentric(4575207.58706  * u.m, 439490.223223  * u.m ,4408855.73665  * u.m),
	'spm': EarthLocation.from_geocentric(-2354953.99638  * u.m, -4940160.36364  * u.m ,3270123.70696  * u.m),
	'srt': EarthLocation.from_geocentric(4865168.39956  * u.m, 791921.113677  * u.m ,4035120.6192  * u.m),
	'sso': EarthLocation.from_geocentric(-4680819.69849  * u.m, 2805720.33556  * u.m ,-3292431.71483  * u.m),
	'tona': EarthLocation.from_geocentric(-872146.41921  * u.m, -5968217.95849  * u.m ,2066779.69943  * u.m),
	'tug': EarthLocation.from_geocentric(4413555.87255  * u.m, 2582749.21567  * u.m ,3803289.51172  * u.m),
	'ukirt': EarthLocation.from_geocentric(-5464374.16997  * u.m, -2493677.16726  * u.m ,2150638.13115  * u.m),
	'vbo': EarthLocation.from_geocentric(1206621.15671  * u.m, 6108765.37778  * u.m ,1379891.3544  * u.m),
	'vla': EarthLocation.from_geocentric(-1601184.40192  * u.m, -5041989.95569  * u.m ,3554875.07686  * u.m),
}
plt.style.use(astropy_mpl_style)

def generate_graph(target, date, site, out_type):

	""" Our main function. Is currently called either from a WSGI application, or from the command line """
	
	# Menu deroulant pour choisir l'observatoire parmis toute la liste que donne astropy:
	# ici comme exemple j'ai choisi La Palma
	#observatory = EarthLocation.of_site(site)
	observatory = sites[site] 

	# ici il faut donner la difference d'heure entre le fuseau de l'observatoire et le fuseau UTC 
	# (qui est a zero par definition)
	# la je le fais a la main, mais bien sur ca sera faut pour chaque observatoire...
	# idealement il faudrait utiliser le package pytz, pour determiner la difference d'heure a partir des 
	# coordonnees (lat,long) de l'observatoire qui sont dans la variable "observatory"
	utcoffset = 0*u.hour  
	
	# date au hasard: dans l'interface offrir un calendrier pour la date
	time = Time(date) - utcoffset
	
	### On commence a calculer le bazar
	targetaltaz = target.transform_to(AltAz(obstime=time,location=observatory))
	#print("Target's's Altitude = {0.alt:.2}".format(targetaltaz))
	
	
	midnight = Time('2018-10-13 00:00:00') - utcoffset
	delta_midnight = np.linspace(-2, 10, 100)*u.hour
	frame_July13night = AltAz(obstime=midnight+delta_midnight,
							  location=observatory)
	targetaltazs_July13night = target.transform_to(frame_July13night)
	
	##############################################################################
	# convert alt, az to airmass with `~astropy.coordinates.AltAz.secz` attribute:
	
	targetairmasss_July13night = targetaltazs_July13night.secz
	
	
	##############################################################################
	# Use  `~astropy.coordinates.get_sun` to find the location of the Sun at 1000
	# evenly spaced times between noon on July 12 and noon on July 13:
	
	delta_midnight = np.linspace(-12, 12, 1000)*u.hour
	times_July12_to_13 = midnight + delta_midnight
	frame_July12_to_13 = AltAz(obstime=times_July12_to_13, location=observatory)
	sunaltazs_July12_to_13 = get_sun(times_July12_to_13).transform_to(frame_July12_to_13)
	
	
	##############################################################################
	# Do the same with `~astropy.coordinates.get_moon` to find when the moon is
	# up. Be aware that this will need to download a 10MB file from the internet
	# to get a precise location of the moon.
	moon_July12_to_13 = get_moon(times_July12_to_13)
	moonaltazs_July12_to_13 = moon_July12_to_13.transform_to(frame_July12_to_13)
	
	
	# Edit the layout
	layout = dict(autosize=True,
		paper_bgcolor='rgba(0,0,0,0)',
		height=500,
		margin=go.layout.Margin(
			l=100,
			r=50,
			b=150,
			t=40,
			pad=4,
		   ),
		title = 'Visibility Chart',
		titlefont = dict(size=26),
		xaxis = dict(title = 'Hours from Midnight',titlefont = dict(size=18), range=[-12, 12],showgrid=False,showline=True,
					 ticks='outside',tickcolor='black',tickwidth=2,ticklen=5,tickfont=dict(size=18)),
		yaxis = dict(title = 'Altitude [deg]',range=[0., 90],titlefont = dict(size=18),showgrid=False,showline=True,ticks='outside',tickcolor='black',
					 tickwidth=2,ticklen=5,tickfont=dict(size=18),hoverformat = '.2f'),
		yaxis2 = dict(title = 'Airmass ',range=[0.,90.],titlefont = dict(size=18),showgrid=False,showline=True,ticks='outside',tickcolor='black',
					 tickwidth=2,ticklen=5,tickfont=dict(size=18),hoverformat = '.2f',overlaying='y',side='right',tickmode='array',
					 tickvals=[90.0,72.25,65.38,56.44,50.28,45.58,38.68,33.75,30.0,24.62],ticktext=["1.00","1.05","1.10","1.20","1.30","1.40","1.60","1.80","2.00","2.40"]),
		shapes = 
			[
			{   # Night
				'type': 'rect',
				'xref': 'x',
				'yref': 'y',
				'x0': delta_midnight.to('hr').value[sunaltazs_July12_to_13.alt < -18*u.deg][0],
				'y0': 0,
				'x1': delta_midnight.to('hr').value[sunaltazs_July12_to_13.alt < -18*u.deg][-1],
				'y1': 90.,
				'line': {'width': 0},
				'fillcolor': 'midnightblue ',
				'layer' : 'below'
			},
	
			{   # Twilight
				'type': 'rect',
				'xref': 'x',
				'yref': 'y',
				'x0': delta_midnight.to('hr').value[sunaltazs_July12_to_13.alt < -0*u.deg][0],
				'y0': 0,
				'x1': delta_midnight.to('hr').value[sunaltazs_July12_to_13.alt < -0*u.deg][-1],
				'y1': 90.,
				'line': {'width': 0},
				'fillcolor': 'midnightblue',
				'opacity' : 0.6,
				'layer' : 'below'
			},
						
				{   # Day
				'type': 'rect',
				'xref': 'x',
				'yref': 'y',
				'x0': delta_midnight.to('hr').value[0],
				'y0': 0,
				'x1': delta_midnight.to('hr').value[-1],
				'y1': 90.,
				'line': {'width': 0},
				'fillcolor': 'skyblue ',
				'opacity' : 0.15,
				'layer' : 'below'
			}],
				 )
	
	
	##############################################################################
	# Find the alt,az coordinates of target at those same times:
	
	targetaltazs_July12_to_13 = target.transform_to(frame_July12_to_13)
	
	traces = []
	
	# Create a trace for the Sun
	traces.append(go.Scatter(
			x=delta_midnight,
			y=sunaltazs_July12_to_13.alt,
			mode='lines',
			name = 'Sun',
			line=dict(color='orange', width=5.0),
			connectgaps=True,
			hoverinfo="none"
		))
	
	# Create a trace for the Moon
	traces.append(go.Scatter(
			x=delta_midnight,
			y=moonaltazs_July12_to_13.alt,
			mode='lines',
			name = 'Moon',
			line=dict(color='lightgrey', width=5.0,dash = 'dot'),
			connectgaps=True,
			hoverinfo="none",
		))
	
	# Create a trace for the target
	traces.append(go.Scatter(
			x=delta_midnight,
			y=targetaltazs_July12_to_13.alt,
			mode='lines',
			name = 'M45',
			line=dict(color='springgreen', width=3.0),
			connectgaps=True,
			text = np.around(targetaltazs_July12_to_13.secz,2),
			hoverinfo = "text",
	#		marker = dict(
	#		color = 'green')
		))
	
	traces.append(go.Scatter(
			x=delta_midnight,
			y=targetaltazs_July12_to_13.secz,
			mode='lines',
			name = 'M45',
			yaxis='y2',
			line=dict(color='springgreen', width=3.0),
			connectgaps=True,
			visible=False
		))
	
	fig = go.Figure(data=traces, layout=layout)
	div_content = py.plot(fig, output_type=out_type)
	return div_content

if __name__ == '__main__':

	""" This one if only triggered if the script is launched from the command line """

	# Ici on choisit l'objet
	# l'utilisateur pourrait avoir le choix:
	# 1) mettre les coordonnees RA,Dec
	# 2) donner le nom (comme dans l'exemple ci dessous) et laisser astropy trouver les coordonnees sur internet
	target = SkyCoord.from_name('M45')

	generate_graph(target, '2018-10-12 23:00:00', 'lapalma', 'file');


def application(environ, start_response):

	""" This is the function called from the web server in a WSGI environment """

	#os.environ.update({
		#'XDG_CONFIG_HOME': '/var/www/astropyconfig',
		#'XDG_CACHE_HOME':  '/var/www/astropycache'
	#})



	req_data = cgi.parse_qs(environ['QUERY_STRING'])
	rep = status = None
	if req_data.get('query'):
		if req_data.get('query')[0] == 'getsites':
			rep = json.dumps(sites.keys());
			status = '200 OK'
	else:
		target = SkyCoord.from_name('M45')
		graph_data = generate_graph(target, '2018-10-12 23:00:00', 'lapalma', 'div');
		rep = json.dumps({'lat': target.ra.degree, 'lon': target.dec.degree, 'div': graph_data})    
		status = '200 OK'



	response_headers = [
		('Content-type', 'application/json'),
		('Content-Length', str(len(rep)))
	]

	start_response(status, response_headers)
	return [rep]


