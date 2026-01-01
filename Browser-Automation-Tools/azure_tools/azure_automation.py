"""
Azure Automation Toolkit
========================
Automate common Azure operations: API keys, resource creation, management.

Requirements:
- Azure CLI installed (az --version)
- Logged in (az login)

Usage:
    python azure_automation.py login
    python azure_automation.py list_subscriptions
    python azure_automation.py list_resources [resource_group]
    python azure_automation.py get_keys <resource_type> <resource_name> <resource_group>
    python azure_automation.py create_resource_group <name> <location>
    python azure_automation.py create_cognitive <name> <resource_group> <kind>
    python azure_automation.py create_storage <name> <resource_group>
"""

import subprocess
import json
import sys
from datetime import datetime


def run_az_command(args: list, parse_json: bool = True) -> dict:
    """Run an Azure CLI command and return the result."""
    cmd = ["az"] + args
    if parse_json:
        cmd.append("-o")
        cmd.append("json")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return {"error": result.stderr, "success": False}
        
        if parse_json and result.stdout.strip():
            return {"data": json.loads(result.stdout), "success": True}
        return {"data": result.stdout, "success": True}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out", "success": False}
    except json.JSONDecodeError:
        return {"data": result.stdout, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


def login():
    """Login to Azure (opens browser for authentication)."""
    print("Opening browser for Azure login...")
    result = run_az_command(["login"], parse_json=False)
    if result["success"]:
        print("✅ Login successful!")
        return list_subscriptions()
    else:
        print(f"❌ Login failed: {result.get('error')}")
    return result


def list_subscriptions():
    """List all Azure subscriptions."""
    result = run_az_command(["account", "list"])
    if result["success"]:
        print("\n📋 Azure Subscriptions:")
        print("-" * 60)
        for sub in result["data"]:
            status = "✓" if sub.get("state") == "Enabled" else "✗"
            default = " (DEFAULT)" if sub.get("isDefault") else ""
            print(f"  {status} {sub['name']}{default}")
            print(f"    ID: {sub['id']}")
        return result["data"]
    else:
        print(f"❌ Error: {result.get('error')}")
    return result


def set_subscription(subscription_id: str):
    """Set the active subscription."""
    result = run_az_command(["account", "set", "--subscription", subscription_id])
    if result["success"]:
        print(f"✅ Active subscription set to: {subscription_id}")
    return result


def list_resource_groups():
    """List all resource groups."""
    result = run_az_command(["group", "list"])
    if result["success"]:
        print("\n📁 Resource Groups:")
        print("-" * 60)
        for rg in result["data"]:
            print(f"  • {rg['name']} ({rg['location']})")
        return result["data"]
    return result


def list_resources(resource_group: str = None):
    """List resources in a resource group or all resources."""
    args = ["resource", "list"]
    if resource_group:
        args.extend(["--resource-group", resource_group])
    
    result = run_az_command(args)
    if result["success"]:
        print(f"\n🔧 Resources{' in ' + resource_group if resource_group else ''}:")
        print("-" * 60)
        for res in result["data"]:
            print(f"  • {res['name']}")
            print(f"    Type: {res['type']}")
            print(f"    Location: {res['location']}")
            print()
        return result["data"]
    return result


# ============== API KEYS ==============

def get_cognitive_keys(resource_name: str, resource_group: str):
    """Get API keys for Cognitive Services / Azure AI."""
    result = run_az_command([
        "cognitiveservices", "account", "keys", "list",
        "--name", resource_name,
        "--resource-group", resource_group
    ])
    if result["success"]:
        keys = result["data"]
        print(f"\n🔑 API Keys for {resource_name}:")
        print("-" * 60)
        print(f"  Key1: {keys.get('key1', 'N/A')[:20]}...")
        print(f"  Key2: {keys.get('key2', 'N/A')[:20]}...")
        return keys
    else:
        print(f"❌ Error: {result.get('error')}")
    return result


def get_storage_keys(account_name: str, resource_group: str):
    """Get access keys for Storage Account."""
    result = run_az_command([
        "storage", "account", "keys", "list",
        "--account-name", account_name,
        "--resource-group", resource_group
    ])
    if result["success"]:
        keys = result["data"]
        print(f"\n🔑 Storage Keys for {account_name}:")
        print("-" * 60)
        for key in keys:
            print(f"  {key['keyName']}: {key['value'][:20]}...")
        return keys
    return result


def get_openai_keys(resource_name: str, resource_group: str):
    """Get API keys for Azure OpenAI."""
    return get_cognitive_keys(resource_name, resource_group)


def get_keys(resource_type: str, resource_name: str, resource_group: str):
    """Get API keys based on resource type."""
    type_map = {
        "cognitive": get_cognitive_keys,
        "openai": get_openai_keys,
        "storage": get_storage_keys,
    }
    
    func = type_map.get(resource_type.lower())
    if func:
        return func(resource_name, resource_group)
    else:
        print(f"❌ Unknown resource type: {resource_type}")
        print(f"   Supported types: {', '.join(type_map.keys())}")
        return {"error": "Unknown resource type"}


# ============== CREATE RESOURCES ==============

def create_resource_group(name: str, location: str = "eastus"):
    """Create a new resource group."""
    result = run_az_command([
        "group", "create",
        "--name", name,
        "--location", location
    ])
    if result["success"]:
        print(f"✅ Resource group '{name}' created in {location}")
    return result


def create_cognitive_service(name: str, resource_group: str, kind: str = "CognitiveServices", 
                            sku: str = "S0", location: str = "eastus"):
    """
    Create a Cognitive Services resource.
    
    Kinds: CognitiveServices, OpenAI, FormRecognizer, ComputerVision, 
           TextAnalytics, SpeechServices, etc.
    """
    result = run_az_command([
        "cognitiveservices", "account", "create",
        "--name", name,
        "--resource-group", resource_group,
        "--kind", kind,
        "--sku", sku,
        "--location", location,
        "--yes"
    ])
    if result["success"]:
        print(f"✅ Cognitive Service '{name}' ({kind}) created")
        return get_cognitive_keys(name, resource_group)
    return result


def create_storage_account(name: str, resource_group: str, sku: str = "Standard_LRS",
                          location: str = "eastus"):
    """Create a Storage Account."""
    result = run_az_command([
        "storage", "account", "create",
        "--name", name,
        "--resource-group", resource_group,
        "--sku", sku,
        "--location", location
    ])
    if result["success"]:
        print(f"✅ Storage account '{name}' created")
        return get_storage_keys(name, resource_group)
    return result


def create_openai_service(name: str, resource_group: str, location: str = "eastus"):
    """Create an Azure OpenAI resource."""
    return create_cognitive_service(name, resource_group, kind="OpenAI", location=location)


# ============== DEPLOYMENTS ==============

def list_openai_deployments(resource_name: str, resource_group: str):
    """List OpenAI model deployments."""
    result = run_az_command([
        "cognitiveservices", "account", "deployment", "list",
        "--name", resource_name,
        "--resource-group", resource_group
    ])
    if result["success"]:
        print(f"\n🤖 Deployments for {resource_name}:")
        print("-" * 60)
        for dep in result["data"]:
            print(f"  • {dep['name']}")
            print(f"    Model: {dep.get('properties', {}).get('model', {}).get('name', 'N/A')}")
        return result["data"]
    return result


def create_openai_deployment(resource_name: str, resource_group: str, 
                            deployment_name: str, model_name: str = "gpt-4",
                            model_version: str = "turbo-2024-04-09"):
    """Deploy a model to Azure OpenAI."""
    result = run_az_command([
        "cognitiveservices", "account", "deployment", "create",
        "--name", resource_name,
        "--resource-group", resource_group,
        "--deployment-name", deployment_name,
        "--model-name", model_name,
        "--model-version", model_version,
        "--model-format", "OpenAI"
    ])
    if result["success"]:
        print(f"✅ Deployment '{deployment_name}' ({model_name}) created")
    return result


# ============== QUICK INFO ==============

def get_account_info():
    """Get current Azure account info."""
    result = run_az_command(["account", "show"])
    if result["success"]:
        acc = result["data"]
        print("\n👤 Current Azure Account:")
        print("-" * 60)
        print(f"  Subscription: {acc['name']}")
        print(f"  ID: {acc['id']}")
        print(f"  Tenant: {acc['tenantId']}")
        print(f"  User: {acc.get('user', {}).get('name', 'N/A')}")
        return acc
    return result


# ============== CLI INTERFACE ==============

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    commands = {
        "login": login,
        "account": get_account_info,
        "list_subscriptions": list_subscriptions,
        "list_groups": list_resource_groups,
        "list_resources": lambda: list_resources(args[0] if args else None),
        "get_keys": lambda: get_keys(args[0], args[1], args[2]) if len(args) >= 3 else print("Usage: get_keys <type> <name> <resource_group>"),
        "create_resource_group": lambda: create_resource_group(args[0], args[1] if len(args) > 1 else "eastus") if args else print("Usage: create_resource_group <name> [location]"),
        "create_cognitive": lambda: create_cognitive_service(args[0], args[1], args[2] if len(args) > 2 else "CognitiveServices") if len(args) >= 2 else print("Usage: create_cognitive <name> <resource_group> [kind]"),
        "create_storage": lambda: create_storage_account(args[0], args[1]) if len(args) >= 2 else print("Usage: create_storage <name> <resource_group>"),
        "create_openai": lambda: create_openai_service(args[0], args[1]) if len(args) >= 2 else print("Usage: create_openai <name> <resource_group>"),
        "list_deployments": lambda: list_openai_deployments(args[0], args[1]) if len(args) >= 2 else print("Usage: list_deployments <resource_name> <resource_group>"),
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(commands.keys())}")


if __name__ == "__main__":
    main()
