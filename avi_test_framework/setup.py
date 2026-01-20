#!/usr/bin/env python3
"""
Setup script for AVI Test Framework
Creates all necessary files and configures the environment
"""

import os
import sys
import yaml
import random
import string
import requests
from pathlib import Path

def create_credentials_file():
    """Create credentials.yaml file with auto-generated credentials"""
    
    # Generate a random username and password
    username = f"avi_test_user_{random.randint(1000, 9999)}"
    password = f"Test@123{random.randint(1000, 9999)}"
    
    credentials_content = {
        'credentials': {
            'username': username,
            'password': password,
            'cache_token': True,
            'token_cache_file': '.token_cache'
        }
    }
    
    with open('credentials.yaml', 'w') as f:
        yaml.dump(credentials_content, f, default_flow_style=False)
    
    print(f"✅ Created credentials.yaml with username: {username}")
    print(f"   Password: {password}")
    return username, password

def test_api_connection(username, password):
    """Test connection to the mock API"""
    print("\n🔗 Testing connection to mock API...")
    
    base_url = "https://semantic-brandea-banao-dc049ed0.koyeb.app"
    
    # Try to register
    try:
        register_url = f"{base_url}/register"
        response = requests.post(register_url, json={
            "username": username,
            "password": password
        }, timeout=10)
        
        if response.status_code in [201, 200, 400]:
            print("   Registration attempt completed")
        else:
            print(f"   Registration status: {response.status_code}")
    
    except Exception as e:
        print(f"   Registration attempt failed: {e}")
    
    # Try to login
    try:
        login_url = f"{base_url}/login1"
        response = requests.post(
            login_url,
            auth=(username, password),
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('token', '')
            print(f"   ✅ Login successful!")
            print(f"   Token received: {token[:20]}...")
            return True
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return False

def create_missing_files():
    """Create any missing required files"""
    
    files_to_check = [
        ('config.yaml', """# AVI Test Framework Configuration
api:
  base_url: "https://semantic-brandea-banao-dc049ed0.koyeb.app"
  endpoints:
    register: "/register"
    login: "/login1"
    tenants: "/api/tenant"
    virtual_services: "/api/virtualservice"
    service_engines: "/api/serviceengine"
  
  timeout: 30
  max_retries: 3

framework:
  parallel_execution: true
  max_workers: 3
  log_level: "INFO"
  log_format: "%(asctime)s - %(levelname)s - %(message)s"
  
  mock_components:
    ssh_enabled: true
    rdp_enabled: true

test_settings:
  default_test_case: "disable_virtual_service"
  validate_response: true
  fail_fast: false
"""),
        
        ('test_cases.yaml', """# Test Case Definitions
test_cases:
  - name: "disable_virtual_service"
    description: "Disable the virtual service named backend-vs-t1r_1000-1"
    target_virtual_service: "backend-vs-t1r_1000-1"
    
    stages:
      pre_fetcher:
        enabled: true
        components: ["tenants", "virtual_services", "service_engines"]
      
      pre_validation:
        enabled: true
        validate: "enabled"
        expected_value: true
      
      trigger:
        enabled: true
        action: "disable"
        payload:
          enabled: false
      
      post_validation:
        enabled: true
        validate: "enabled"
        expected_value: false
    
    mock_operations:
      - type: "ssh"
        operation: "connect"
        host: "mock_host_1"
      
      - type: "ssh"
        operation: "execute_command"
        command: "show service status"
      
      - type: "rdp"
        operation: "validate_connection"
        host: "mock_host_2"
"""),
        
        ('requirements.txt', """requests==2.31.0
PyYAML==6.0.1
colorama==0.4.6
""")
    ]
    
    for filename, content in files_to_check:
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("AVI TEST FRAMEWORK SETUP")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('framework', exist_ok=True)
    
    # Create missing files
    create_missing_files()
    
    # Create credentials file
    if not os.path.exists('credentials.yaml'):
        username, password = create_credentials_file()
        
        # Test the credentials
        if test_api_connection(username, password):
            print("\n✅ Setup completed successfully!")
            print("\nNext steps:")
            print("1. Run: python main.py")
            print("2. For parallel execution: python main.py --parallel")
            print("3. For verbose output: python main.py --verbose")
        else:
            print("\n⚠️  API connection test failed.")
            print("You may need to manually edit credentials.yaml")
            print("with your registered username and password")
    else:
        print("\n✅ credentials.yaml already exists")
        print("\nRun the framework with: python main.py")

if __name__ == "__main__":
    main()