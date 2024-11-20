import os
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, SerperDevTool, PDFSearchTool

@CrewBase
class EstudioProyectoCrew():
	"""Crew para análisis y matching de perfiles profesionales"""

	def __init__(self):
		try:
			config_path = os.path.join(os.path.dirname(__file__), 'config')
			
			# Verificar que el directorio existe
			if not os.path.exists(config_path):
				raise FileNotFoundError(f"Directory not found: {config_path}")
			
			# Cargar configuraciones
			agents_path = os.path.join(config_path, 'agents.yaml')
			tasks_path = os.path.join(config_path, 'tasks.yaml')
			
			for path in [agents_path, tasks_path]:
				if not os.path.exists(path):
					raise FileNotFoundError(f"Configuration file not found: {path}")
			
			with open(agents_path, 'r', encoding='utf-8') as f:
				self.agents_config = yaml.safe_load(f)
				
			with open(tasks_path, 'r', encoding='utf-8') as f:
				self.tasks_config = yaml.safe_load(f)
				
		except Exception as e:
			raise Exception(f"Error loading configurations: {str(e)}")

	@agent
	def cv_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['cv_analyzer'],
			verbose=True,
			tools=[
				PDFSearchTool(root_dir='./data/cv.pdf', mode='rb'),
				#FileReadTool(root_dir='./data/cv.pdf', mode='rb')
			]
		)

	@agent
	def position_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['position_expert'],
			verbose=True,
			tools=[FileReadTool(root_dir='./data'), SerperDevTool()]
		)

	@agent
	def profile_matcher(self) -> Agent:
		return Agent(
			config=self.agents_config['profile_matcher'],
			verbose=True,
			tools=[SerperDevTool()]
		)

	@agent
	def linkedin_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['linkedin_scraper'],
			verbose=True,
			tools=[FileReadTool(root_dir='./data'), SerperDevTool()]
		)

	@task
	def cv_analysis_task(self) -> Task:
		return Task(config=self.tasks_config['cv_analysis_task'])

	@task
	def linkedin_analysis_task(self) -> Task:
		return Task(config=self.tasks_config['linkedin_analysis_task'])

	@task
	def position_analysis_task(self) -> Task:
		return Task(config=self.tasks_config['position_analysis_task'])

	@task
	def matching_task(self) -> Task:
		return Task(config=self.tasks_config['matching_task'])

	@crew
	def crew(self) -> Crew:
		"""Crea el crew de análisis de perfiles"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			planning=True
		)