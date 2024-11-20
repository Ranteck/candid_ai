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
				FileReadTool(root_dir='./data')  # Especifica el directorio raíz
			],
			instructions="""
			Si no puedes acceder o leer el CV correctamente, debes:
			1. Indicar explícitamente que no pudiste acceder a la información
			2. NO generar o inventar información que no puedas verificar
			3. Sugerir alternativas para obtener la información necesaria
			"""
		)

	@agent
	def position_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['position_expert'],
			verbose=True,
			tools=[
				FileReadTool(root_dir='./data'),    # Para archivos generales
				TXTSearchTool(),                    # Para búsqueda en TXT
				PDFSearchTool(),                    # Para búsqueda en PDF
				DOCXSearchTool(),                   # Para búsqueda en DOCX
				SerperDevTool(),
				WebsiteSearchTool()
			]
		)

	@agent
	def profile_matcher(self) -> Agent:
		return Agent(
			config=self.agents_config['profile_matcher'],
			verbose=True,
			tools=[SerperDevTool()],
			instructions="""
			Al realizar el matching:
			1. Usar SOLO información verificada de los análisis previos
			2. Si falta información, indicarlo explícitamente
			3. NO asumir ni inventar datos faltantes
			4. Calcular porcentajes solo con información confirmada
			5. Indicar claramente qué aspectos no pudieron evaluarse por falta de datos
			"""
		)

	@agent
	def linkedin_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['linkedin_scraper'],
			verbose=True,
			tools=[
				FileReadTool(root_dir='./data'),  # Para leer datos de LinkedIn guardados localmente
				SerperDevTool()  # Para búsquedas generales
			],
			instructions="""
			Si no puedes acceder al perfil de LinkedIn:
			1. Reportar explícitamente la falla de acceso
			2. NO inventar información del perfil
			3. Sugerir métodos alternativos para obtener la información
			"""
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