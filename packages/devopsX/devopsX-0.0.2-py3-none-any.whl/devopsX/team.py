import logging
logging.basicConfig(level=logging.INFO)
from devopsX.abstractdevops import AbstractDevOps
# Represents the teams in a project
class Team(AbstractDevOps):
	
	def __init__(self,personal_access_token, organization_url):
		super(Team,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	
	def get_teams(self, project_id):
		return self.core_client.get_teams(project_id)
