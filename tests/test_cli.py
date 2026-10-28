import unittest
from unittest.mock import patch

from click.testing import CliRunner

from main import cli


class TestCLI(unittest.TestCase):
    """Tests for the Click command-line interface."""

    def setUp(self):
        self.runner = CliRunner()

    def test_help_shows_commands(self):
        """Test that the help output lists all commands."""
        result = self.runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("delete", result.output)
        self.assertIn("list", result.output)

    @patch("main.load_tasks", return_value=[])
    @patch("main.list_tasks")
    def test_list_command(self, mock_list_tasks, mock_load_tasks):
        """Test that list loads and displays tasks."""
        result = self.runner.invoke(cli, ["list"])

        self.assertEqual(result.exit_code, 0)
        mock_load_tasks.assert_called_once_with()
        mock_list_tasks.assert_called_once_with([])

    @patch("main.add_task", return_value=True)
    @patch("main.load_tasks", return_value=[])
    def test_add_command(self, mock_load_tasks, mock_add_task):
        """Test that add loads tasks and calls add_task."""
        result = self.runner.invoke(
            cli,
            [
                "add",
                "--title", "Study Python",
                "--description", "Complete the assessment",
                "--due-date", "30-10-2026",
            ],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        mock_load_tasks.assert_called_once_with()
        mock_add_task.assert_called_once_with(
            [],
            "Study Python",
            "Complete the assessment",
            "30-10-2026",
        )

    @patch("main.delete_task", return_value=True)
    @patch("main.load_tasks", return_value=[])
    def test_delete_command(self, mock_load_tasks, mock_delete_task):
        """Test that delete loads tasks and calls delete_task."""
        result = self.runner.invoke(
            cli,
            ["delete", "--title", "Study Python"],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        mock_load_tasks.assert_called_once_with()
        mock_delete_task.assert_called_once_with([], "Study Python")
        self.assertIn("Task deleted successfully.", result.output)
