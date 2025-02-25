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
