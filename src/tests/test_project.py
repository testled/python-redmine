import os
import datetime
import unittest2

from python_redmine import Redmine, Project

class ProjectTests(unittest2.TestCase):

    def setUp(self):

        # Figure out the path of the responses folder.
        self.responses_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "responses")

        # Mock the projects.json method.
        projects_response_file = open(os.path.join(self.responses_path, "projects.json"), "r")
        Redmine.get_projects_json = lambda x: projects_response_file.read()

        # Mock the issues.json method.
        issues_response_file = open(os.path.join(self.responses_path, "issues.json"), "r")
        Project.get_issues_json = lambda x: issues_response_file.read()

    def test_get_issues(self):
        """
        Tests that we get a correct set of projects.
        """

        redmine = Redmine("http://example.com", "abc123")

        project = redmine.projects[0]

        self.assertEqual([issue.id for issue in project.issues], [1, 2, 3, 4])

