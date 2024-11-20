from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    FileReadTool,          # Para leer CVs en diferentes formatos
    SerperDevTool,         # Para búsquedas generales
    WebsiteSearchTool,     # Para análisis de sitios web específicos
    TXTSearchTool,         # Para búsqueda en TXT
    PDFSearchTool,         # Para búsqueda en PDF
    DOCXSearchTool,        # Para búsqueda en DOCX
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
				PDFSearchTool(),
				FileReadTool(root_dir='./data')
			]
		)

	@agent
	def position_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['position_expert'],
			verbose=True,
			tools=[
				FileReadTool(root_dir='./data'),
				SerperDevTool()
			]
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
			tools=[
				FileReadTool(root_dir='./data'),
				SerperDevTool()
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
			context=[self.cv_analysis_task()]
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
				self.cv_analysis_task(),
				self.linkedin_analysis_task(),
				self.position_analysis_task()
			],
			output_file='./output/matching_report.md',
			expected_output="""
			El reporte debe:
			1. Indicar explícitamente qué información no pudo verificarse
			2. Calcular porcentajes solo con datos confirmados
			3. Separar claramente hechos verificados vs información no disponible
			4. Incluir disclaimers sobre limitaciones del análisis
			5. Sugerir pasos adicionales para obtener información faltante
			"""
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