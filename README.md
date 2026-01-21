<header>
    <h1>Avi Automation Framework</h1>
    <p>Mass-Scale Health Scanner & Operational Controller</p>
</header>

<section>
    <h2>Project Overview</h2>
    <p>This framework is a production-grade Python solution designed for the <strong>VMware NSX Advanced Load Balancer (Avi Vantage)</strong>. It is engineered to handle massive environments containing <strong>1,925+ Virtual Services</strong> using high-performance concurrency and automated discovery.</p>
    
    

    <div class="feature-grid">
        <div class="feature-item">
            <h3>Dynamic Discovery</h3>
            <p>Automatically crawls the entire Controller inventory using API pagination (handling <code>next</code> links) to ensure 100% data visibility across large datasets.</p>
        </div>
        <div class="feature-item">
            <h3>Threaded Execution</h3>
            <p>Utilizes a <code>ThreadPoolExecutor</code> to analyze health and latency across thousands of objects in seconds rather than hours.</p>
        </div>
        <div class="feature-item">
            <h3>5-Stage Lifecycle</h3>
            <p>Follows a strict Fetch → Validate → Action → Verify → Cleanup cycle to guarantee idempotency and environment stability.</p>
        </div>
        <div class="feature-item">
            <h3>Auto-Reporting</h3>
            <p>Generates timestamped CSV health reports highlighting "Action Items"—services that are administratively enabled but operationally down.</p>
        </div>
    </div>
</section>

<section>
    <h2>The Automation Workflow</h2>
    <p>Each task executed by the framework follows a validated lifecycle to prevent configuration drift and ensure state persistence:</p>
    
    

    <table>
        <thead>
            <tr>
                <th>Stage</th>
                <th>Phase</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Pre-Fetcher</td>
                <td>Targeted API call using <code>?name=</code> filters or full inventory pagination.</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Validation</td>
                <td>Cross-references UUIDs and ensures administrative state (Enabled/Disabled) is correct.</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Action</td>
                <td>Executes the RESTful <code>PUT</code> request to modify the object state on the Controller.</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Verification</td>
                <td>Confirms the Controller's <code>oper_status</code> has updated successfully in the database.</td>
            </tr>
            <tr>
                <td>5</td>
                <td>Cleanup</td>
                <td>Restores original settings to maintain the production baseline after testing.</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Setup & Installation</h2>
    <p>Ensure you have Python 3.8+ installed. You can install the required dependencies via pip:</p>
    <div class="code-block">pip install requests pyyaml</div>
    
    <h3>Configuration</h3>
    <p>Update your <code>config/settings.yaml</code> file with the correct Controller credentials:</p>
    <div class="code-block">
api:
  base_url: "https://your-controller-ip"
  username: "anush_avi_test_01"
  password: "your_secure_password"
    </div>
</section>

<section>
    <h2>Troubleshooting</h2>
    <div class="status-box">
        <h4>Connection Timeouts</h4>
        <p>If the script fails while managing >2000 items, increase the <code>timeout</code> in <code>main.py</code> to 60s and reduce <code>max_workers</code> to 5 to lower the API stress on the Controller.</p>
    </div>
    <div class="status-box">
        <h4>Status 419 / Session Expired</h4>
        <p>The Avi Controller terminates idle sessions for security. The <code>AviAutomationFramework</code> class includes an <code>authenticate()</code> method to refresh tokens and re-establish sessions automatically.</p>
    </div>
</section>

<footer>
    <p>Avi Automation Framework &copy; 2026 | Developed for High-Scale SDN Environments</p>
</footer>

</body>
</html>
