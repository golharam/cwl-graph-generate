import unittest
import sys
import os
import io

"""
Unit Tests for the get_workflow_dot Function (draw_arrow sub-function) in cwl_graph_generate.py
The function draw_arrow can wait forever without throwing an assertion error due to the use of pdb.set_trace() in the except block. This causes the program to pause execution and wait for user input indefinitely. By removing or modifying the debugger call, the function doesn't enter an indefinite waiting. May be another simple fix can be to remove the pdb call in the except and simply catch the assertion error as follows.

except AssertionError as e:
        _logger.error(f"Assertion failed: {str(e)}")

Context:
The original implementation of the draw_arrow sub-function contained assertions that could halt execution if certain conditions were not met. Specifically, it would halt if source_num or target_num were None for file-based inputs or outputs. This behavior was problematic in production as it could stop the entire workflow execution. To address this, the assertions were replaced with warnings, allowing the function to continue executing and improving overall reliability.

These tests ensure that the get_workflow_dot function:
1. Properly generates warnings instead of halting when source_num or target_num is None.
2. Continues execution and completes graph generation without interruption, ensuring robustness.

Test Cases:
1. test_warning_for_none_source_num:
    - Verifies that a warning is generated when source_num is None for a file-based input.

2. test_warning_for_none_target_num:
    - Checks that a warning is generated when target_num is None for a file-based output.

3. test_no_warnings_for_non_file_based:
    - Ensures that no warnings are produced for non-file-based inputs and outputs.

4. test_skip_drawing_arrow_for_none_values:
    - Verifies that arrows are not drawn for file-based inputs/outputs with None nums.
    - Checks that only one arrow is drawn (the non-conditional one).
"""

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cwl_graph_generate
from cwl_graph_generate import get_workflow_dot, ids_by_workflow

class MockCommandLineTool:
    def __init__(self):
        self.tool = {"inputs": [{"id": "in1"}], "outputs": [{"id": "out"}]}

class TestWorkflowDot(unittest.TestCase):
    def setUp(self):
        cwl_graph_generate.indent_level = 0
        ids_by_workflow.clear()
        self.held_stderr = io.StringIO()
        self.original_stderr = sys.stderr
        sys.stderr = self.held_stderr

    def tearDown(self):
        sys.stderr = self.original_stderr

    def create_tool(self, input_id, output_id):
        class SimpleTool:
            def __init__(self):
                self.tool = {
                    "id": "test_workflow",
                    "inputs": [{"id": input_id}],
                    "outputs": [{"id": output_id, "outputSource": "step1/out"}],
                    "steps": [{
                        "id": "step1",
                        "in": [{"id": "in1", "source": input_id, "valueFrom": "$(inputs.input1)"}],
                        "out": [{"id": "out"}]
                    }]
                }
                self.steps = [type('Step', (), {
                    'id': 'step1',
                    'tool': {
                        "inputs": [{"id": "in1", "source": input_id, "valueFrom": "$(inputs.input1)"}],
                        "outputs": [{"id": "out"}]
                    },
                    'embedded_tool': MockCommandLineTool()
                })()]
        return SimpleTool()

    def test_warning_for_none_source_num(self):
        tool = self.create_tool("file://input/path", "out")
        cwl_graph_generate.CommandLineTool = MockCommandLineTool
        get_workflow_dot(tool, 1, "test_workflow_id")
        output = self.held_stderr.getvalue()
        self.assertIn("[WARNING_ARROW] source_num is None for file-based source: file://input/path", output)

    def test_warning_for_none_target_num(self):
        tool = self.create_tool("in", "file://output/path")
        cwl_graph_generate.CommandLineTool = MockCommandLineTool
        get_workflow_dot(tool, 1, "test_workflow_id")
        output = self.held_stderr.getvalue()
        self.assertIn("[WARNING_ARROW] target_num is None for file-based target: file://output/path", output)

    def test_no_warnings_for_non_file_based(self):
        tool = self.create_tool("in", "out")
        cwl_graph_generate.CommandLineTool = MockCommandLineTool
        get_workflow_dot(tool, 1, "test_workflow_id")
        output = self.held_stderr.getvalue()
        self.assertNotIn("[WARNING_ARROW] source_num is None", output)
        self.assertNotIn("[WARNING_ARROW] target_num is None", output)

    def test_skip_drawing_arrow_for_none_values(self):
        tool = self.create_tool("file://input/path", "file://output/path")
        cwl_graph_generate.CommandLineTool = MockCommandLineTool
        cwl_graph_generate.arrows.clear()  # Ensure arrows list is empty
        
        get_workflow_dot(tool, 1, "test_workflow_id")
        
        output = self.held_stderr.getvalue()
        
        # Check that warnings were logged
        self.assertIn("[WARNING_ARROW] source_num is None for file-based source: file://input/path", output)
        self.assertIn("[WARNING_ARROW] target_num is None for file-based target: file://output/path", output)
        
        # Check that only the non-file-based arrow was added
        self.assertEqual(len(cwl_graph_generate.arrows), 1)
        self.assertTrue(any('value_from_node' in arrow for arrow in cwl_graph_generate.arrows))
        
        # Check that file-based arrows were not added
        self.assertFalse(any('file://input/path' in arrow for arrow in cwl_graph_generate.arrows))
        self.assertFalse(any('file://output/path' in arrow for arrow in cwl_graph_generate.arrows))

if __name__ == '__main__':
    unittest.main()
