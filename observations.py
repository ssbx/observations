import plotly.offline as py
import plotly.graph_objs as go

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.coordinates import get_sun, get_moon



def generate_graph(obj_name, date, site, out_type):
	# Ici on choisit l'objet
	# l'utilisateur pourrait avoir le choix:
	# 1) mettre les coordonnees RA,Dec
	# 2) donner le nom (comme dans l'exemple ci dessous) et laisser astropy trouver les coordonnees sur internet
	target = SkyCoord.from_name(obj_name)
	
	
	# Menu deroulant pour choisir l'observatoire parmis toute la liste que donne astropy:
	from astropy.coordinates import EarthLocation
	EarthLocation.get_site_names()
	# ici comme exemple j'ai choisi La Palma
	observatory = EarthLocation.of_site(site)
	# ici il faut donner la difference d'heure entre le fuseau de l'observatoire et le fuseau UTC (qui est a zero par definition)
	# la je le fais a la main, mais bien sur ca sera faut pour chaque observatoire...
	# idealement il faudrait utiliser le package pytz, pour determiner la difference d'heure a partir des coordonnees (lat,long) de l'observatoire qui sont dans la variable "observatory"
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
	
	from astropy.coordinates import get_sun
	delta_midnight = np.linspace(-12, 12, 1000)*u.hour
	times_July12_to_13 = midnight + delta_midnight
	frame_July12_to_13 = AltAz(obstime=times_July12_to_13, location=observatory)
	sunaltazs_July12_to_13 = get_sun(times_July12_to_13).transform_to(frame_July12_to_13)
	
	
	##############################################################################
	# Do the same with `~astropy.coordinates.get_moon` to find when the moon is
	# up. Be aware that this will need to download a 10MB file from the internet
	# to get a precise location of the moon.
	
	from astropy.coordinates import get_moon
	moon_July12_to_13 = get_moon(times_July12_to_13)
	moonaltazs_July12_to_13 = moon_July12_to_13.transform_to(frame_July12_to_13)
	
	
	# Edit the layout
	layout = dict(autosize=False,
		width=1000,
		height=800,
		margin=go.layout.Margin(
			l=150,
			r=50,
			b=75,
			t=50,
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
	generate_graph('M45', '2018-10-12 23:00:00', 'lapalma', 'file');
