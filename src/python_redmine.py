from datetime import datetime
import simplejson
import requests

class Issue(object):
    def __init__(self, issue_data):
        # A newly constructed object will be clean.
        self._dirty = False

        # Assign all the properties from the JSON representation.
        for key in issue_data:
            if key == "created_on" or key == "updated_on":
                setattr(self, key, datetime.strptime(issue_data[key][:19], "%Y/%m/%d %H:%M:%S"))
            else:
                setattr(self, key, issue_data[key])

class Project(object):
    """
    This is a single Redmine project.
    """

    def __init__(self, project_data):
        """
        Sets up a new Project object based on the dict representation from the API.
        """

        # A newly constructed object will be clean.
        self._dirty = False
        self._issues = []

        # Assign all the properties from the JSON representation.
        for key in project_data:
            if key == "created_on" or key == "updated_on":
                setattr(self, key, datetime.strptime(project_data[key][:19], "%Y/%m/%d %H:%M:%S"))
            else:
                setattr(self, key, project_data[key])

    def __unicode__(self):
        return self.name

    @property
    def issues(self):
        """Get the current list of projects."""
        if not self._issues:
            self.get_issues()
        return self._issues

    def get_issues_json(self):
        response = requests.get("%s/issues.json" % self._redmine_uri, params={'key': self._api_key})
        return response.content

    def get_issues(self):
        parsed_response = simplejson.loads(self.get_issues_json())
        for issue_data in parsed_response['issues']:
            self._issues.append(Issue(issue_data))

    def get_issue(self, **kwargs):
        pass
#        if "id" in kwargs:
#            for project in self.projects:
#                if int(project.id) == int(kwargs['id']):
#                    return project
#        if "identifier" in kwargs:
#            for project in self.projects:
#                if project.identifier == kwargs['identifier']:
#                    return project
#        return None


class Redmine(object):
    def __init__(self, redmine_uri, api_key):
        self._redmine_uri = redmine_uri
        self._api_key = api_key
        self._projects = []

    def __unicode__(self):
        return self.redmine_uri

    @property
    def projects(self):
        """Get the current list of projects."""
        if not self._projects:
            self.get_projects()
        return self._projects

    def get_projects_json(self):
        response = requests.get("%s/projects.json" % self._redmine_uri, params={'key': self._api_key})
        return response.content

    def get_projects(self):
        parsed_response = simplejson.loads(self.get_projects_json())
        print parsed_response
        for project_data in parsed_response['projects']:
            self._projects.append(Project(project_data))

    def get_project(self, **kwargs):
        if "id" in kwargs:
            for project in self.projects:
                if int(project.id) == int(kwargs['id']):
                    return project
        if "identifier" in kwargs:
            for project in self.projects:
                if project.identifier == kwargs['identifier']:
                    return project
        return None