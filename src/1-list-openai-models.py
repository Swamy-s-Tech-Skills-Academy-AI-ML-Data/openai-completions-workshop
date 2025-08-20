"""List available OpenAI models using the OPENAI_API_KEY environment variable.

Prerequisite: Set an environment variable named OPENAI_API_KEY (or provide a .env loaded elsewhere).
"""

import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=api_key)

# Call the models API to retrieve a list of available models
models = client.models.list()

# debug output - show response
print(models)

# save to file
with open('oai-models.json', 'w') as file:
    file.write(str(models))

# Print out the organization that owns the models
for model in models.data:
    print("ID:", model.id)
    print("Model owned by:", model.owned_by)
    print("-------------------")
