#!/usr/bin/env python3
"""
Main entry point for AVI Test Automation Framework
"""

import sys
import logging
import argparse
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

from framework.api_client import APIClient
from framework.test_runner import TestRunner
from framework.utils import load_config, setup_logging

def print_banner():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}    AVI LOAD BALANCER TEST AUTOMATION FRAMEWORK")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def main():
    parser = argparse.ArgumentParser(description='AVI Test Automation Framework')
    parser.add_argument('--parallel', action='store_true', help='Execute test cases in parallel')
    parser.add_argument('--test-case', type=str, help='Run specific test case by name')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        log_level = logging.DEBUG if args.verbose else logging.INFO
        setup_logging(log_level)
        logger = logging.getLogger(__name__)
        
        logger.info(f"{Fore.GREEN}=== Starting Test Automation Framework ===")
        
        # Load configurations
        logger.info(f"{Fore.BLUE}Loading configuration files...")
        config = load_config('config.yaml')
        test_cases_config = load_config('test_cases.yaml')
        credentials = load_config('credentials.yaml')
        
        # Initialize API client
        logger.info(f"{Fore.BLUE}Initializing API client...")
        api_client = APIClient(
            base_url=config['api']['base_url'],
            credentials=credentials['credentials']
        )
        
        # Authenticate
        logger.info(f"{Fore.BLUE}Authenticating with mock API...")
        if api_client.authenticate():
            logger.info(f"{Fore.GREEN}✓ Authentication successful")
        else:
            logger.error(f"{Fore.RED}Authentication failed")
            sys.exit(1)
        
        # Initialize test runner
        test_runner = TestRunner(
            api_client=api_client,
            config=config,
            test_cases_config=test_cases_config,
            parallel=args.parallel
        )
        
        # Execute test cases
        test_cases = test_cases_config['test_cases']
        logger.info(f"{Fore.BLUE}Executing {len(test_cases)} test case(s)...")
        
        start_time = datetime.now()
        results = test_runner.run_all(test_cases)
        end_time = datetime.now()
        
        # Print summary
        logger.info(f"\n{Fore.CYAN}{'='*60}")
        logger.info(f"{Fore.YELLOW}TEST EXECUTION SUMMARY")
        logger.info(f"{Fore.CYAN}{'='*60}")
        
        total = len(results)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = total - passed
        
        logger.info(f"{Fore.WHITE}Total Test Cases: {total}")
        logger.info(f"{Fore.GREEN}Passed: {passed}")
        logger.info(f"{Fore.RED if failed > 0 else Fore.WHITE}Failed: {failed}")
        logger.info(f"{Fore.WHITE}Execution Time: {(end_time - start_time).total_seconds():.2f} seconds")
        
        logger.info(f"\n{Fore.GREEN}=== Framework Execution Completed ===")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()