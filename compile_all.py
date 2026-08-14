#!/usr/bin/env python3
"""
Compile all Python files in the project to check for syntax errors.
"""

import py_compile
import os
import sys
from pathlib import Path


def compile_python_files(directory):
    """Recursively compile all Python files in a directory."""
    errors = []
    compiled = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    py_compile.compile(file_path, doraise=True)
                    compiled += 1
                    print(f"✓ {file_path}")
                except py_compile.PyCompileError as e:
                    errors.append((file_path, str(e)))
                    print(f"✗ {file_path}: {e}")
    
    return compiled, errors


if __name__ == '__main__':
    # Get project root directory
    project_root = Path(__file__).parent
    
    # Directories to compile
    directories = ['app', 'tests']
    
    # Also compile root-level Python files
    root_files = ['run.py']
    
    print("Compiling Python files...\n")
    
    total_compiled = 0
    all_errors = []
    
    # Compile root-level files
    for file in root_files:
        file_path = project_root / file
        if file_path.exists():
            try:
                py_compile.compile(str(file_path), doraise=True)
                total_compiled += 1
                print(f"✓ {file_path}")
            except py_compile.PyCompileError as e:
                all_errors.append((str(file_path), str(e)))
                print(f"✗ {file_path}: {e}")
    
    # Compile directories
    for directory in directories:
        dir_path = project_root / directory
        if dir_path.exists():
            compiled, errors = compile_python_files(str(dir_path))
            total_compiled += compiled
            all_errors.extend(errors)
    
    print(f"\n{'='*50}")
    print(f"Compiled: {total_compiled} files")
    
    if all_errors:
        print(f"Errors: {len(all_errors)}")
        sys.exit(1)
    else:
        print("All files compiled successfully!")
        sys.exit(0)

