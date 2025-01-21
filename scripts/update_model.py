import datetime

# Example: Append a timestamp to README.md
with open("README.md", "a") as readme_file:
    readme_file.write(f"\nLast updated: {datetime.datetime.now().isoformat()}\n")

print("README.md updated with timestamp.")
