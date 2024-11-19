from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    FileReadTool,          # Para leer CVs en diferentes formatos
    SerperDevTool,         # Para búsquedas generales
    WebsiteSearchTool,     # Para análisis de sitios web específicos
)

@CrewBase
class EstudioProyectoCrew():
	"""Crew para análisis y matching de perfiles profesionales"""

	@agent
	def cv_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['cv_analyzer'],
			verbose=True,
			tools=[
				FileReadTool(root_dir='./data')  # Especifica el directorio raíz
			]
		)

	@agent
	def position_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['position_expert'],
			verbose=True,
			tools=[
				SerperDevTool(),      # Para investigar tendencias del mercado
				WebsiteSearchTool()    # Para analizar descripciones de puestos similares
			]
		)

	@agent
	def profile_matcher(self) -> Agent:
		return Agent(
			config=self.agents_config['profile_matcher'],
			verbose=True,
			tools=[SerperDevTool()]  # Para validar skills y tecnologías
		)

	@agent
	def linkedin_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['linkedin_scraper'],
			verbose=True,
			tools=[
				SerperDevTool(),       # Para búsquedas de perfiles
				WebsiteSearchTool()     # Para análisis de sitios web
			]
		)

	@task
	def cv_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['cv_analysis_task']
		)

	@task
	def linkedin_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['linkedin_analysis_task'],
			context=[self.cv_analysis_task]
		)

	@task
	def position_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['position_analysis_task']
		)

	@task
	def matching_task(self) -> Task:
		return Task(
			config=self.tasks_config['matching_task'],
			context=[
				self.cv_analysis_task,
				self.linkedin_analysis_task,
				self.position_analysis_task
			],
			output_file='./output/matching_report.md'
		)

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