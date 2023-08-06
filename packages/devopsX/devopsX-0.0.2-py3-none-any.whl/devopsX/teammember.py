import logging
logging.basicConfig(level=logging.INFO)
from devopsX.abstractdevops import AbstractDevOps

# Represent a team member
class TeamMember():

	def __init__(self,personal_access_token, organization_url):
		super(TeamMember,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	
	def get_team_members(self, project_id, team_id):
		return self.core_client.get_team_members_with_extended_properties(project_id=project_id,team_id=team_id)
    
	def get_all_team_members_project(self):
		projects = self.core_client.get_projects()
		all_team_members = []
        
		for project in projects:
			teams = self.core_client.get_teams(project.id)
			for team in teams:
				team_members = self.core_client.get_team_members(project.id,team.id)
				for team_member in team_members:
					team_member.additional_properties["team"] = team.id
					all_team_members.append(team_member)
		
		return all_team_members