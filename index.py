#!/usr/bin/env python

import os
import cgitb
import cgi
cgitb.enable()
import astropy.coordinates

import observations

def build_select_sites(selected):
	sites = ''
	for s in astropy.coordinates.EarthLocation.get_site_names():
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

	html_form += '<label for="target_object_name">Target</label>'
	html_form += '<input type="name" id="target_object_name" name="target_object_name" value="' + target_object_name + '"/><br>'

	html_form += '<label for="target_period">Date</label>'
	html_form += '<input type="date" id="target_period" name="target_period" value="' + target_period +  '"/><br>'

	html_form += '<input type="submit" value="Submit">'
	html_form += '</form>'
	return html_form
 


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
	#print observations.generate_graph('M45', '2018-10-12 23:00:00', 'lapalma', 'div')
	print '<div id="aladin-lite-div"></div>'
	print '<script type="text/javascript" charset="utf_8" src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>'
	print '<script type="text/javascript" charset="utf_8" src="https://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.js"></script>'
	print '<script type="text/javascript">aladin = A.aladin("#aladin-lite-div", {survey: "P/DSS2/color", fov: 60,showReticle: true,showZoomControl: true, showFullScreenControl: true, showLayersControl: true, showGotoControl: true, showShareControl: true, fulscreen: true });</script>'

	print "</body>"
	print "</html>"

