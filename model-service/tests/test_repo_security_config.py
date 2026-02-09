import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_JSON_PATH = REPO_ROOT / "n8n" / "workflow-digitization-qc.json"
CI_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "tests.yml"


def test_n8n_shell_moves_default_disabled():
    workflow = json.loads(WORKFLOW_JSON_PATH.read_text())
    conditional_nodes = {
        node["name"]: node
        for node in workflow["nodes"]
        if node["name"] in {"Allow shell moves? (passed)", "Allow shell moves? (failed)"}
    }

    assert set(conditional_nodes.keys()) == {"Allow shell moves? (passed)", "Allow shell moves? (failed)"}
    for node in conditional_nodes.values():
        condition = node["parameters"]["conditions"]["conditions"][0]["leftValue"]
        assert "USE_SHELL_MOVES || 'false'" in condition


def test_n8n_shell_move_commands_keep_quoted_paths():
    workflow = json.loads(WORKFLOW_JSON_PATH.read_text())
    move_nodes = {
        node["name"]: node["parameters"]["command"]
        for node in workflow["nodes"]
        if node["name"] in {"Move to processed", "Move to failed"}
    }

    assert set(move_nodes.keys()) == {"Move to processed", "Move to failed"}
    for command in move_nodes.values():
        assert "mv -- " in command
        assert "JSON.stringify($binary.data.filePath)" in command


def test_ci_actions_are_commit_pinned():
    workflow_text = CI_WORKFLOW_PATH.read_text().splitlines()
    uses_lines = [line.strip() for line in workflow_text if "uses:" in line]
    assert uses_lines, "No workflow actions found"

    sha_pin = re.compile(r"uses:\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}(\s+#.*)?$")
    for line in uses_lines:
        assert sha_pin.search(line), f"Action not pinned to commit SHA: {line}"
