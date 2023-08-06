
import sys
import os
import glob

from PySide6 import QtCore, QtWidgets, QtGui, QtCharts
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QChart, QChartView, QLineSeries
import pandas as pd


class ChartData:
	def __init__(self):
		self.chart = None
		self.xAxis = None	
		self.yAxis = None	
		self.chartView = None			



class MyWidget(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()

		main = QtWidgets.QWidget(self)
		layout = QtWidgets.QVBoxLayout(self)

		btnRefresh = QtWidgets.QPushButton("&Refresh")
		btnRefresh.clicked.connect(self.onRefreshClicked)

		self.statFileTabs = QtWidgets.QTabWidget(self)
		self.lastTab = 0

		layout.addWidget(btnRefresh)		
		layout.addWidget(self.statFileTabs)

		self.charts = { }
		self.tabs = { }

		main.setLayout(layout)	
		self.resize(1000, 800)		
		self.setCentralWidget(main)		
		self.initializeCharts()
		self.refreshStatsData()

	def onRefreshClicked(self):
		self.refreshStatsData()

	def refreshStatsData(self):
		for fn in glob.glob("out/Stats/*.txt"):			
			data0 = pd.read_csv(fn, sep='\t', index_col=0)			
			for col in data0:
				chartKey = fn + ":" + col

				series = QLineSeries()
				for index,value in data0[col].iteritems():
					series.append(index, value)

				cd = self.charts[chartKey]
				cd.chart.removeAllSeries()
				cd.chart.addSeries(series)
				cd.xAxis.setRange(data0[col].index.array.min(), data0[col].index.array.max())	
				cd.yAxis.setRange(data0[col].array.min(), data0[col].array.max())	
				series.attachAxis(cd.xAxis)
				series.attachAxis(cd.yAxis)

	def initializeCharts(self):
		
		for fn in glob.glob("out/Stats/*.txt"):
			scrollArea = QtWidgets.QScrollArea(self)
			tabPage = QtWidgets.QWidget(self)
			layout = QtWidgets.QVBoxLayout(self)
			data0 = pd.read_csv(fn, sep='\t', index_col=0)
			scrollArea.setWidgetResizable(True)

			for col in data0:
				chartKey = fn + ":" + col

				#series = QLineSeries()
				#for index,value in data0[col].iteritems():
				#	series.append(index, value)

				chart = QChart()
				chart.legend().hide()
				chart.setTitle(col)
				
				xAxis = QtCharts.QValueAxis()
				yAxis = QtCharts.QValueAxis()
				
				xAxis.setTitleText(data0.index.name)
				yAxis.setTitleText(col)

				xAxis.setLabelFormat("%g")
				yAxis.setLabelFormat("%g")

				xAxis.setTickCount(5)
				yAxis.setTickCount(5)
				
				chart.addAxis(xAxis, Qt.AlignBottom)
				chart.addAxis(yAxis, Qt.AlignLeft)						

				chartView = QChartView(chart)
				chartView.setRenderHint(QPainter.Antialiasing)				
				chartView.setMinimumSize(100, 300)
				chartView.setMaximumSize(1000000, 300)
				
				cd = ChartData()
				cd.chart = chart
				cd.xAxis = xAxis
				cd.yAxis = yAxis
				cd.chartView = chartView

				self.charts[chartKey] = cd
				
				layout.addWidget(chartView)
			
			tabPage.setLayout(layout)
			scrollArea.setWidget(tabPage)
			self.statFileTabs.addTab(scrollArea, os.path.basename(fn))


def run():
	app = QtWidgets.QApplication([])

	widget = MyWidget()    
	#widget.setWindowState(QtCore.Qt.WindowMaximized)
	widget.show()
	
	sys.exit(app.exec())

if __name__ == "__main__":
	
	run()
	