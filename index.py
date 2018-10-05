#!/usr/bin/env python

import os
import cgitb
import cgi
cgitb.enable()
from astropy.coordinates import SkyCoord, EarthLocation
import observations

def build_select_sites(selected):
	sites = ''
	for s in EarthLocation.get_site_names():
		if not s:
			continue
		sel = ""
		if s == selected:
			sel = "selected"
		sites += '<option value="' + s + '" ' + sel + '>' + s + '</option>\n'
	return sites


def build_form(old_form):
	target_site_name = build_select_sites(old_form.getvalue('target_site_name'));
	target_object_name = old_form.getvalue('target_object_name');
	if not target_object_name:
		target_object_name = ''
	target_period = old_form.getvalue('target_period');
	if not target_period:
		target_period = ''

	html_form = '<form>\n'

	html_form += '<label for="target_site_name">Site</label>\n'
	html_form += '<select name="target_site_name" value="' + "tug" + '">' + target_site_name + '</select><br>'

	html_form += '<label for="target_object_name">Target (name or coordinates in the form of <strong>(LON, LAT)</strong></label>'
	html_form += '<input type="name" id="target_object_name" name="target_object_name" value="' + target_object_name + '"/><br>'

	html_form += '<label for="target_period">Date (evening)</label>'
	html_form += '<input type="date" id="target_period" name="target_period" value="' + target_period +  '"/><br>'

	html_form += '<input type="submit" value="Submit">'
	html_form += '</form>'
	return html_form
 
def get_target_coord(form):
	target_str = form.getvalue('target_object_name')
	if not target_str:
		return None
	if target_str.startswith('('):
		target_str = target_str[1:-1]
		coords = target_str.split(',')
		return SkyCoord(coords[0], coords[1], unit='deg')
	return SkyCoord.from_name(target_str)


if __name__ == '__main__':
	form = cgi.FieldStorage()
	print "Content-type: text/html"
	print
	print "<html>"
	print "<head>"
	print "<title>Observations</title>"
	print '<link rel="stylesheet" href="https://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.css" />'
	print "</head>"
	print "<body>"
	print "<h1>%s %s %s</h1>" % ('a', 'b', 'c')
	print "<h1>Observations</h1>"
	print "<div>" + build_form(form) + "</div>"
	if form.getvalue('target_site_name'):
		if form.getvalue('target_object_name'):
			target_coords = get_target_coord(form)
			ra = target_coords.ra.degree;
			dec = target_coords.dec.degree;
			print observations.generate_graph(get_target_coord(form), '2018-10-12 23:00:00', form.getvalue('target_site_name'), 'div')
	print '<div id="aladin-lite-div"></div>'
	print '<script type="text/javascript" charset="utf_8" src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>'
	print '<script type="text/javascript" charset="utf_8" src="https://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.js"></script>'
	print '<script type="text/javascript"> $(document).ready(function() { aladin = A.aladin("#aladin-lite-div", {survey: "P/DSS2/color", fov: 60,showReticle: true,showZoomControl: true, showFullScreenControl: true, showLayersControl: true, showGotoControl: true, showShareControl: true, fulscreen: true }); aladin.gotoRaDec(' + str(ra) + ',' + str(dec) + '); });</script>'

	print "</body>"
	print "</html>"

