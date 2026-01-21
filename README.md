# Avi Load Balancer Test Automation Framework

<p>
A modular, <b>configuration-driven Python framework</b> designed to automate and validate 
Virtual Services on the VMware NSX Advanced Load Balancer (Avi Vantage).
</p>

<p>
This project demonstrates high-performance parallel execution and a rigorous 
<b>4-stage operational workflow</b> against a live authenticated Mock API.
</p>

---

## 🚀 Why This Project?

Network automation at scale requires more than just scripts; it requires a structured framework. This project:
* **Automates at Scale:** Capable of scanning 1,925+ Virtual Services using multi-threading.
* **Ensures Idempotency:** Follows a strict Fetch-Validate-Action-Verify cycle.
* **Configuration First:** Dynamically parses YAML for credentials and test targets.
* **Protocol Ready:** Includes stubbed components for SSH and RDP management.

---

## 🏗️ Key Concepts Implemented

* **Parallel Execution:** Uses `ThreadPoolExecutor` for concurrent task handling.
* **State Management:** Validates administrative (`enabled`) vs operational (`oper_up`) states.
* **RESTful Automation:** Implements full CRUD operations (GET/PUT) with Bearer Token auth.
* **Galois Field Logic:** Structural logic inspired by error-control coding principles.

---

## 🚦 4-Stage Workflow Walkthrough



1. **Pre-Fetcher:** Connects to the Controller to fetch all Tenants, VSs, and Service Engines.
2. **Pre-Validation:** Targets `backend-vs-t1r_1000-1` and verifies it is currently "Enabled".
3. **Task / Trigger:** Executes a `PUT` request to disable the VS using its unique UUID.
4. **Post-Validation:** Confirms the state change was successful via a final API check.

---

## 💻 Source Code Snippets

### Framework Configuration (`settings.yaml`)
```yaml
api:
  base_url: "[https://semantic-brandea-banao-dc049ed0.koyeb.app/](https://semantic-brandea-banao-dc049ed0.koyeb.app/)"
  username: "your_username"
  password: "your_password"
