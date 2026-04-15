import os
import ollama


def read_terraform():
    content = ""
    for f in ["main.tf", "variables.tf", "outputs.tf"]:
        if os.path.exists(f):
            with open(f) as file:
                content += f"\n\n# {f}\n" + file.read()
    return content


def generate_tests(tf_code):
    prompt = f"""
You are an expert in Terraform and Terratest.

Generate Terratest (Go) unit tests for this Terraform module.

Requirements:
- Must work for ANY Terraform module (GCS, BigQuery, IAM, etc.)
- Use terraform.InitAndPlan
- Validate outputs dynamically (do not hardcode unless necessary)
- Follow best practices
- Code must compile
- Return ONLY Go code (no explanations)

Terraform code:
{tf_code}
"""

    response = ollama.generate(
        model="llama3",
        prompt=prompt
    )

    output = response["response"]

    # limpiar markdown si viene con ```
    if "```" in output:
        parts = output.split("```")
        if len(parts) > 1:
            output = parts[1]

    return output


def save_tests(code):
    os.makedirs("tests", exist_ok=True)

    with open("tests/auto_test.go", "w") as f:
        f.write(code)


def run():
    print("📖 Reading Terraform...")
    tf_code = read_terraform()

    print("🧠 Generating tests with Ollama...")
    tests = generate_tests(tf_code)

    print("💾 Saving tests...")
    save_tests(tests)

    print("✅ Tests generated in tests/auto_test.go")


if __name__ == "__main__":
    main()