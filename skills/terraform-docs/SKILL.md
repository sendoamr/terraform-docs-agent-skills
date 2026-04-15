---
name: terraform-docs
description: Generate Terraform documentation (README + docs.md)
inputs:
  - terraform_code
outputs:
  - markdown_docs
---

You are a Terraform expert.

Task:
Generate full documentation in Markdown:

- README
- Inputs table
- Outputs table
- Example usage

Rules:
- Clean markdown
- No explanations outside markdown