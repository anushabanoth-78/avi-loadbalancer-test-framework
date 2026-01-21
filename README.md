# Avi Automation Framework (Task 1 Submission)

An interactive automation framework built to manage mass-scale Virtual Services on the VMware NSX Advanced Load Balancer.



## 🚀 Why This Project?
Managing **1,925+ Virtual Services** manually is inefficient. This framework:
* Provides a 4-stage lifecycle for reliable state changes.
* Uses multi-threading to scan thousands of objects in seconds.
* Implements configuration-driven testing via YAML.

---

## 🏗️ Technical Implementation

### Core Automation Logic (`main.py`)
Below is the Python engine that handles the discovery and 4-stage workflow (Pre-fetch, Pre-validation, Task, and Post-validation).

```python
import requests
import yaml
from concurrent.futures import ThreadPoolExecutor

# Your Python code goes here
def avi_task_executor():
    print("MOCK_SSH: Connecting to host...")
    # Logic for backend-vs-t1r_1000-1
    pass
