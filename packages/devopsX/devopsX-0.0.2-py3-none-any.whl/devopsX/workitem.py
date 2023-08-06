import logging
logging.basicConfig(level=logging.INFO)
from devopsX.abstractdevops import AbstractDevOps
from azure.devops.v5_1.work_item_tracking import WorkItemTrackingClient 
from azure.devops.v5_1.work_item_tracking.models import Wiql

# Represent a item of work in a project xxx
class WorkItem(AbstractDevOps):

	def __init__(self,personal_access_token, organization_url):
		super(WorkItem,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	
	# Returns a list of workitems
	def get_work_items(self,project_id): 
		try:
			logging.info("Start function: get_work_items")
						
			logging.info("End function: get_work_items")
			return self.work_item_tracking_client.get_work_items(project_id)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
	
	# Return a specifc workitem from a project
	def get_work_item(self,work_item_id,project_id): 
		try:
			logging.info("Start function: get_work_item")
				
			logging.info("End function: get_work_item")

			return self.work_item_tracking_client.get_work_item(work_item_id,project_id)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
	
	# Return a specifc workitem from a project with detais
	def get_work_item(self,work_item_id,fields="All", as_of=None, expand="All"):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")

			return self.work_item_tracking_client.get_work_item(id=work_item_id, 
                                                        project=None,
                                                        fields=fields,
                                                        as_of=as_of,
                                                        expand=expand)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 


	def get_relation(self, relation):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")

			return self.work_item_tracking_client.get_relation_type(relation)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
    
	def get_backlog_work_items(self, project,team, backlog):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")
			team_context = self.create_team_context(project, team)
			return self.work_client.get_backlog_level_work_items(team_context, backlog.id)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def get_work_item_query_by_wiql_epic_user_story_product_backlog_item(self):
		try:
			wiql = Wiql(
			query="""select 
					*
					from WorkItems
					where 
					[System.WorkItemType] = 'User Story' or 
					[System.WorkItemType] = 'Product Backlog Item' or 
					[System.WorkItemType] = 'Epic'
					order by [System.ChangedDate] desc"""
					
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []
		
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
	def get_work_item_query_by_wiql_task(self):
		try:
			wiql = Wiql(
			query="""
					select [System.Id],
						[System.WorkItemType],
						[System.Title],
						[System.State],
						[System.AreaPath],
						[System.IterationPath],
						[System.Tags],
						[System.TeamProject]
					from WorkItems
					where 
					[System.WorkItemType] = 'Task' 
					order by [System.ChangedDate] desc"""
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def get_work_item_query_by_wiql(self):
		try:
			wiql = Wiql(
			query="""
					select [System.Id],
						[System.WorkItemType],
						[System.Title],
						[System.State],
						[System.AreaPath],
						[System.IterationPath],
						[System.Tags]
					from WorkItems
					order by [System.ChangedDate] desc"""
				)
			wiql_results = self.work_item_tracking_client.query_by_wiql(wiql).work_items
			if wiql_results:
				return wiql_results
			else:
				return []
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 