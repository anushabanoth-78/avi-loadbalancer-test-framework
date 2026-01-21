<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Avi Automation Framework - Documentation</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; }
        header { background: #2c3e50; color: #fff; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem; }
        h1 { margin: 0; font-size: 2.5rem; }
        h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 2rem; }
        h3 { color: #2980b9; }
        code { background: #e8eff0; padding: 2px 5px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; }
        .code-block { background: #2d2d2d; color: #f8f8f2; padding: 1.5rem; border-radius: 8px; overflow-x: auto; font-family: 'Consolas', monospace; line-height: 1.4; margin: 1rem 0; }
        .feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 2rem 0; }
        .feature-item { background: #fff; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #3498db; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .status-box { background: #fff; border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin-top: 1rem; }
        .badge { display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }
        .badge-success { background: #27ae60; color: white; }
        .badge-alert { background: #e74c3c; color: white; }
        table { width: 100%; border-collapse: collapse; margin: 1rem 0; background: #fff; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background: #f2f2f2; }
    </style>
</head>
<body>

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
            <p>Automatically crawls the entire Controller inventory using API pagination (handling <code>next</code> links) to ensure 100% data visibility.</p>
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
            <p>Generates timestamped CSV health reports highlighting "Action Items" (services that are enabled but operationally down).</p>
        </div>
    </div>
</section>

<section>
    <h2>The Automation Workflow</h2>
    <p>Each task executed by the framework follows a validated lifecycle to prevent configuration drift:</p>
    
    

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
                <td>Targeted API call using <code>?name=</code> filters to minimize data transfer.</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Validation</td>
                <td>Cross-references UUIDs and ensures administrative state is correct.</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Action</td>
                <td>Executes the RESTful <code>PUT</code> request to modify the object state.</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Verification</td>
                <td>Confirms the Controller's <code>oper_status</code> has updated successfully.</td>
            </tr>
            <tr>
                <td>5</td>
                <td>Cleanup</td>
                <td>Restores original settings to maintain lab/production baseline.</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Setup & Installation</h2>
    <p>Ensure you have Python 3.8+ installed. Install dependencies via pip:</p>
    <div class="code-block">
        pip install requests pyyaml
    </div>
    
    <h3>Configuration</h3>
    <p>Update <code>config/settings.yaml</code> with your Controller credentials:</p>
    <div class="code-block">
api:<br>
&nbsp;&nbsp;base_url: "https://your-controller-ip"<br>
&nbsp;&nbsp;username: "anush_avi_test_01"<br>
&nbsp;&nbsp;password: "your_secure_password"
    </div>
</section>

<section>
    <h2>Troubleshooting</h2>
    <div class="status-box">
        <h4>Connection Timeouts</h4>
        <p>If managing >2000 items, increase <code>timeout</code> in <code>main.py</code> to 60s and reduce <code>max_workers</code> to 5.</p>
    </div>
    <div class="status-box">
        <h4>Status 419 / Session Expired</h4>
        <p>The Avi Controller terminates idle sessions. The <code>AviAutomationFramework</code> class includes an <code>authenticate()</code> method to refresh tokens automatically.</p>
    </div>
</section>

<footer>
    <hr>
    <p style="text-align: center; font-size: 0.8rem; color: #777;">
        Avi Automation Framework &copy; 2026 | Developed for High-Scale SDN Environments
    </p>
</footer>

</body>
</html>
