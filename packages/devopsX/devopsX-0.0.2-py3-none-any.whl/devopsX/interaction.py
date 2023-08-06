import logging
logging.basicConfig(level=logging.INFO)

from devopsX.abstractdevops import AbstractDevOps

# Represent the time-box in a project 
class Interaction(AbstractDevOps):
	def __init__(self,personal_access_token, organization_url):
		super(Interaction,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
		

	def get_interactions(self, project, team):
		try:
			logging.info("Start function: get_work_items")
						
			logging.info("End function: get_work_items")
			team_context = self.create_team_context(project, team)
			return self.work_client.get_team_iterations(team_context)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)