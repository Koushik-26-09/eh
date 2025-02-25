Step 1: Install MongoDB on Kali Linux
MongoDB is not included in Kali's default repositories, so we need to install it manually.

1. Add MongoDB Repository
bash
Copy
Edit
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
2. Import MongoDB GPG Key
bash
Copy
Edit
curl -fsSL https://pgp.mongodb.com/server-5.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-5.0.gpg
3. Update Packages and Install MongoDB
bash
Copy
Edit
sudo apt update
sudo apt install -y mongodb-org
4. Start MongoDB Service
bash
Copy
Edit
sudo systemctl start mongod
sudo systemctl enable mongod  # Enable auto-start on boot
5. Verify MongoDB Installation
bash
Copy
Edit
mongo --eval 'db.runCommand({ connectionStatus: 1 })'
If MongoDB is running, it will return a connection status message.

Step 2: Install shodan CLI and Setup API Key
1. Install Shodan CLI
bash
Copy
Edit
pip install shodan
or

bash
Copy
Edit
sudo apt install python3-pip -y
pip3 install shodan
2. Get Shodan API Key
Sign up at Shodan
After signing up, go to "My Account" to find your API key.
3. Initialize Shodan with Your API Key
bash
Copy
Edit
shodan init YOUR_SHODAN_API_KEY
Replace YOUR_SHODAN_API_KEY with your actual key.

Step 3: Install Required Tools
The script uses jq for JSON formatting. Install it with:

bash
Copy
Edit
sudo apt install jq -y
Step 4: Run the Script
1. Save the Script
Create a file and copy your script into it:

bash
Copy
Edit
nano vuln_fetcher.sh
Paste the script and save (CTRL + X, then Y and ENTER).

2. Make the Script Executable
bash
Copy
Edit
chmod +x vuln_fetcher.sh
3. Run the Script
bash
Copy
Edit
./vuln_fetcher.sh
Step 5: Verify Data in MongoDB
After fetching NVD and MITRE vulnerabilities, check if data is stored in MongoDB:

bash
Copy
Edit
mongo
use db1
show collections
db.cves.find().pretty()
For MITRE:

bash
Copy
Edit
use db2
show collections
db.cves.find().pretty()
For Shodan responses:

bash
Copy
Edit
use db3
show collections
db.shodan_responses.find().pretty()
Now you have a fully functional vulnerability fetching tool on Kali Linux! 🚀


1/2

You said:
how to create db collections
ChatGPT said:
Creating Databases and Collections in MongoDB on Kali Linux
Once MongoDB is installed and running, follow these steps to create databases and collections.

1. Open the MongoDB Shell
Start the MongoDB shell by running:

bash
Copy
Edit
mongo
2. Create a Database
MongoDB does not create a database until you insert data into it. To create a database, switch to it:

bash
Copy
Edit
use db1  # Replace db1 with your desired database name
This will switch to db1, but the database will not be created until a collection is added.

3. Create a Collection
A collection in MongoDB is like a table in SQL databases.

Method 1: Automatic Collection Creation
MongoDB automatically creates a collection when you insert a document:

bash
Copy
Edit
db.cves.insertOne({ "cve_id": "CVE-2024-0001", "description": "Example vulnerability" })
This will:

Create the cves collection (if it doesn't exist)
Insert a sample CVE document
Create the db1 database (if it didn't exist)
Method 2: Manual Collection Creation
You can also manually create an empty collection:

bash
Copy
Edit
db.createCollection("cves")
Output:

json
Copy
Edit
{ "ok" : 1 }
Now, the cves collection exists in db1.

4. Verify Database and Collections
Check Current Database
bash
Copy
Edit
db
It should return:

nginx
Copy
Edit
db1
List All Databases
bash
Copy
Edit
show dbs
If the database is empty, it won't appear. Add data to make it visible.

List Collections in the Current Database
bash
Copy
Edit
show collections
It should show:

nginx
Copy
Edit
cves
View Data in a Collection
bash
Copy
Edit
db.cves.find().pretty()
5. Repeat for Other Databases
For db2 (MITRE data):

bash
Copy
Edit
use db2
db.createCollection("cves")
For db3 (Shodan responses):

bash
Copy
Edit
use db3
db.createCollection("shodan_responses")
Now your MongoDB databases and collections are ready! 🚀






You said:
according to that code
ChatGPT said:
Based on your script, you need to create three MongoDB databases and collections for storing NVD, MITRE, and Shodan data.

Here’s how you can create them before running the script, ensuring there are no errors during data import.

1. Open MongoDB Shell
Start MongoDB if it’s not already running:

bash
Copy
Edit
sudo systemctl start mongod
Then, open the MongoDB shell:

bash
Copy
Edit
mongo
2. Create Databases and Collections
For NVD Data (db1)
bash
Copy
Edit
use db1
db.createCollection("cves")
For MITRE Data (db2)
bash
Copy
Edit
use db2
db.createCollection("cves")
For Shodan Responses (db3)
bash
Copy
Edit
use db3
db.createCollection("shodan_responses")
3. Verify Database and Collections
After creating the collections, check if they exist:

List all databases (Note: Empty databases won’t show up)
bash
Copy
Edit
show dbs
Check collections in each database
For NVD Data (db1):

bash
Copy
Edit
use db1
show collections
For MITRE Data (db2):

bash
Copy
Edit
use db2
show collections
For Shodan Responses (db3):

bash
Copy
Edit
use db3
show collections
Each should output:

nginx
Copy
Edit
cves  # (for db1 and db2)
shodan_responses  # (for db3)
4. Now You Can Run Your Script
Once the databases and collections are set up, execute your script:

bash
Copy
Edit
./vuln_fetcher.sh
Since your script uses mongoimport, it will insert data directly into these collections:

NVD CVEs → db1.cves
MITRE CVEs → db2.cves
Shodan Responses → db3.shodan_responses
After running the script, verify data insertion using:

bash
Copy
Edit
use db1
db.cves.find().pretty()
