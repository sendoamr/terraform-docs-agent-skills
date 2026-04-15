import importlib.util
import os

SKILLS_PATH = "skills"

def load_skill(skill_name):
    path = os.path.join(SKILLS_PATH, skill_name, "run.py")

    spec = importlib.util.spec_from_file_location(skill_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_skill(skill_name):
    skill = load_skill(skill_name)
    return skill.run()


if __name__ == "__main__":
    print("Running terraform-docs...")
    run_skill("terraform-docs")

    print("Running terraform-tests...")
    run_skill("terraform-tests")