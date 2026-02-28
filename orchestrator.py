import argparse
import yaml
import os

CONFIG_PATH = "config/repo-groups.yaml"

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def plan(config):
    print("\n=== PLAN MODE ===")
    print(f"Managed base path: {config['base_path']}")
    for project_name, project_data in config["projects"].items():
        print(f"\nProject: {project_name}")
        for repo in project_data["repos"]:
            print(f" - {repo['name']} ({repo['blueprint']})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["plan"], help="Operation mode")
    args = parser.parse_args()

    config = load_config()

    if args.command == "plan":
        plan(config)

if __name__ == "__main__":
    main()