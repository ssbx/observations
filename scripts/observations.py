#!/usr/bin/env python 
""" 
Observations blablabla 

Herve Bouy

"""


""" Requires this for astropy to work correctly with wsgi """
import os
if __name__ != '__main__':
	os.environ.update({
		'XDG_CONFIG_HOME': '/var/www/astropyconfig',
		'XDG_CACHE_HOME':  '/var/www/astropycache'})


import astropy.units 		as u
import matplotlib.pyplot 	as plt
import numpy 				as np
import plotly.offline 		as py
import plotly.graph_objs 	as go
import cgi
import json
import sys
from astropy.config			import get_config_dir, get_cache_dir
from astropy.coordinates 	import SkyCoord, EarthLocation, AltAz, get_sun, get_moon
from astropy.time 			import Time
from astropy.visualization 	import astropy_mpl_style

EarthLocation.get_site_names()
plt.style.use(astropy_mpl_style)
graph_output_type = 'div'


def application(environ, start_response):

	""" This is the function called from the web server in a WSGI environment """



	req_data = cgi.parse_qs(environ['QUERY_STRING'])
	commands = ['getsites', 'draw']

	if not req_data.get('query'):
		return http_reply('400 Bad Request', '', start_response)

	if req_data.get('query')[0] == 'getsites':
		return http_reply('200 OK', json.dumps(sorted(filter(None, EarthLocation.get_site_names()))), start_response);

	if req_data.get('query')[0] == 'draw':

		if not req_data.get('site'):
			return http_reply('400 Bad Request (No site defined)', '', start_response)

		if not req_data.get('target'):
			return http_reply('400 Bad Request (No target defined)', '', start_response)

		if not req_data.get('date'):
			return http_reply('400 Bad Request (No date defined)', '', start_response)

		req_site 	= req_data.get('site')[0]
		str_target 	= req_data.get('target')[0]
		req_date	= req_data.get('date')[0]
		print >> sys.stderr, req_date

		if str_target.startswith('('):
			str_target = str_target[1:-1]
			str_coords = str_target.split(',')
			req_target = SkyCoord(str_coords[0], str_coords[1], unit='deg')
		else:
			try:
				req_target = SkyCoord.from_name(str_target)
			except Exception: 
				return http_reply('400 Bad Request (Unable to find object)', '', start_response)

		graph_data = generate_graph(req_target, req_date, req_site);
		rep = json.dumps({'lat': req_target.ra.degree, 'lon': req_target.dec.degree, 'div': graph_data})    

		return http_reply('200 OK', rep, start_response);

	return http_reply('400 Bad Request (unknonwn query)', '', start_response)





def http_reply(status, message, start_response):
	response_headers = [
		('Content-type', 'application/json'),
		('Content-Length', str(len(message)))]
	start_response(status, response_headers)
	return [message]


def generate_graph(target, date, site):

	""" 
	Our main function. Is currently called either from a WSGI application. Could be called from command line
	with little efforts 
	"""
	
	# Menu deroulant pour choisir l'observatoire parmis toute la liste que donne astropy:
	# ici comme exemple j'ai choisi La Palma
	observatory = EarthLocation.of_site(site)

	# ici il faut donner la difference d'heure entre le fuseau de l'observatoire et le fuseau UTC 
	# (qui est a zero par definition)
	# la je le fais a la main, mais bien sur ca sera faut pour chaque observatoire...
	# idealement il faudrait utiliser le package pytz, pour determiner la difference d'heure a partir des 
	# coordonnees (lat,long) de l'observatoire qui sont dans la variable "observatory"
	utcoffset = 0*u.hour  
	
	# date au hasard: dans l'interface offrir un calendrier pour la date
	time = Time(date + ' 23:00:00') - utcoffset
	
	### On commence a calculer le bazar
	targetaltaz = target.transform_to(AltAz(obstime=time,location=observatory))
	#print("Target's's Altitude = {0.alt:.2}".format(targetaltaz))
	
	
	midnight = Time(date + ' 00:00:00') - utcoffset
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
	div_content = py.plot(fig, output_type=graph_output_type)
	return div_content


""" for test purpose """
if __name__ == '__main__':
	graph_output_type = 'file';
	generate_graph(SkyCoord.from_name(sys.argv[1]), sys.argv[2], sys.argv[3])


