import os
from core.ollama import generate

def read_tf():
    content = ""
    for f in ["main.tf", "variables.tf", "outputs.tf"]:
        if os.path.exists(f):
            with open(f) as file:
                content += f"\n\n# {f}\n" + file.read()
    return content


def run():
    tf_code = read_tf()

    prompt = f"""
                Generate Terraform documentation.
                
                Code:
                {tf_code}
            """

    result = generate(prompt)

    with open("docs.md", "w") as f:
        f.write(result)

    return "docs generated"