import requests
import logging
from typing import List, Dict, Optional
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str, credentials: Dict):
        self.base_url = base_url.rstrip('/')
        self.credentials = credentials
        self.session = requests.Session()
        self.token = None
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def authenticate(self) -> bool:
        try:
            # Try to register first
            register_url = f"{self.base_url}/register"
            payload = {
                "username": self.credentials['username'],
                "password": self.credentials['password']
            }
            
            try:
                self.session.post(register_url, json=payload, timeout=10)
            except:
                pass
            
            # Login to get token
            login_url = f"{self.base_url}/login1"
            response = self.session.post(
                login_url,
                auth=HTTPBasicAuth(self.credentials['username'], self.credentials['password']),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                
                if self.token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.token}'
                    })
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def get_tenants(self) -> List[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/tenant", timeout=10)
            if response.status_code == 200:
                return response.json().get('results', [])
            return []
        except:
            return []
    
    def get_virtual_services(self) -> List[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/virtualservice", timeout=10)
            if response.status_code == 200:
                return response.json().get('results', [])
            return []
        except:
            return []
    
    def get_service_engines(self) -> List[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/serviceengine", timeout=10)
            if response.status_code == 200:
                return response.json().get('results', [])
            return []
        except:
            return []
    
    def get_virtual_service_by_name(self, name: str) -> Optional[Dict]:
        virtual_services = self.get_virtual_services()
        for vs in virtual_services:
            if vs.get('name') == name:
                return vs
        return None
    
    def update_virtual_service(self, uuid: str, payload: Dict) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/api/virtualservice/{uuid}"
            response = self.session.put(url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None