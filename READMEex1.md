MongoDB and Shodan Setup Guide for Kali Linux

Step 1: Install MongoDB on Kali Linux

MongoDB is not included in Kali's default repositories, so we need to install it manually.

1. Add MongoDB Repository

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

2. Import MongoDB GPG Key

curl -fsSL https://pgp.mongodb.com/server-5.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-5.0.gpg

3. Update Packages and Install MongoDB

sudo apt update
sudo apt install -y mongodb-org

4. Start MongoDB Service

sudo systemctl start mongod
sudo systemctl enable mongod  # Enable auto-start on boot

5. Verify MongoDB Installation

mongo --eval 'db.runCommand({ connectionStatus: 1 })'

If MongoDB is running, it will return a connection status message.

Step 2: Install Shodan CLI and Setup API Key

1. Install Shodan CLI

pip install shodan

OR

sudo apt install python3-pip -y
pip3 install shodan

2. Get Shodan API Key

Sign up at Shodan

After signing up, go to "My Account" to find your API key.

3. Initialize Shodan with Your API Key

shodan init YOUR_SHODAN_API_KEY

Replace YOUR_SHODAN_API_KEY with your actual key.

Step 3: Install Required Tools

The script uses jq for JSON formatting. Install it with:

sudo apt install jq -y

Step 4: Run the Script

1. Save the Script

Create a file and copy your script into it:

nano vuln_fetcher.sh

Paste the script and save (CTRL + X, then Y, and ENTER).

2. Make the Script Executable

chmod +x vuln_fetcher.sh

3. Run the Script

./vuln_fetcher.sh

Step 5: Create Databases and Collections in MongoDB

1. Open MongoDB Shell

mongo

2. Create Databases and Collections

For NVD Data (db1)

use db1
db.createCollection("cves")

For MITRE Data (db2)

use db2
db.createCollection("cves")

For Shodan Responses (db3)

use db3
db.createCollection("shodan_responses")

3. Verify Database and Collections

List all databases (Note: Empty databases won’t show up)

show dbs

Check collections in each database

For NVD Data (db1):

use db1
show collections

For MITRE Data (db2):

use db2
show collections

For Shodan Responses (db3):

use db3
show collections

Expected Output:

cves  # (for db1 and db2)
shodan_responses  # (for db3)

Step 6: Verify Data in MongoDB

Check NVD Data in MongoDB (db1)

use db1
show collections
db.cves.find().pretty()

Check MITRE Data in MongoDB (db2)

use db2
show collections
db.cves.find().pretty()

Check Shodan Responses in MongoDB (db3)
----------------------------------------------------------------------------------------------
OWASP ZAP (Zed Attack Proxy) provides script-based authentication, allowing users to define custom authentication mechanisms for web applications. Below is a step-by-step guide to setting up script-based authentication in OWASP ZAP.

Step 1: Start OWASP ZAP
Open OWASP ZAP.
Ensure the target application is running and accessible.
Step 2: Set Up a Context
In OWASP ZAP, go to "Contexts" → "New Context".
Name the context (e.g., MyAppContext).
Add the target URL to the context.
Step 3: Identify Authentication Parameters
Open the login page in a browser (or use ZAP's "Manual Request Editor").
Inspect the login request (via Developer Tools or ZAP's proxy).
Identify:
Login URL (e.g., https://example.com/login)
Request type (POST or GET)
Username and password fields
Any additional tokens (CSRF, session ID, etc.)
Step 4: Enable Script-Based Authentication
Go to "Contexts" → Select your context → "Authentication" tab.
Choose "Script-based Authentication" from the dropdown.
Step 5: Create an Authentication Script
Open ZAP's Scripts tab (View → Show Tab → Scripts).
Right-click "Authentication" → New Script.
Select:
Type: Authentication
Engine: JavaScript
Template: "HTTP Authentication Script" (or blank)
Name the script (e.g., MyAuthScript).
Step 6: Write the Authentication Script
Replace the script content with something like this:

javascript
Copy
Edit
function authenticate(helper, paramsValues, credentials) {
    var loginUrl = paramsValues.get("loginUrl");
    var username = credentials.getParam("username");
    var password = credentials.getParam("password");

    var requestBody = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password);

    var msg = helper.prepareMessage();
    msg.getRequestHeader().setURI(new URI(loginUrl, false));
    msg.setRequestBody(requestBody);
    msg.getRequestHeader().setHeader("Content-Type", "application/x-www-form-urlencoded");

    helper.sendAndReceive(msg);

    return msg;
}
// OWASP ZAP Script-Based Authentication
// This script sends a login request and extracts session cookies for authentication.

function authenticate(helper, paramsValues, credentials) {
    var loginUrl = paramsValues.get("loginUrl"); // Get login URL from script parameters
    var username = credentials.getParam("username"); // Get username
    var password = credentials.getParam("password"); // Get password

    // Construct the login request body (modify based on your form fields)
    var requestBody = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password);

    // Prepare the HTTP request
    var msg = helper.prepareMessage();
    msg.getRequestHeader().setURI(new org.parosproxy.paros.network.HttpSender(new java.net.URI(loginUrl, false)));
    msg.getRequestHeader().setMethod("POST"); // Change to "GET" if login uses a GET request
    msg.setRequestBody(requestBody);
    msg.getRequestHeader().setHeader("Content-Type", "application/x-www-form-urlencoded");

    // Send login request
    helper.sendAndReceive(msg);

    // Check for successful authentication (Modify based on your response)
    var responseBody = msg.getResponseBody().toString();
    if (responseBody.contains("Invalid username or password")) {
        print("Authentication failed: Invalid credentials.");
        return null;
    }

    // Extract session cookies
    var cookies = msg.getResponseHeader().getHttpCookies();
    for (var i = 0; i < cookies.size(); i++) {
        print("Extracted Cookie: " + cookies.get(i).toString());
    }

    return msg;
}

Modify:

loginUrl: Set the actual login endpoint.
requestBody: Match the form data structure.
Step 7: Configure Authentication Parameters
Under "Contexts" → "Authentication", select the new script.
Click "Script Parameters" and set:
loginUrl: The login API or form URL.
Step 8: Define User Credentials
Under "Users", add a user.
Enter username & password.
Associate the user with the authentication script.
Step 9: Configure Session Management
Under "Contexts" → "Session Management", choose:
Cookie-based session management (for web apps).
HTTP Authentication (for basic auth).
Step 10: Test Authentication
Under "Users", right-click the user → "Authenticate".
Check if authentication works:
Go to "HTTP Sessions" tab.
Verify if a session is created.
Step 11: Enable Authorization Detection (Optional)
Go to "Contexts" → "Authorization".
Configure rules to detect unauthorized access.
Step 12: Start Scanning
Select "Spider" or "Active Scan".
Choose the authenticated user.
Start scanning.
