import logging
logging.basicConfig(level=logging.INFO)
from devopsX.abstractdevops import AbstractDevOps
# Represent a type of Workitem 
class WorkItemType():
	
	def __init__(self,personal_access_token, organization_url):
		super(WorkItemType,self).__init__(personal_access_token=personal_access_token,organization_url=organization_url)
	
	# Return workitem types
	def get_work_item_type(self,project):
		try:
			logging.info("Start function: get_work_item")
			logging.info("End function: get_work_item")
			return self.work_item_tracking_client.get_work_item_types(project)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 