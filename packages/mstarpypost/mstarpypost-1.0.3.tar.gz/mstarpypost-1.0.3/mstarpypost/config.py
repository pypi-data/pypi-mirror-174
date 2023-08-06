


from typing import Optional
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from enum import Enum, IntEnum


def ToFloatVec(str="", delim=","):
	if str is None:
		return tuple()
	return tuple(map(float, str.split(delim)))

def ToIntVec(str="", delim=","):
	if str is None:
		return tuple()
	return tuple(map(int, str.split(delim)))

def ToColorVec(str="", delim=","):
	return [ max(0.0, min(1.0, v / 255.0)) for v in ToFloatVec(str, delim) ]

def ToBool(v):
	if isinstance(v, bool):
		return v
	elif isinstance(v, str):
		return v.lower() in ("yes", "true", "t", "1")
	elif isinstance(v, int):
		return v != 0
	
	raise ValueError("Cannot parse value to boolean: " + str(v))

def smootherStep(e0, e1, x):
	x = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
	return x * x * x * (x * (x * 6 - 15) + 10)

class VTKVariable(BaseModel):
	name: str
	min: float
	max: float
	component: int = 0
	display_name: str = ""
	color_scale: str = "magma"
	discrete: bool = False
	discrete_n: int = 12

def ColorInt2Float(v):
	return max(0.0, min(1.0, v / 255.0))

class RGBIntValue(BaseModel):
	red: int = Field(0, ge=0, le=255)
	green: int = Field(0, ge=0, le=255)
	blue: int = Field(0, ge=0, le=255)

	def ToFloatValue(self) -> tuple[float, float, float]:
		return (ColorInt2Float(self.red), ColorInt2Float(self.green), ColorInt2Float(self.blue))

class OpacityFuncType(str, Enum):
	smooth = 'smooth'
	ramp = 'ramp'
	constant = 'constant'

class DirEnum(str, Enum):
	xn = 'xn'
	xp = 'xp'
	yn = 'yn'
	yp = 'yp'
	zn = 'zn'
	zp = 'zp'
		
	def direction(self):		
			m = { DirEnum.xn:0, 
					DirEnum.xp:0, 
					DirEnum.yn:1, 
					DirEnum.yp:1, 
					DirEnum.zn:2, 
					DirEnum.zp:2 }
			return m[self]
		
	def sign(self):		
		m = { DirEnum.xn:-1, 
				DirEnum.xp:1, 
				DirEnum.yn:-1, 
				DirEnum.yp:1, 
				DirEnum.zn:-1, 
				DirEnum.zp:1 }
		return m[self]

class TimesEnum(str, Enum):
	all = 'all'
	last = 'last'

class OpacityFunction(BaseModel):
	type: OpacityFuncType = OpacityFuncType.smooth
	start: float = Field(0.0, ge=0.0, le=1.0)
	end: float = Field(1.0, ge=0.0, le=1.0)
	constant_value: float = Field(1.0, ge=0.0, le=1.0)

class BlockDataPipeline(BaseModel):
	file: str
	color_by: str

class MovingBodyPipeline(BaseModel):
	file: str
	color_by: str

class ParticlesPipeline(BaseModel):
	file: str
	color_by: str

class StaticStlPipeline(BaseModel):
	file: str
	solid_color: RGBIntValue
	solid_opacity: float = Field(..., ge=0.0, le=1.0)

class VolumePipeline(BaseModel):
	file: str
	color_by: str
	opacity_function: OpacityFunction = OpacityFunction()

class Watermark(BaseModel):
	filename: str
	location: str = "ul"
	alpha: float = 0.25


class ViewStandard(BaseModel):	
	name: str
	eye_side: DirEnum
	up: DirEnum	


class ViewCustom(BaseModel):
	name: str
	eye_position: tuple[float, float, float]
	look_at: tuple[float, float, float]
	up: tuple[float, float, float]
	eye_position: tuple[float, float, float]
	fit: bool = False

class VideoOption(BaseModel):
	enabled: bool = False
	speed: float = Field(1.0, gt=0.0)
	quality: int = Field(20, gt=1, lt=30)

class VTKPlotConfig(BaseModel):

	name: str
	size_x: int = Field(1024, ge=10)
	size_y: int = Field(1024, ge=10)
	image_output: bool = True
	time: TimesEnum = TimesEnum.all
	background_color: RGBIntValue = RGBIntValue()

	variables: list[VTKVariable] = []
	block_pipelines: list[BlockDataPipeline] = list()
	moving_pipelines: list[MovingBodyPipeline]=  list()
	particle_pipelines: list[ParticlesPipeline]=  list()
	stl_pipelines: list[StaticStlPipeline]=  list()
	volume_pipelines: list[VolumePipeline]=  list()
	
	standard_views: list[ViewStandard]
	custom_views: list[ViewCustom] = []

	watermarks: list[Watermark] = []
	video_options: VideoOption = VideoOption()

class PlotAxisEnum(str, Enum):
	linear = "linear"
	log10 = "log10"


class StatPlotDataSeries(BaseModel):

	filename: str
	x: Optional[str]
	y: Optional[str]
	x_column: Optional[int] = 0
	y_column: Optional[int] = 0
	line_color: Optional[RGBIntValue]
	line_style: Optional[str] = "solid"
	line_width: Optional[float]
	name: Optional[str]

class LegendLocEnum(str, Enum):
	best = "best"
	upper_left = "upper left"
	upper_right = "upper right"
	lower_left = "lower left"
	lower_right = "lower right"
	upper_center = "upper center"
	lower_center = "lower center"
	center_left = "center left"
	center_right = "center right"
	center = "center"

class StatPlotStyle(BaseModel):
	name: Optional[str]
	size: Optional[tuple[float, float]]
	style: Optional[list[str]]
	legend_location: Optional[LegendLocEnum]

	def override(self, rhs):		
		if rhs is None:
			return self
		s = self.copy()
		if rhs.size is not None:
			s.size = rhs.size
		if rhs.style is not None:
			s.style = rhs.style
		if rhs.legend_location is not None:
			s.legend_location = rhs.legend_location
		return s


class StatPlot(BaseModel):

	name: str
	y_title: Optional[str]
	x_title: Optional[str]
	chart_title: Optional[str]
	x_lim: Optional[tuple[float, float]]
	y_lim: Optional[tuple[float, float]]	
	y_axis: PlotAxisEnum = PlotAxisEnum.linear
	series: list[StatPlotDataSeries]
	style: Optional[StatPlotStyle]


class ResultStatImage(BaseModel):

	name: str
	config: StatPlot
	image_filename: str

class ResultAutoStatImage(BaseModel):

	name: str
	stat_filename: str
	image_filename: str

class ResultVtkImage(BaseModel):
	time: float
	image_filename: str
	config: VTKPlotConfig
	view: str	

class ResultsProcessed(BaseModel):
	custom_stat_plots: list[ResultStatImage] = []
	auto_stat_plots: list[ResultAutoStatImage] = []
	vtk_images: list[ResultVtkImage] = []

class BatchPostConfig(BaseModel):
	plots: list[VTKPlotConfig] = None		
	default_stat_plot_style: Optional[StatPlotStyle]
	stat_plots: list[StatPlot] = None
	auto_stat_plots: bool = False
	auto_pdf_report: bool = False

class AutoReportConfig(BaseModel):
	title: str
	results: ResultsProcessed	
	model_tree_filename: Optional[str]

