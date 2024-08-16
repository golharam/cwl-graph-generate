import unittest
from unittest.mock import patch
from io import StringIO
from cwl_graph_generate import endId, strip_path  # Import the functions from 'cwl_graph_generate.py'


"""
Unit Tests for the endId Function in cwl_graph_generate.py
The endId function might not pick the conditional variable (like run_manta_step) which is also an operational variable because it relies on the exact ID matching in embedded_tool_part, but conditional variables are often evaluated at runtime, and their presence in the embedded_tool_part might not be guaranteed or they might not be handled the same way as regular IDs.

These tests ensure that the endId function robustly handles different scenarios that are likely to occur in CWL workflows where IDs might serve dual roles as both operational parameters and control parameters:

1. test_end_id_with_exact_match: Verifies that the function correctly identifies and returns a matching ID when present. This is crucial for steps in the workflow that depend on specific IDs being accurately recognized and processed.

2. test_end_id_with_no_match: Ensures that the function returns the original tool_id when no matching ID is found. This case is important for handling situations where an ID, expected as a control parameter, does not match any operational parameters, allowing the workflow to continue without error.

3. test_end_id_with_empty_list: Tests the function's behavior when no IDs are available to match against, ensuring it returns the original tool_id. This scenario supports workflows with optional inputs or configurations, maintaining smooth execution.

4. test_non_existing_id: Confirms that the function returns the original tool_id when the provided ID does not exist among the operational parameters. This test is crucial for workflows where control parameters might be misinterpreted as data inputs, ensuring that such mismatches do not disrupt the workflow's execution.

These tests collectively ensure that endId effectively supports workflow flexibility and robustness, handling variations in ID usage without causing failures.
"""

class TestEndIdFunction(unittest.TestCase):
    def test_end_id_with_exact_match(self):
        """Test endId returns the correct ID when an exact match is found."""
        tool_id = "tool#123"
        embedded_tool_part = [{"id": "tool#123"}, {"id": "tool#456"}]
        expected = "tool#123"
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = endId(tool_id, embedded_tool_part)
            self.assertEqual(result, expected)
            self.assertIn("[DEBUG_MATCH]", mock_stderr.getvalue(), "Expected debug message for match not found")

    def test_end_id_with_no_match(self):
        """Test endId returns the original tool_id when no match is found."""
        tool_id = "tool#789"
        embedded_tool_part = [{"id": "tool#123"}, {"id": "tool#456"}]
        expected = "789"
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = endId(tool_id, embedded_tool_part)
            self.assertEqual(result, expected)
            self.assertIn("[DEBUG_NOMATCH]", mock_stderr.getvalue(), "Expected debug message for no match not found")

    def test_end_id_with_empty_list(self):
        """Test endId returns the original tool_id when the list is empty."""
        tool_id = "tool#000"
        embedded_tool_part = []
        expected = "000"
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = endId(tool_id, embedded_tool_part)
            self.assertEqual(result, expected)
            self.assertIn("[DEBUG_NOMATCH]", mock_stderr.getvalue(), "Expected debug message for empty list not found")

    def test_non_existing_id(self):
        """Test endId with a tool_id that does not exist in the embedded_tool_part."""
        tool_id = "path/to/analysis_tool_b"
        embedded_tool_part = [{"id": "tool#123"}, {"id": "path/to/analysis_tool_a"}]
        expected = "analysis_tool_b"
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = endId(tool_id, embedded_tool_part)
            self.assertEqual(result, expected)
            self.assertIn("[DEBUG_NOMATCH]", mock_stderr.getvalue(), "Expected debug message for non-existing ID not found")

# Run the tests
if __name__ == "__main__":
    unittest.main()

