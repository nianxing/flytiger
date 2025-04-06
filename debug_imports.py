#!/usr/bin/env python
# This script is used to debug import issues

import os
import sys
import importlib

print("=== Environment Information ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"Sys.path: {sys.path}")
print("============================")

print("\n=== Testing Imports ===")

def test_import(module_name):
    try:
        module = importlib.import_module(module_name)
        print(f"✓ Successfully imported {module_name}")
        return module
    except Exception as e:
        print(f"✗ Failed to import {module_name}: {str(e)}")
        return None

# Test critical imports
flask = test_import("flask")
dotenv = test_import("dotenv")
config = test_import("config")
azure_storage_blob = test_import("azure.storage.blob")
azure_data_tables = test_import("azure.data.tables")

# Try to import specific modules from our app
test_import("app")
app_init = test_import("app.__init__")

# Check if any routes are accessible
test_import("app.routes.main")
test_import("app.routes.products")
test_import("app.routes.orders")
test_import("app.routes.cart")

# Try importing the app itself
test_import("run")

print("\n=== Directory Structure ===")
for root, dirs, files in os.walk("."):
    # Skip directories that start with .
    if "/." in root:
        continue
    level = root.count(os.sep)
    indent = " " * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    sub_indent = " " * 4 * (level + 1)
    for file in files:
        if not file.startswith("."):
            print(f"{sub_indent}{file}")

print("\n=== Debug Complete ===") 