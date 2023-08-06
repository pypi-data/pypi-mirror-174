
from datetime import datetime
import os
from itertools import groupby
import xml.etree.ElementTree as ET

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus.figures import Figure
from reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.graphics.charts.lineplots import LinePlot,ScatterPlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.shapes import Drawing   

from .config import AutoReportConfig
from .config import ResultAutoStatImage
	

class MyDocTemplate(BaseDocTemplate):
	def __init__(self, filename, **kw):
		self.allowSplitting = 0
		BaseDocTemplate.__init__(self, filename, **kw)
		template = PageTemplate('normal', [Frame(1*inch, 1*inch, 6*inch, 9*inch, id='F1')])
		self.addPageTemplates(template)
		self.current_key_index = 1
	
	def afterFlowable(self, flowable):
		if flowable.__class__.__name__ == "Paragraph":
			text = flowable.getPlainText()
			style = flowable.style.name
			
			if style == "Heading1":
				self.current_key_index += 1
				key = str(self.current_key_index)
				self.canv.bookmarkPage(key)
				self.canv.addOutlineEntry(text, key, 0, 0)
				self.notify("TOCEntry", (0, text, self.page))
			elif style == "Heading2":
				self.current_key_index += 1
				key = str(self.current_key_index)
				self.canv.bookmarkPage(key)
				self.canv.addOutlineEntry(text, key, 1, 0)
				self.notify("TOCEntry", (1, text, self.page))
			elif style == "Heading3":
				self.current_key_index += 1
				key = str(self.current_key_index)
				self.canv.bookmarkPage(key)
				self.canv.addOutlineEntry(text, key, 2, 0)
				self.notify("TOCEntry", (2, text, self.page))

def get_model_tree(modelFn = ""):
	SKIPPED_CATS = [ "Object View", "Geometry View", "View" , "Display Attributes" ]
	SKIPPED_NAMES = [ "Name", "Enabled" ]
	tree = ET.parse(modelFn)
	root = tree.getroot()
	model = root.find("model")
	
	def sort_by_preferred(x):
		preferred_ordering = [            
			"LatticeDomain",
			"VoxelizedBody",
			"ImmersedBody",
			"SimulationParameters",
			"ParticleZone",
			"BubbleZone",
			"ScalarField",
		]
		if x in preferred_ordering:
			return preferred_ordering.index(x)
		else:
			return len(preferred_ordering)       
	
	def _walk_component(c, component_tables, level):        
		level += 1
		table = [ ["Properties", "Value", "Units" ]  ]        
		
		cat_props = {}

		for p in c.findall("./property"):
			name = p.get("name", "")
			cat = p.get("category", "General")
			units = p.get("units", "")                       
			
			if any([ c in cat for c in SKIPPED_CATS]):
				continue             
			if any([ n in name for n in SKIPPED_NAMES]):
				continue
				
			value = ""
			if p.text is not None:
				value = p.text
				
			table.append([ name, value,  units ])

			if cat not in cat_props:
				cat_props[cat] = []

			cat_props[cat].append([name, value, units])
		
		component_tables.append({
			'name':c.get("name"),
			'table': table,
			'categorized_tables': cat_props,
			'id': "component_"
		})
				
		for child in c.findall("./component"):
			_walk_component(child, component_tables, level)
		
	component_tables = []    
	for c in model.findall("./component"):
		_walk_component(c, component_tables, 1)  
	
	screen_shots = []
	out_dir = os.path.dirname(modelFn)
	for img in root.findall("./screenShots/image"):
		fname = os.path.join(out_dir, img.get("filename"))
		screen_shots.append(fname)

	return component_tables,screen_shots

def create_auto_report(conf: AutoReportConfig, outputfn="Report.pdf"):
	# Report style variables
	styles = getSampleStyleSheet()
	style = styles["Normal"]
	h1 = styles["Heading1"]
	h2 = styles["Heading2"]
	h3 = styles["Heading3"]
	h4 = styles["Heading4"]
	h5 = styles["Heading5"]
	normal = styles["Normal"]

	report = []
	report.append( Spacer(1, 2*inch) )
	report.append( Paragraph(conf.title, h1) )
	report.append( Spacer(1, 2*inch) )
	report.append( Paragraph( "Created: " + datetime.now().strftime("%x - %X"), normal) )
	report.append( Paragraph( conf.title, normal) )

	msbname = ""
	version = ""
	if conf.model_tree_filename is not None and os.path.isfile(conf.model_tree_filename):
		reportxml = ET.parse(conf.model_tree_filename).getroot()
		if (n := reportxml.find("./model")) is not None:
			report.append( Paragraph( "M-Star CFD Version: " + n.get("version", ""), normal) )			
			report.append( Paragraph( "MSB File: " + n.get("filename", ""), normal) )			


	# Report parts
	
	report.append( PageBreak() )

	# Table of contents
	toc = TableOfContents()
	toc.levelStyles = [h1, h2]
	report.append(toc)
	report.append(PageBreak())

	# MSB summary: images, properties listing
	if conf.model_tree_filename is not None and os.path.isfile(conf.model_tree_filename):

		objTree,screens = get_model_tree(conf.model_tree_filename)		
		report.append(Paragraph("Model Summary", h1))

		for screenfn in screens:
			report.append(Image(screenfn, width=4*inch, height=4*inch, kind='bound'))

		for compProps in objTree:
			t = Table(compProps["table"])
			t.setStyle(TableStyle([("ROWBACKGROUNDS", (0,0), (-1,-1), (colors.HexColor(0xe6e6e6), colors.HexColor(0xffffff)))]))
			
			report.append(Paragraph(compProps["name"], h2))
			report.append(t)
		

	# Custom stat plots
	report.append(Paragraph("Stats Plots", h1))
	for plot in conf.results.custom_stat_plots:
		report.append(Paragraph(plot.name, h2))
		img = Image(plot.image_filename, width=6*inch, height=6*inch, kind='bound')
		report.append(img)        				

	# VTK images (only last time shown)
	report.append(Paragraph("VTK Data", h1))

	# Auto stat plots
	def getStatFilename(g: ResultAutoStatImage):
		return g.stat_filename

	auto_stat_plots = sorted(conf.results.auto_stat_plots, key=getStatFilename)

	report.append(Paragraph("Auto Stats Plots", h1))
	for key,group in groupby(auto_stat_plots, key=getStatFilename):
		report.append(Paragraph(os.path.basename(key), h2))
		for plot in group:
			report.append(Paragraph(plot.name, h3))	
			img = Image(plot.image_filename,  width=6*inch, height=6*inch, kind='bound')
			report.append(img)   
	
	print ("-- Writing report PDF:", outputfn)
	doc = MyDocTemplate(outputfn)
	doc.multiBuild(report)
