import logging
import threading
import time
from typing import Dict, List
from datetime import datetime
from colorama import Fore

logger = logging.getLogger(__name__)

class TestCase:
    def __init__(self, name: str, config: Dict, api_client):
        self.name = name
        self.config = config
        self.api_client = api_client
        self.vs_uuid = None
    
    def execute(self) -> Dict:
        logger.info(f"\n{Fore.CYAN}{'='*50}")
        logger.info(f"{Fore.YELLOW}Executing Test Case: {self.name}")
        logger.info(f"{Fore.CYAN}{'='*50}")
        
        start_time = datetime.now()
        
        try:
            # Execute stages
            self._pre_fetcher()
            self._pre_validation()
            self._trigger()
            self._post_validation()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = {
                'test_case_name': self.name,
                'status': 'PASS',
                'duration': duration,
                'timestamp': start_time.isoformat()
            }
            
            logger.info(f"\n{Fore.GREEN}Test Case {self.name}: PASS ({duration:.2f}s)")
            return result
            
        except Exception as e:
            logger.error(f"{Fore.RED}Test case failed: {str(e)}")
            return {
                'test_case_name': self.name,
                'status': 'FAIL',
                'error': str(e),
                'duration': (datetime.now() - start_time).total_seconds()
            }
    
    def _pre_fetcher(self):
        logger.info(f"\n{Fore.BLUE}[Pre-Fetcher Stage]")
        
        components = self.config['stages']['pre_fetcher']['components']
        
        for component in components:
            if component == 'tenants':
                tenants = self.api_client.get_tenants()
                logger.info(f"  ✓ Fetched {len(tenants)} tenants")
                if tenants:
                    logger.info(f"     Sample: {[t.get('name', 'N/A') for t in tenants[:3]]}")
                
            elif component == 'virtual_services':
                virtual_services = self.api_client.get_virtual_services()
                logger.info(f"  ✓ Fetched {len(virtual_services)} virtual services")
                if virtual_services:
                    logger.info(f"     Sample: {[vs.get('name', 'N/A') for vs in virtual_services[:3]]}")
                
            elif component == 'service_engines':
                service_engines = self.api_client.get_service_engines()
                logger.info(f"  ✓ Fetched {len(service_engines)} service engines")
                if service_engines:
                    logger.info(f"     Sample: {[se.get('name', 'N/A') for se in service_engines[:3]]}")
    
    def _pre_validation(self):
        logger.info(f"\n{Fore.BLUE}[Pre-Validation Stage]")
        
        target_vs_name = self.config.get('target_virtual_service')
        if not target_vs_name:
            raise Exception("No target virtual service specified")
        
        virtual_service = self.api_client.get_virtual_service_by_name(target_vs_name)
        
        if not virtual_service:
            raise Exception(f"Virtual service '{target_vs_name}' not found")
        
        self.vs_uuid = virtual_service.get('uuid')
        logger.info(f"  ✓ Found VS '{target_vs_name}' (UUID: {self.vs_uuid})")
        
        field = self.config['stages']['pre_validation'].get('validate')
        expected_value = self.config['stages']['pre_validation'].get('expected_value')
        
        actual_value = virtual_service.get(field)
        if actual_value == expected_value:
            logger.info(f"  ✓ Validation passed: {field} = {actual_value}")
        else:
            raise Exception(f"Validation failed: {field} = {actual_value} (expected {expected_value})")
    
    def _trigger(self):
        logger.info(f"\n{Fore.BLUE}[Task/Trigger Stage]")
        
        if not self.vs_uuid:
            raise Exception("No virtual service UUID available")
        
        action = self.config['stages']['trigger'].get('action')
        payload = self.config['stages']['trigger'].get('payload', {})
        
        logger.info(f"  ⚡ Executing action: {action}")
        logger.info(f"  📤 Payload: {payload}")
        
        if action == 'disable':
            result = self.api_client.update_virtual_service(self.vs_uuid, payload)
            if result:
                logger.info(f"  ✓ Virtual service updated successfully")
                logger.info(f"  📥 Response: {result}")
            else:
                raise Exception("Failed to update virtual service")
        
        # Mock operations
        logger.info(f"\n{Fore.MAGENTA}[Mock Operations]")
        mock_ops = self.config.get('mock_operations', [])
        for op in mock_ops:
            if op.get('type') == 'ssh':
                logger.info(f"  🔐 MOCK_SSH: {op.get('operation')} - {op}")
            elif op.get('type') == 'rdp':
                logger.info(f"  🖥️  MOCK_RDP: {op.get('operation')} - {op}")
    
    def _post_validation(self):
        logger.info(f"\n{Fore.BLUE}[Post-Validation Stage]")
        
        if not self.vs_uuid:
            return
        
        virtual_service = self.api_client.get_virtual_service_by_name(
            self.config.get('target_virtual_service')
        )
        
        if virtual_service:
            field = self.config['stages']['post_validation'].get('validate')
            expected_value = self.config['stages']['post_validation'].get('expected_value')
            
            actual_value = virtual_service.get(field)
            if actual_value == expected_value:
                logger.info(f"  ✓ Post-validation passed: {field} = {actual_value}")
            else:
                logger.warning(f"  ⚠ Post-validation warning: {field} = {actual_value} (expected {expected_value})")


class TestRunner:
    def __init__(self, api_client, config: Dict, test_cases_config: Dict, parallel: bool = False):
        self.api_client = api_client
        self.config = config
        self.test_cases_config = test_cases_config
        self.parallel = parallel
    
    def run_all(self, test_cases: List[Dict]) -> List[Dict]:
        if self.parallel and len(test_cases) > 1:
            return self._run_parallel(test_cases)
        else:
            return self._run_sequential(test_cases)
    
    def _run_sequential(self, test_cases: List[Dict]) -> List[Dict]:
        results = []
        
        for test_case_config in test_cases:
            test_case = TestCase(
                name=test_case_config['name'],
                config=test_case_config,
                api_client=self.api_client
            )
            
            result = test_case.execute()
            results.append(result)
            time.sleep(1)
        
        return results
    
    def _run_parallel(self, test_cases: List[Dict]) -> List[Dict]:
        results = []
        threads = []
        
        def run_test_case(test_case_config, result_list):
            test_case = TestCase(
                name=test_case_config['name'],
                config=test_case_config,
                api_client=self.api_client
            )
            result = test_case.execute()
            result_list.append(result)
        
        logger.info(f"\n{Fore.YELLOW}Running {len(test_cases)} test cases in parallel...")
        
        for test_case_config in test_cases:
            thread = threading.Thread(
                target=run_test_case,
                args=(test_case_config, results)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        logger.info(f"{Fore.GREEN}All parallel test cases completed")
        return results