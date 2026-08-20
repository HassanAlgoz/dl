from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text

from dspy.primitives import Prediction


def _print_python_block(console: Console, header: Text, code: str) -> None:
    console.print(header)
    console.print(Syntax(code, "python", theme="monokai", background_color="#333333"))



def print_pretty_react_trajectory(result: Prediction) -> None:
    

    console = Console()

    emoji_mapping = {
        'thought': '💭',
        'tool_name': '🛠️',
        'tool_args': '🗝️',
        'observation': '🔎'
    }
    color_mapping = {
        'thought': 'cyan',
        'tool_name': 'yellow',
        'tool_args': 'magenta',
        'observation': 'green'
    }

    for step, value in result.trajectory.items():
        for key, val in value.items() if isinstance(value, dict) else [(step, value)]:
            for prefix in emoji_mapping:
                if key.startswith(prefix):
                    text = Text(f"{emoji_mapping[prefix]} {key}:", style=f"bold {color_mapping[prefix]}")
                    console.print(text, val)
                    break
            else:
                console.print(f"{key}: {val}")
        

def print_pretty_codeact_trajectory(result: Prediction, answer: str = None) -> None:
    """
    Pretty print a CodeAct trajectory in the following order:
    1. All generated_code/code_output pairs (ordered as generated_code_X, code_output_X, ...).
    2. The reasoning step.
    3. The final answer.
    """
    console = Console()
    emoji_mapping = {
        'generated_code': '📜',
        'code_output': '🖨️',
        'reasoning': '🤔',
        'answer': '✨'
    }

    trajectory = getattr(result, "trajectory", {})
    # Collect code steps by index for ordered output
    indices = []
    for k in trajectory:
        if k.startswith("generated_code"):
            idx = k.replace("generated_code", "")
            indices.append(idx)
    # Sort indices for step order ("" if just "generated_code" with no number)
    indices_sorted = sorted(indices, key=lambda x: int(x) if x.isdigit() else 0)

    # Display generated_code_N + code_output_N in order
    for idx in indices_sorted:
        gen_code_key = f"generated_code{idx}"
        code_out_key = f"code_output{idx}"
        if gen_code_key in trajectory:
            text = Text(f"{emoji_mapping['generated_code']} {gen_code_key}:", style="bold")
            _print_python_block(console, text, str(trajectory[gen_code_key]))
        if code_out_key in trajectory:
            text = Text(f"{emoji_mapping['code_output']} {code_out_key}:", style="bold")
            console.print(text, Text(str(trajectory[code_out_key])))

    # Show reasoning (if present)
    reasoning = result.get("reasoning")
    if reasoning:
        text = Text(f"{emoji_mapping['reasoning']} reasoning:", style="bold")
        console.print(text, Text(str(reasoning)))

    # Show answer (provided argument)
    if answer is not None:
        text = Text(f"{emoji_mapping['answer']} answer:", style="bold")
        console.print(text, Text(str(answer)))

