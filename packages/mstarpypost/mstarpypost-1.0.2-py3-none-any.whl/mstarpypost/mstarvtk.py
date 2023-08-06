
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import xml.etree.ElementTree as ET
import os
import re
import io
import glob
import numpy as np
from matplotlib import cm
import matplotlib as mpl
from collections import namedtuple
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import math
import logging

def vtk2pil(renderer, width, height):
	
	renderWindow = vtk.vtkRenderWindow()
	renderWindow.AddRenderer(renderer)
	renderWindow.SetOffScreenRendering(1)
	renderWindow.SetSize(width, height)
	renderWindow.SetMultiSamples(4)
	renderWindow.Render()

	windowto_image_filter = vtk.vtkWindowToImageFilter()
	windowto_image_filter.SetInput(renderWindow)    

	writer = vtk.vtkPNGWriter()
	writer.SetInputConnection(windowto_image_filter.GetOutputPort())

	writer.WriteToMemoryOn()
	writer.Write()

	buf = io.BytesIO()
	buf.write(writer.GetResult())
	buf.seek(0)
	
	return Image.open(buf)    

def fig2pil(fig):
    # Save a matplotlib figure to an PIL Image
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return Image.open(buf)

def make_title_image(title="", subtitle="", size=(500,500)):
    # Make title frame image

    img = Image.new("RGB", size)

    h1 = ImageFont.truetype("arial.ttf", 26)
    h2 = ImageFont.truetype("arial.ttf", 18)
    normal = ImageFont.truetype("arial.ttf", 16)
    draw = ImageDraw.Draw(img)

    if len(title):
        draw.text((size[0]/2, size[1]/2), title, anchor="md", font=h1)

    if len(subtitle):
        draw.text((size[0]/2, size[1]/2), subtitle, anchor="ma", font=h2)

    draw.text((size[0], 0), datetime.now().isoformat(timespec="minutes"), anchor="ra", font=normal)
    draw.text(size, "Created with M-Star CFD", anchor="rd", font=normal)

    return img

class UniqueFloatSet:
	def __init__(self, tolerance=1e-3):
		self.tolerance = tolerance
		self.myset = []
	
	def insert(self, val):
		addVal = False
		for v in self.myset:
			if abs(v - val) > self.tolerance:
				addVal = True
		self.myset.append(val)
		return True
	
	def values(self):
		return self.myset

class ScalarModeEnum:
	Default = 0
	PointData = 1
	CellData = 2
	PointFieldData = 3
	CellFieldData = 4
	FieldData = 5

def AddImageToDims(imgData, bbox, uniqFloats):
	bnds = imgData.GetBounds()
	extent = imgData.GetExtent()
	nx = extent[1] - extent[0]
	ny = extent[3] - extent[2]
	nz = extent[5] - extent[4]
	lx = bnds[1] - bnds[0]
	ly = bnds[3] - bnds[2]
	lz = bnds[5] - bnds[4]
	dx = lx / nx if nx > 0 else 0
	dy = ly / ny if ny > 0 else 0
	dz = lz / nz if nz > 0 else 0
	if dx > 0:
		uniqFloats.insert(dx)
	if dy > 0:
		uniqFloats.insert(dy)
	if dz > 0:
		uniqFloats.insert(dz)
	bbox.AddBounds(bnds)

def GetNiceSamplingBounds(dobj):
	# interrogate a data object and determine good resampling bounds
	
	overallBbox = vtk.vtkBoundingBox()
	uniqueDxs = UniqueFloatSet()
	
	it = dobj.NewIterator()
	it.InitTraversal()
	while not it.IsDoneWithTraversal():
		AddImageToDims(it.GetCurrentDataObject(), overallBbox, uniqueDxs)
		it.GoToNextItem()
	
	maxDx = max(uniqueDxs.values())
	nx = overallBbox.GetLength(0) / maxDx
	ny = overallBbox.GetLength(1) / maxDx
	nz = overallBbox.GetLength(2) / maxDx
	nx = int( max(1, nx) )
	ny = int( max(1, ny) )
	nz = int( max(1, nz) )
	
	return nx, ny, nz
		
def GetFieldDataRanges(fd=None):
	r = []
	for i in range(fd.GetNumberOfArrays()):
		a = fd.GetArray(i)
		ncomp = a.GetNumberOfComponents()
		for ci in range(ncomp):
			amin,amax = a.GetRange(ci)
			r.append( (a.GetName(), ncomp, amin, amax ) )
	return r

def GetVariableRanges(dset):	
	for name,ncomp,compmin,compmax in GetFieldDataRanges(dset.GetCellData()):	
		yield ("CELL", name, ncomp, compmin, compmax )
	for name,ncomp,compmin,compmax in GetFieldDataRanges(dset.GetPointData()):	
		yield ("POINT", name, ncomp, compmin, compmax )

from collections import namedtuple
VariableKey = namedtuple("VariableKey", ["name", "component", "type"])

def GetDataObjectVariableRanges(dobj):
	vars = {}
	if dobj.IsA("vtkCompositeDataSet"):
		it = dobj.NewIterator()
		it.InitTraversal()
		while not it.IsDoneWithTraversal():
			comptype,compname,compi,compmin,compmax = GetVariableRanges(it.GetCurrentDataObject())
			key = VariableKey(name=compname, component=compi, type=comptype)

			if key in vars:
				compmin = min(vars[key][0], compmin)
				compmax = max(vars[key][1], compmax)
			
			vars[key] = (compmin, compmax)
			it.GoToNextItem()
	else:
		for comptype,compname,compi,compmin,compmax in GetVariableRanges(dobj):		 
			key = VariableKey(name=compname, component=compi, type=comptype)
			vars[key] = (compmin, compmax)
	
	for k,v in vars.items():
		yield (k.type, k.name, k.component, v[0], v[1])	

def CellToPointPipeline(inputDataObj):
	if inputDataObj.GetClassName() == "vtkMultiBlockDataSet":
		logging.debug ("-- Multi block data set")
		geoFilter = vtk.vtkCompositeDataGeometryFilter()
		geoFilter.SetInputDataObject(inputDataObj)		
		
		nx, ny, nz = GetNiceSamplingBounds(inputDataObj)			
		resample = vtk.vtkResampleToImage()
		resample.UseInputBoundsOn()
		resample.SetSamplingDimensions(nx, ny, nz)
		resample.SetInputConnection(geoFilter.GetOutputPort())		
		return resample

	else:
		logging.debug ("-- Single block, using vtkCellDataToPointData")
		c2p = vtk.vtkCellDataToPointData()
		c2p.SetInputDataObject(inputDataObj)
		return c2p


def GetAvailableVariables(dset):
	vars = []
	for i in range(dset.GetCellData().GetNumberOfArrays()):
		a = dset.GetCellData().GetAbstractArray(i)
		vars.append( ("CELL", a.GetName(), a.GetNumberOfComponents(), a.GetRange()) )
		
	for i in range(dset.GetPointData().GetNumberOfArrays()):
		a = dset.GetPointData().GetAbstractArray(i)
		vars.append( ("POINT", a.GetName(), a.GetNumberOfComponents(), a.GetRange() ) )
		
	return vars
	
def PrintAvailableVariables(dset):
	v = GetAvailableVariables(dset)
	print(v)

def NiceVariableName(vname=""):
	bad = ['/', '\\', ':', ' ']
	for b in bad:
		vname = vname.replace(b, "")
	return vname

def CreateColorTransferFunction(varname="", minlimit=0, maxlimit=1, colorscale="viridis", ncolors = 256, discrete=False, discreteN=12):	

	ctf = None
	if discrete:
		ctf = vtk.vtkDiscretizableColorTransferFunction ()
		ctf.SetDiscretize(True)
		ctf.SetNumberOfValues(discreteN)
	else:
		ctf = vtk.vtkColorTransferFunction ()

	sampled = np.linspace(minlimit, maxlimit, ncolors)
	norm = mpl.colors.Normalize(minlimit, maxlimit)		
	c = cm.get_cmap(colorscale, ncolors)
	for i in range(ncolors):			
		r,g,b,a = c(norm(sampled[i]))
		ctf.AddRGBPoint(sampled[i], r, g, b)
	return ctf

class PvdReader:
	def __init__(self, pvdfn=""):
		if os.path.isfile(pvdfn):
			self.pvd = pvdfn
		else:
			rel_file = os.path.join("out", "Output", pvdfn)
			if os.path.isfile(rel_file):
				self.pvd = os.path.join("out", "Output", pvdfn)
		
	def get_times(self):
		r = ET.parse(self.pvd).getroot()
		timeset = set()
		for d in r.findall(".//DataSet"):
			timeset.add(float(d.get("timestep")))
		times = sorted(timeset)
		return times
		
	def get_filenames(self, time):
		r = ET.parse(self.pvd).getroot()
		
		pvddir = os.path.dirname(self.pvd)
		fns = []
		for d in r.findall(".//DataSet"):
			if time == float(d.get("timestep")):
				fns.append(os.path.join(pvddir, d.get("file")))
			
		return fns
		
	def get_data(self, time):
		
		blockFileNames = self.get_filenames(time)
		blocks =  [] 		
		for fn in blockFileNames:
			extension = os.path.splitext(fn)[1]
			if extension == ".vti":
				reader = vtk.vtkXMLImageDataReader()
			elif extension == ".vtp":
				reader = vtk.vtkXMLPolyDataReader()
			reader.SetFileName(fn)
			reader.Update()
			blocks.append(reader.GetOutput())

		if len(blocks) == 1:
			return blocks[0]
		else:
			index = 1
			root = vtk.vtkMultiBlockDataSet()		
			for b in blocks:
				root.SetBlock(index, b)
				index += 1
			return root
		return None
	
		
	def print_summary(self):
		print("PVD: ", self.pvd)
		for t in self.get_times():
			print("Time: ", t)
			for fn in self.get_filenames(t):
				print("\t",fn)

class MStarFile:
	def __init__(self, fn=""):
		self.filename=fn
		self.name = os.path.basename(fn)
		self.timegroup = ""
		self.type = ""		
		self.color_by_variable = False
		self.solid_color_default = "lightgrey"

		if self.name == "Walls.stl":
			self.timegroup = "Static"
			self.type = "Walls"
		elif self.name == "BoundaryConditions.pvd":
			self.timegroup = "Static"
			self.type = "BC"
		elif self.name == "Volume.pvd":
			self.timegroup = "Volume"
			self.type = "Volume"
			self.color_by_variable = True
		else:
			m = re.match(r"^(Slice|Volume)([^_]+)_(.*)\.pvd$", self.name)
			if m:
				
				self.timegroup = m.group(1)				
				self.type = m.group(2)
				self.name = m.group(3)

			if self.type in[ "X", "Y", "Z" ]:
				self.color_by_variable = True		

	def __str__(self):
		return "Filename: {0}, Time Group: {1}, Type: {2}".format(self.filename, self.timegroup, self.timegroup)

	def data_ranges(self, time):
		if self.filename.endswith(".pvd"):
			reader = PvdReader(self.filename)
			d = reader.get_data(time)
			return GetDataObjectVariableRanges(d)
		return None

	def get_pipeline(self, model):
		o = None
		if self.type in [ "X", "Y", "Z" ]:
			o = BlockDataPipeline(self.filename, model.get_time())
			o.mapper.SelectColorArray(model.variable)			
			#renderer.AddActor(o.actor)

		elif self.type == "MovingBody":
			o = MovingBodyPipeline(self.filename, model.get_time())
			#renderer.AddActor(o.actor)

		elif self.type == "Walls":
			o = StaticStlPipeline(self.filename)
			#renderer.AddActor(o.actor)

		elif self.type == "Particles":
			o = ParticlesPipeline(self.filename, model.get_time())
			#renderer.AddActor(o.actor)

		elif self.type == "Volume":
			o = VolumeRenderingPipeline(self.filename, model.get_time(), model.get_color(), model.get_opacity())
			o.mapper.SetScalarModeToUsePointFieldData()
			o.mapper.SelectScalarArray(model.variable)
			#renderer.AddVolume(o.actor)
		
		return o

	def add_pipeline(self, model, renderer):
		p = self.get_pipeline(model)
		if p is not None:
			renderer.AddActor(p.actor)

class VolumeRenderingPipeline:
	def __init__(self, fn="", time=0.0, color=None, opacity=None):		
		reader = PvdReader(fn)
		pvd_data = reader.get_data(time)
				
		if pvd_data.GetClassName() == "vtkMultiBlockDataSet":
			logging.debug ("-- Multi block data set")
			geoFilter = vtk.vtkCompositeDataGeometryFilter()
			geoFilter.SetInputDataObject(pvd_data)
			geoFilter.Update()
			last = geoFilter
			
			nx, ny, nz = GetNiceSamplingBounds(pvd_data)			
			resample = vtk.vtkResampleToImage()
			resample.UseInputBoundsOn()
			resample.SetSamplingDimensions(nx, ny, nz)
			resample.SetInputConnection(last.GetOutputPort())
			resample.Update()
			last = resample

		else:
			logging.debug ("-- Single block, using vtkCellDataToPointData")
			c2p = vtk.vtkCellDataToPointData()
			c2p.SetInputDataObject(pvd_data)
			c2p.Update()
			last = c2p

		opacityUnitDistance = 0.001
		im = last.GetOutput()
		imDims = im.GetDimensions()
		maxImDims = max(*imDims)
		bbox = vtk.vtkBoundingBox(im.GetBounds())
		if bbox.IsValid() and maxImDims > 0:
			opacityUnitDistance = 10 * bbox.GetDiagonalLength() / float(maxImDims)		

		self.last_filter = last
		mapper = vtk.vtkSmartVolumeMapper()
		mapper.SetInputConnection(last.GetOutputPort())
		mapper.SetBlendModeToComposite()
		mapper.SetRequestedRenderModeToDefault()		

		prop = vtk.vtkVolumeProperty()
		prop.SetColor(color)
		prop.SetScalarOpacity(opacity)
		prop.ShadeOff()
		prop.SetScalarOpacityUnitDistance(0.01)
		prop.SetInterpolationTypeToLinear()

		actor = vtk.vtkVolume()
		actor.SetMapper(mapper)
		actor.SetProperty(prop)

		self.ranges =  [ r for r in GetDataObjectVariableRanges(last.GetOutputDataObject(0)) ]
		self.reader = reader
		self.mapper = mapper
		self.actor = actor	

		logging.debug (str(self.ranges))

	def get_histogram(self):		

		logging.debug ("Get histogram")
		assignAttr = vtk.vtkAssignAttribute()
		assignAttr.SetInputConnection(self.last_filter.GetOutputPort())
		assignAttr.Assign("Volume Fraction (-)", 0, 0) # assign point field to scalar attribute

		logging.debug ("image stencil")
		stencil = vtk.vtkImageToImageStencil()
		stencil.SetInputConnection(assignAttr.GetOutputPort())
		stencil.ThresholdBetween(0.5, 1.5)
		stencil.Update()

		nbins = 255
		binwidth = 0.01
		binstart = 0

		logging.debug ("image accum")
		accum = vtk.vtkImageAccumulate()
		accum.SetInputConnection(self.last_filter.GetOutputPort())
		accum.SetComponentSpacing(binwidth, binwidth, binwidth)
		accum.SetComponentExtent(0, nbins-1, 0, 0, 0, 0)
		accum.SetComponentOrigin(binstart, 0, 0)
		accum.SetIgnoreZero(True)
		#accum.SetStencilData(stencil.GetOutput())
		logging.debug ("image accum UPDATE")
		accum.Update()
		
		logging.debug ("to numpy")
		counts = vtk_to_numpy(accum.GetOutput().GetPointData().GetScalars())
		bins = np.linspace(binstart, (nbins-1)*binwidth, nbins)
		total = np.sum(counts)

		fxv = counts / total
		fx = counts / (total * binwidth)
		int_fx = np.zeros(fx.shape)
		for i in range(fx.shape[0]):
			int_fx[i] = np.sum(fx[0:i] * binwidth)            

		data = pd.DataFrame({
			"counts": counts,
			"fxv": fxv,
			"fx": fx,
			"integral_fx": int_fx
		}, index=bins)
		return data
		

class ParticlesPipeline:
	def __init__(self, fn="", time=0.0):		
		reader = PvdReader(fn)
		pvd_data = reader.get_data(time)

		glyphSrc = vtk.vtkSphereSource()		
		glyphSrc.SetRadius(0.002)

		glyph = vtk.vtkGlyph3D()
		glyph.SetSourceConnection(glyphSrc.GetOutputPort())
		glyph.SetInputDataObject(pvd_data)
		glyph.ScalingOff()
		last = glyph

		if pvd_data.GetClassName() == "vtkMultiBlockDataSet":

			geoFilter = vtk.vtkCompositeDataGeometryFilter()
			geoFilter.SetInputDataObject(pvd_data)
			geoFilter.Update()
			last = geoFilter	

		ctf = vtk.vtkColorTransferFunction()
		ctf.SetColorSpaceToDiverging()

		colorx = np.linspace(0, 1, 256)
		colorrgb = cm.get_cmap("viridis", len(colorx))
		for x in colorx:
			r,g,b,a = colorrgb(x)
			ctf.AddRGBPoint(x, r, g, b)

		mapper = vtk.vtkDataSetMapper()
		mapper.SetInputConnection(last.GetOutputPort())
		#mapper.SelectColorArray(variable_name)
		#mapper.SetColorModeToMapScalars()
		mapper.ScalarVisibilityOff()
		#mapper.SetLookupTable(ctf)
		#mapper.UseLookupTableScalarRangeOn()
		#mapper.SetScalarModeToUsePointFieldData()
		#mapper.InterpolateScalarsBeforeMappingOn()
		#mapper.SetScalarModeToUseCellFieldData()

		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetRepresentationToSurface()
		actor.GetProperty().SetColor(1, 0, 0)

		self.reader = reader
		self.mapper = mapper
		self.actor = actor

class StaticStlPipeline:
	def __init__(self, fn="", opacity=0.5):
		reader = vtk.vtkSTLReader()
		reader.SetFileName(fn)
		reader.Update()
		mapper = vtk.vtkPolyDataMapper()
		mapper.SetInputConnection(reader.GetOutputPort())
		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetRepresentationToSurface()
		actor.GetProperty().SetOpacity(opacity)

		self.reader = reader
		self.mapper = mapper
		self.actor = actor 

class MovingBodyPipeline:
	def __init__(self, fn="", time=0.0):

		reader = PvdReader(fn)
		pvd_data = reader.get_data(time)

		last = None

		if pvd_data.GetClassName() == "vtkMultiBlockDataSet":

			geoFilter = vtk.vtkCompositeDataGeometryFilter()
			geoFilter.SetInputDataObject(pvd_data)
			geoFilter.Update()
			last = geoFilter						

		ctf = vtk.vtkColorTransferFunction()
		ctf.SetColorSpaceToDiverging()

		colorx = np.linspace(0, 1, 256)
		colorrgb = cm.get_cmap("viridis", len(colorx))
		for x in colorx:
			r,g,b,a = colorrgb(x)
			ctf.AddRGBPoint(x, r, g, b)

		mapper = vtk.vtkPolyDataMapper()
		if last is None:
			mapper.SetInputDataObject(pvd_data)
		else:
			mapper.SetInputConnection(last.GetOutputPort())

		#mapper.SelectColorArray(variable_name)
		#mapper.SetColorModeToMapScalars()
		#mapper.ScalarVisibilityOn()
		#mapper.SetLookupTable(ctf)
		#mapper.UseLookupTableScalarRangeOn()
		#mapper.SetScalarModeToUsePointFieldData()
		#mapper.InterpolateScalarsBeforeMappingOn()
		#mapper.SetScalarModeToUseCellFieldData()

		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetRepresentationToSurface()

		self.reader = reader
		self.mapper = mapper
		self.actor = actor

class BlockDataPipeline:

	def __init__(self, fn="", time=0.0, doResample=True, color=None):

		reader = PvdReader(fn)
		pvd_data = reader.get_data(time)

		if pvd_data.GetClassName() == "vtkMultiBlockDataSet":

			geoFilter = vtk.vtkCompositeDataGeometryFilter()
			geoFilter.SetInputDataObject(pvd_data)
			geoFilter.Update()
			last = geoFilter

			if doResample:
				nx, ny, nz = GetNiceSamplingBounds(pvd_data)				
				resample = vtk.vtkResampleToImage()
				resample.UseInputBoundsOn()
				resample.SetSamplingDimensions(nx, ny, nz)
				resample.SetInputConnection(last.GetOutputPort())
				resample.Update()
				last = resample

		else:

			c2p = vtk.vtkCellDataToPointData()
			c2p.SetInputDataObject(pvd_data)
			last = c2p

		thr = vtk.vtkThreshold()			
		thr.SetInputConnection(last.GetOutputPort())
		thr.ThresholdByUpper(0.5)
		thr.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "Volume Fraction (-)")
		last = thr

		if color is None:
			color = vtk.vtkColorTransferFunction()
			color.SetColorSpaceToDiverging()

			colorx = np.linspace(0, 1, 256)
			colorrgb = cm.get_cmap("viridis", len(colorx))
			for x in colorx:
				r,g,b,a = colorrgb(x)
				color.AddRGBPoint(x, r, g, b)

		mapper = vtk.vtkDataSetMapper()
		mapper.SetInputConnection(last.GetOutputPort())
		#mapper.SelectColorArray(variable_name)
		#mapper.SetColorModeToMapScalars()
		mapper.ScalarVisibilityOn()
		mapper.SetLookupTable(color)
		#mapper.UseLookupTableScalarRangeOn()
		mapper.SetScalarModeToUsePointFieldData()
		mapper.InterpolateScalarsBeforeMappingOn()
		#mapper.SetScalarModeToUseCellFieldData()

		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetRepresentationToSurface()

		self.reader = reader
		self.mapper = mapper
		self.actor = actor

class MStarResults:
	def __init__(self, outdir="out", timegroup="Slice"):
		self.outdir = outdir
		self.output = os.path.join(outdir, "Output")
		self.stats = os.path.join(outdir, "Stats")
		self.timegroup = timegroup
		self.reload()
		self.ctf = {}
		self.opacity = {}
		self.variable = ""
		self.textprop = None
		self.show_statics = True
		self.time = 0

	def set_show_statics(self, val):
		self.show_statics = val

	def get_color(self):
		return self.get_scalar_bar(self.variable)
	
	def get_opacity(self):
		if self.variable in self.opacity:
			return self.opacity[self.variable]
		return 1.0

	def set_opacity(self, varname, xs, ys):
		opfunc = vtk.vtkPiecewiseFunction()
		for x,y in zip(xs, ys):
			opfunc.AddPoint(x, y)
		self.opacity[varname] = opfunc

	def set_variable(self, varname=""):
		self.variable = varname
		
	def set_ctf(self, varname="", cmap=None, mplnorm=None):
		ctf = vtk.vtkColorTransferFunction()		
				
		sampled = np.linspace(mplnorm.vmin, mplnorm.vmax, cmap.N)		
		for i in range(cmap.N):			
			r,g,b,a = cmap(mplnorm(sampled[i]))
			ctf.AddRGBPoint(sampled[i], r, g, b)

		self.ctf[varname] = ctf

	def set_scalar_bar(self, varname="", minlimit=0, maxlimit=1, colorscale="viridis"):
		ctf = vtk.vtkColorTransferFunction()		
		
		ncolors = 256
		sampled = np.linspace(minlimit, maxlimit, ncolors)
		norm = mpl.colors.Normalize(minlimit, maxlimit)		
		c = cm.get_cmap(colorscale, ncolors)
		for i in range(ncolors):			
			r,g,b,a = c(norm(sampled[i]))
			ctf.AddRGBPoint(sampled[i], r, g, b)

		self.ctf[varname] = ctf

	def get_scalar_bar(self, varname=""):
		if len(varname) == 0:
			return self.ctf[self.variable]

		if varname in self.ctf:
			return self.ctf[varname]
		return vtk.vtkColorTransferFunction()

	def reload(self):
		self.files = []
		for fn in glob.glob(os.path.join(self.output, "*.*")):
			if os.path.isfile(fn):				
				m = MStarFile(fn)
				logging.debug( str( m ))
				self.files.append(m)
		
	def print_summary(self):
		for f in self.files:
			print(f)
		
	def get_group_times(self, grpname=""):
		for p in self.files:
			if p.timegroup == grpname:
				r = PvdReader(p.filename)
				return r.get_times()
		return []
	
	def get_times(self):
		return self.get_group_times(self.timegroup)	

	def set_time(self, time):
		self.time = time

	def get_time(self):
		return self.time

	def get_dt(self):
		t = self.get_times()
		if len(t) >= 2:
			return t[1] - t[0]
		return 0

	def set_variable(self, varname="", vartype='POINT'):
		self.variable = varname
		self.variable_type = vartype

	def set_text_property(self, prop):
		self.textprop = prop

	def get_variable_ranges(self):
		# Get variable ranges
		# yields tuples of (variablename, min, max)

		vars = {}
		for f in self.files:
			if f.type in [ "X", "Y", "Z", "Volume" ]:
				r = f.data_ranges(self.time)
				if r:
					for ctype,cname,comp,minv,maxv in r:
						key = (cname, comp, ctype)
						#key = cname
						compmin = minv
						compmax = maxv

						if key in vars:
							compmin = min(vars[key][0], compmin)
							compmax = max(vars[key][1], compmax)
												
						vars[key] = (compmin, compmax)

		for k,v in vars.items():	
			#yield (k, v[0], v[1])
			yield (*k, *v)


	def add_scalar_bar(self, renderer):
		scalarBar = vtk.vtkScalarBarActor()
		scalarBar.SetLookupTable(self.ctf[self.variable])		
		scalarBar.SetNumberOfLabels(5)		

		if self.textprop is not None:
			scalarBar.AnnotationTextScalingOff()
			scalarBar.SetLabelTextProperty(self.textprop)
			scalarBar.SetAnnotationTextProperty(self.textprop)
			scalarBar.SetTitleTextProperty(self.textprop)

		renderer.AddActor2D(scalarBar)

	def plot(self, renderer):

		grps = [ self.timegroup ]
		if self.show_statics:
			grps.append("Static")

		for f in self.files:

			if f.timegroup in grps:
				f.add_pipeline(self, renderer)				

	def get_volume_pipeline(self):
		for f in self.files:
			if f.timegroup in [ self.timegroup ] and f.type == "Volume":
				return f.get_pipeline(self)

	def get_slice_pipelines(self, time):
		
		for f in self.files:
			if f.timegroup in  [ "Slice", "Static" ] :
				yield f.make_pipeline(time)


def mymax(x,y):
	if x > y:
		return x
	return y


def reset_camera_tight2(renderer, margin_factor=1.02, bounds=None):
	""" Resets camera so the content fit tightly within the window.

	Parameters
	----------
	margin_factor : float (optional)
		Margin added around the content. Default: 1.02.

	"""
	renderer.ComputeAspect()
	cam = renderer.GetActiveCamera()
	aspect = renderer.GetAspect()

	X1, X2, Y1, Y2, Z1, Z2 = renderer.ComputeVisiblePropBounds()

	if bounds is None:
		X1, X2, Y1, Y2, Z1, Z2   = renderer.ComputeVisiblePropBounds()
	else:
		X1, X2, Y1, Y2, Z1, Z2  = bounds

	width, height = X2-X1, Y2-Y1
	center = np.array((X1 + width/2., Y1 + height/2., 0))

	angle = np.pi*cam.GetViewAngle()/180.
	dist = max(width/aspect[0], height) / np.sin(angle/2.) / 2.
	position = center + np.array((0, 0, dist*margin_factor))

	cam.SetViewUp(0, 1, 0)
	cam.SetPosition(*position)
	cam.SetFocalPoint(*center)
	renderer.ResetCameraClippingRange(X1, X2, Y1, Y2, Z1, Z2)

	parallelScale = max(width/aspect[0], height) / 2.
	cam.SetParallelScale(parallelScale*margin_factor)

def create_camera_tight(eye_index=0, eye_flip=1, up_index=1, bounds=None):
	""" 
	Parameters
	----------
	eye_index: 0, 1, 2  for x y or z
	eye_flip: set negative for flip direction
	up_index: 0, 1 2  which way is up?

	"""	

	camera = vtk.vtkCamera()
	padding_factor = 1.1

	directions = [0, 1, 2]
	directions.remove(eye_index)
	directions.remove(up_index)
	width_index = directions[0]

	if bounds is None:
		raise ValueError("bounds must be provided")
	else:
		xmn,xmx,ymn,ymx,zmn,zmx = bounds

	xl = xmx - xmn
	yl = ymx - ymn
	zl = zmx - zmn
	l = [xl, yl, zl]
	xc = xmn + xl * 0.5
	yc = ymn + yl * 0.5
	zc = zmn + zl * 0.5

	tanangle = math.tan(camera.GetViewAngle() * math.pi / 180.0 / 2.0)
	xeye = xl * padding_factor / (2 * tanangle)
	yeye = yl * padding_factor / (2 * tanangle)
	zeye = zl * padding_factor / (2 * tanangle)
	eye_d = [ xeye, yeye, zeye ]

	aspect_ratio = 1.0 
	needed_height = aspect_ratio * l[width_index]

	eye = [ xc, yc, zc ]
	up = [0,0,0]
	height = mymax(needed_height, l[up_index]) * 0.5
	up[up_index] = 1
	eye[eye_index] += max(eye_d) * eye_flip	

	camera.SetParallelProjection(True)	
	camera.SetParallelScale(height)		
	camera.SetViewUp(up)
	camera.SetPosition(eye)
	camera.SetFocalPoint(xc,yc,zc)

	return camera

def reset_camera_tight(renderer, eye_index=0, eye_flip=1, up_index=1, bounds=None):
	""" Resets camera so the content fit tightly within the window.

	Parameters
	----------
	eye_index: 0, 1, 2  for x y or z
	eye_flip: set negative for flip direction
	up_index: 0, 1 2  which way is up?

	"""	
	camera = renderer.GetActiveCamera()
	aspect = renderer.GetAspect()	
	padding_factor = 1.1

	directions = [0, 1, 2]
	directions.remove(eye_index)
	directions.remove(up_index)
	width_index = directions[0]

	if bounds is None:
		xmn,xmx,ymn,ymx,zmn,zmx  = renderer.ComputeVisiblePropBounds()
	else:
		xmn,xmx,ymn,ymx,zmn,zmx = bounds

	xl = xmx - xmn
	yl = ymx - ymn
	zl = zmx - zmn
	l = [xl, yl, zl]
	#print (xmn,xmx,ymn,ymx,zmn,zmx)
	#print (l)

	xc = xmn + xl * 0.5
	yc = ymn + yl * 0.5
	zc = zmn + zl * 0.5

	tanangle = math.tan(camera.GetViewAngle() * math.pi / 180.0 / 2.0)
	xeye = xl * padding_factor / (2 * tanangle)
	yeye = yl * padding_factor / (2 * tanangle)
	zeye = zl * padding_factor / (2 * tanangle)
	eye_d = [ xeye, yeye, zeye ]

	aspect_ratio = 1.0 #float(view.ViewSize[1]) / float(view.ViewSize[0])
	needed_height = aspect_ratio * l[width_index]

	eye = [ xc, yc, zc ]
	up = [0,0,0]
	#print (needed_height, l, up_index, l[up_index])
	height = mymax(needed_height, l[up_index]) * 0.5

	up[up_index] = 1
	eye[eye_index] += max(eye_d) * eye_flip

	#print ("-- Updating camera: ", "height=", height, "up=", up, "pos=", eye, "focal=", (xc,yc,zc))

	camera.SetParallelProjection(True)	
	camera.SetParallelScale(height)		
	camera.SetViewUp(up)
	camera.SetPosition(eye)
	camera.SetFocalPoint(xc,yc,zc)

def dumpActor2d(a):
	print("GetPosition()=", a.GetPosition())
	print("GetPosition2()=", a.GetPosition2())
	print("H=", a.GetHeight(), "W=", a.GetWidth())

def create_scalarbar_image(ctf, size=(100,100), textprop=None):
	colors = vtk.vtkNamedColors()

	scalarBar = vtk.vtkScalarBarActor()
	scalarBar.SetLookupTable(ctf)		
	scalarBar.SetNumberOfLabels(5)	
	scalarBar.SetTitleTextProperty(textprop)
	scalarBar.SetLabelTextProperty(textprop)
	scalarBar.SetAnnotationTextProperty(textprop)	
	scalarBar.SetPosition(0, 0.01)
	scalarBar.SetWidth(0.95)
	scalarBar.SetHeight(0.95)

	renderer = vtk.vtkRenderer()	
	renderer.SetBackground(colors.GetColor3d("White"))    	
	renderer.AddActor2D(scalarBar)	

	renderWindow = vtk.vtkRenderWindow()
	renderWindow.AddRenderer(renderer)
	renderWindow.SetOffScreenRendering(1)
	renderWindow.SetSize( int(size[0]/2), int(size[1]/2) )
	renderWindow.SetMultiSamples(4)
	renderWindow.Render()

	windowto_image_filter = vtk.vtkWindowToImageFilter()
	windowto_image_filter.SetInput(renderWindow)
	windowto_image_filter.SetScale(2)	

	writer = vtk.vtkPNGWriter()
	writer.SetInputConnection(windowto_image_filter.GetOutputPort())
	writer.WriteToMemoryOn()
	writer.Write()

	buf = io.BytesIO()
	buf.write(writer.GetResult())
	buf.seek(0)

	return buf

def f2icolor(x=1.0):
	return int( x * 255 )

def color2int(rgb=(0.0,0.0,0.0)):
	return ( f2icolor( rgb[0]), f2icolor( rgb[1] ), f2icolor( rgb[2] ))

def draw_color_bar(ctf=None, opacityFunc=None, size=(10,100), nticks=5, min=0.0, max=1.0, fontsize=16):
	img = Image.new("RGBA", size=size)	

	font = ImageFont.truetype("arial.ttf", fontsize)
	dr = ImageDraw.Draw(img)

	barwidth = 0.3333

	w = size[0] * barwidth
	n = size[1]
	for i in range(size[1]):
		x = min + i * (max - min) / n
		rgbflt = [ 0.0, 0.0, 0.0 ]
		ctf.GetColor(x, rgbflt)
		rgb = color2int(rgbflt)
		opacity =  f2icolor ( 1.0 )

		if opacityFunc is not None:
			opacity = f2icolor (  opacityFunc.GetValue(x) )

		rgba = (rgb[0], rgb[1], rgb[2], opacity)
		dr.line([ (0, n-i), (w, n-i )  ], fill=rgba )

	anchors = [ "lm" ] * nticks
	anchors[0] = "ls"
	anchors[-1] = "lt"
	values = np.linspace(min, max, nticks)

	for i in range(nticks):
		y = n - i * (n / (nticks - 1))
		val = "{0:.3g}".format( values[i] )
		dr.text(xy=(w+1, y), text=val, anchor=anchors[i], font=font, fill="black")

	#dr.text( (0,h), title , anchor='la', font=font )
	return img

def make_frames(caseDir="", timegroup="", variables=[]):
	"""
	"""

	results = MStarResults(timegroup=timegroup, outdir=os.path.join(caseDir, "out"))

	title = os.path.basename(caseDir)

	#  Output directory to place all data and images
	output_dir = os.path.join(caseDir, "out/Processed")

	# Define variable names, min, max contour values
	#variables = variables

	# Get all variables, using auto-computed ranges based on last available time step
	#variables = results.get_variable_ranges()

	# (name, eye direction, up direction, flip)
	views = [
		("front", 0, 1, False),
		#("back", 0, 1, True),
		("top", 1, 2, False),
		#("bottom", 1, 2, True),
		#("side_1", 2, 1, False),
		("side_2", 2, 1, True),
	]

	img_size = (500,500)

	colors = vtk.vtkNamedColors()

	textprop = vtk.vtkTextProperty()
	textprop.SetFontSize(48)
	textprop.SetFontFamilyToArial()
	textprop.ItalicOff()
	textprop.ShadowOff()
	textprop.BoldOff()
	textprop.SetLineSpacing(1.1)
	textprop.SetColor(colors.GetColor3d("Black"))

	results.set_text_property(textprop)

	for variable_name,vmin,vmax,cmapname in variables:

		var_name = NiceVariableName(variable_name)
		var_out_dir = os.path.join(output_dir, var_name)	
		os.makedirs(var_out_dir, exist_ok=True)
					
		results.set_scalar_bar(variable_name, vmin, vmax, cmapname)
		results.set_opacity(variable_name, [vmin, vmax], [0, 1.0])			
		results.set_variable(variable_name)		
		results.set_show_statics(False)

		#scalar_bar_img = Image.open( create_scalarbar_image(results.get_scalar_bar(), (50,img_size[1]) , textprop))
		scalar_bar_img_2 = draw_color_bar(results.get_scalar_bar(), opacityFunc=results.get_opacity(), size=(75, img_size[1]), min=vmin, max=vmax)	

		# Render the frames directly into a video file
		img_index = 0
		
		for t in results.get_times():
			
			camera = vtk.vtkCamera()
			camera.SetPosition(1, 1, 1)
			camera.SetFocalPoint(0, 0, 0)

			renderer = vtk.vtkRenderer()
			text_annotation = "  ".join( ( title, variable_name, "t = {0}".format(t) ) )
			#textMapperL.SetInput("\n".join( ( title, variable_name, "t={0}".format(t) ) ))
			renderer.SetBackground(colors.GetColor3d("White"))    
			#renderer.AddActor2D(textActorL)			
			renderer.SetActiveCamera(camera)
			
			results.set_time(t)
			results.plot(renderer)		

			axes = vtk.vtkAxesActor()

			renderWindow = vtk.vtkRenderWindow()
			renderWindow.AddRenderer(renderer)
			renderWindow.SetOffScreenRendering(1)
			renderWindow.SetSize( int(img_size[0]/2), int(img_size[1]/2) )
			renderWindow.SetMultiSamples(4)

			# An interactor
			renderWindowInteractor = vtk.vtkRenderWindowInteractor()
			renderWindowInteractor.SetRenderWindow(renderWindow)

			# lower left axis orientation
			widget = vtk.vtkOrientationMarkerWidget()
			rgba = [0] * 4
			colors.GetColor('Carrot', rgba)
			widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
			widget.SetOrientationMarker(axes)
			widget.SetInteractor(renderWindowInteractor)
			widget.SetViewport(0.0, 0.0, 0.1, 0.1)
			widget.SetEnabled(1)			
			
			for v in views:
				view_name = v[0]
				view_eye = v[1]
				view_up = v[2]
				view_flip = v[3]

				renderWindow.Render()

				windowto_image_filter = vtk.vtkWindowToImageFilter()
				windowto_image_filter.SetInput(renderWindow)
				windowto_image_filter.SetScale(2)

				reset_camera_tight(renderer, eye_index=view_eye, up_index=view_up)

				writer = vtk.vtkPNGWriter()
				writer.SetInputConnection(windowto_image_filter.GetOutputPort())
				writer.WriteToMemoryOn()
				writer.Write()

				buf = io.BytesIO()
				buf.write(writer.GetResult())
				buf.seek(0)

				# Read data into PIL image buffer
				vtk_img = Image.open(buf)
				
				w = vtk_img.size[0]
				h = vtk_img.size[1]
				
				total_w = w + scalar_bar_img_2.size[0]
				total_h = h + 20

				# Stack VTK image with scalar bar and annotation in a new image		
				com_img = Image.new("RGBA", size=(total_w, total_h), color=(255,255,255))
				com_img.paste(vtk_img, (0,0) )
				com_img.alpha_composite(scalar_bar_img_2.copy(), dest=(w,0))

				font = ImageFont.truetype("arial.ttf", 15)
				dr = ImageDraw.Draw(com_img)

				dr.text( (0,h), title , anchor='la', font=font, fill="black" )
				dr.text( (total_w/2,h), variable_name , anchor='ma', font=font, fill="black" )
				dr.text( (total_w,h), "t = {0}".format(t) , anchor='ra', font=font , fill="black")
							
				fn = "{name}_{view_name}_{n:05}.png".format(name=var_name, n=img_index, view_name=view_name)
				fn = os.path.join(var_out_dir, fn)		
				print ("-- Rendering time: ", t, "-->", fn)
				com_img.save(fn)

			img_index += 1
		
		
		
		
	