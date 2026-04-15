import os
import ollama


# -----------------------------
# 1. READ TERRAFORM
# -----------------------------
def read_terraform():
    content = ""

    for f in ["main.tf", "variables.tf", "outputs.tf"]:
        if os.path.exists(f):
            with open(f) as file:
                content += f"\n\n# {f}\n{file.read()}"

    return content


# -----------------------------
# 2. DETECT MODULE TYPE
# -----------------------------
def detect_module_type(tf_code: str):
    if "google_storage_bucket" in tf_code:
        return "GCS_BUCKET"
    elif "bigquery_dataset" in tf_code:
        return "BIGQUERY"
    elif "google_project_iam" in tf_code or "iam" in tf_code.lower():
        return "IAM"
    else:
        return "GENERIC_TERRAFORM"


# -----------------------------
# 3. GENERATE TESTS
# -----------------------------
def generate_tests(tf_code, module_type):
    prompt = f"""
You are a senior DevOps engineer expert in Terraform testing.

Generate a COMPLETE Terratest (Go) test suite.

Module type detected: {module_type}

REQUIREMENTS:
- Must work for ANY Terraform module of this type
- Use terraform.InitAndPlan
- Use terraform.Output for validations
- Must be production-grade
- Must compile
- Use clean Go structure

OUTPUT FORMAT RULES:
You MUST return multiple files separated like this:

// file: setup.go
<code>

// file: terraform_test.go
<code>

// file: helpers.go
<code>

DO NOT include explanations.
ONLY return code.

Terraform code:
{tf_code}
"""

    response = ollama.generate(
        model="llama3",
        prompt=prompt
    )

    return response["response"]


# -----------------------------
# 4. PARSE FILES
# -----------------------------
def parse_and_save(output):
    os.makedirs("tests", exist_ok=True)

    current_file = None
    buffer = []

    for line in output.split("\n"):
        if line.startswith("// file:"):
            # save previous file
            if current_file and buffer:
                with open(f"tests/{current_file}", "w") as f:
                    f.write("\n".join(buffer))

            current_file = line.replace("// file:", "").strip()
            buffer = []
        else:
            buffer.append(line)

    # save last file
    if current_file and buffer:
        with open(f"tests/{current_file}", "w") as f:
            f.write("\n".join(buffer))


# -----------------------------
# 5. MAIN RUNNER
# -----------------------------
def run():
    print("📖 Reading Terraform...")
    tf_code = read_terraform()

    print("🧠 Detecting module type...")
    module_type = detect_module_type(tf_code)
    print(f"🔎 Module detected: {module_type}")

    print("🤖 Generating tests with Ollama...")
    output = generate_tests(tf_code, module_type)

    print("💾 Saving structured tests...")
    parse_and_save(output)

    print("✅ Tests generated in /tests")


if __name__ == "__main__":
    run()