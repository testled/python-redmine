import os
import datetime
import unittest2

from python_redmine import Redmine, Project

class RedmineTests(unittest2.TestCase):

    def setUp(self):

        # Figure out the path of the responses folder.
        self.responses_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "responses")

        # Mock the projects.json method.
        project_response_file = open(os.path.join(self.responses_path, "projects.json"), "r")
        Redmine.get_projects_json = lambda x: project_response_file.read()

    def test_get_projects(self):
        """
        Tests that we get a correct set of projects.
        """

        redmine = Redmine("http://example.com", "abc123")
        self.assertEqual([project.name for project in redmine.projects], ["Test Project 1", "Test Project 2", "Test Project 3", "Test Project 4"])

    def test_project_properties(self):
        """
        Tests that the project properties have been set correctly.
        """

        redmine = Redmine("http://example.com", "abc123")
        project = redmine.projects[0]

        self.assertEqual(project.name, "Test Project 1")
        self.assertEqual(project.identifier, "test-project-1")
        self.assertEqual(project.description, "Test Project 1 Description")

    def test_project_dates(self):
        """
        Tests that the project properties which are dates have been set correctly.
        """

        redmine = Redmine("http://example.com", "abc123")
        project = redmine.projects[0]

        self.assertEqual(project.created_on, datetime.datetime(2011, 11, 4, 9, 38, 41))
        self.assertEqual(project.updated_on, datetime.datetime(2011, 11, 4, 9, 38, 41))

    def test_get_project_by_id(self):
        """
        Tests getting a project by id.
        """

        redmine = Redmine("http://example.com", "abc123")
        project = redmine.get_project(id = 2)

        self.assertEqual(project.name, "Test Project 2")

    def test_get_project_by_slug(self):
        """
        Tests getting a project by identifier.
        """

        redmine = Redmine("http://example.com", "abc123")
        project = redmine.get_project(identifier = "test-project-4")

        self.assertEqual(project.name, "Test Project 4")

    def test_get_project_by_id_doesnt_exist(self):
        """
        Tests getting a project by id where the id doesn't exist.
        """

        redmine = Redmine("http://example.com", "abc123")
        project = redmine.get_project(id = 5)

        self.assertEqual(project, None)

    def test_get_project_by_slug_doesnt_exist(self):
        """
        Tests getting a project by identifier.
        """

        redmine = Redmine("http://example.com", "abc123")
        project = redmine.get_project(identifier = "abc123")

        self.assertEqual(project, None)

