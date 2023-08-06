

from .mstarvtk import PvdReader
import pyarrow as pa
import vtk
from vtk.numpy_interface import dataset_adapter
import polars as po
import numpy as np
import os

parquet_compression = "snappy"

def convert(pvdfn="", single_file="", separate_files_dir="", output_format="", id_select=[]):
	"""
	Convert a particles pvd file into a pyarrow table
	"""

	pvdReader = PvdReader(pvdfn)

	single_obj = None
	do_concat_file = len(single_file) > 0
	do_sep_files = len(separate_files_dir) > 0

	for time in pvdReader.get_times():
		for fn in pvdReader .get_filenames(time):

			reader = vtk.vtkXMLPolyDataReader()
			reader.SetFileName(fn)
			reader.Update()
			
			dataobj = dataset_adapter.WrapDataObject(reader.GetOutput())
			
			datad = {}
			pointname = [ "x", "y", "z" ]
			nrows = 0
			for compIndex in range(0, dataobj.Points.shape[1]):
				nrows = dataobj.Points.shape[0]
				datad[pointname[compIndex]] = pa.array(dataobj.Points[:,compIndex])

			for key in dataobj.PointData.keys():

				dataarr = dataobj.PointData[key]
				if len(dataarr.shape) == 1:
					datad[key] = pa.array(dataarr)
				else:
					for compIndex in range(0, dataarr.shape[1]):
						datad[key + " " + str(compIndex)] = pa.array(dataarr[:,compIndex])
					
			datad["time"] = np.repeat(time, nrows)
			df = po.DataFrame(datad)
			
			if id_select is not None and len(id_select):
				df = df.filter(po.col("ID").is_in(id_select))

			if do_concat_file:
				if single_obj is None:
					single_obj = df
				else:
					single_obj = po.concat([single_obj, df], how="vertical")

			if do_sep_files:
				if output_format.lower() == "csv":
					out_fn = os.path.join(separate_files_dir, "time_%g.csv" % time)
					os.makedirs(os.path.dirname(out_fn), exist_ok=True)
					df.write_csv(out_fn)
				elif output_format.lower() == "parquet":
					out_fn = os.path.join(separate_files_dir, "time_%g.parquet" % time)
					os.makedirs(os.path.dirname(out_fn), exist_ok=True)
					df.write_parquet(out_fn, compression=parquet_compression)


			#print (df.head())

	if single_obj is not None:
		if os.path.splitext(single_file)[1].lower() == ".csv":
			single_obj.write_csv(single_file)
		elif os.path.splitext(single_file)[1].lower() == ".parquet":
			single_obj.write_parquet(single_file, compression=parquet_compression)

def cli():
	
	import argparse
	import glob

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input-dir", default="out", help="where is solver output located?")
	parser.add_argument("-o", "--output-dir", default="out/Processed", help="where output files are written")
	parser.add_argument("--format", default='csv', help="output file format", choices=["csv", "parquet"])
	parser.add_argument("--freq", default='slice', help="time frequency selection", choices=["slice", "volume", "all"])
	parser.add_argument("--separate", default=False, action='store_true', help="store files for each time. Note that a new sub-directory will be created for each particle set")
	parser.add_argument("-id", "--select-id", action='append', help="Select particle by IDs during conversion")
	clargs = parser.parse_args()

	if clargs.select_id is not None and len(clargs.select_id) > 0:
		clargs.select_id = list(map(int, clargs.select_id))

	fileglobs = []

	if clargs.freq in [ "volume", "all"] :
		fileglobs.append("VolumeParticles_*.pvd")
	if clargs.freq in [ "slice", "all"] :
		fileglobs.append("SliceParticles_*.pvd")

	for fglob in fileglobs:
		for fn in glob.glob(os.path.join(clargs.input_dir, "Output", fglob)):

			single_fn = os.path.join(clargs.output_dir, os.path.splitext(os.path.basename(fn))[0])
			separate_dir = ""
			if clargs.separate:
				separate_dir = single_fn
				single_fn = ""		
			else:
				single_fn += "." + clargs.format

			print("-- Processing file:", fn)
			convert(fn, 
							single_file=single_fn, 
							separate_files_dir=separate_dir, 
							output_format=clargs.format, 
							id_select=clargs.select_id)


if __name__ == "__main__":

	convert("out/Output/SliceParticles_Particles.pvd", 
			single_file="out/Processed/particledata.parquet", 
			separate_files_dir="out/Processed/ParticleData/", 
			output_format="parquet")