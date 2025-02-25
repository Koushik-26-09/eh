#!/bin/bash

# MongoDB connection details
MONGO_HOST="127.0.0.1"
MONGO_PORT="27017"
DB1="db1"  # Database for NVD data
DB2="db2"  # Database for MITRE data
DB3="db3"  # Database for Shodan responses

# Shodan API key (replace with your actual API key)
SHODAN_API=""

# Function to fetch vulnerabilities from NVD
fetch_nvd() {
    echo "Fetching NVD data..."
    # Fetch raw data from NVD
    curl -s 'https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&search_type=last3months&isCpeNameSearch=false' \
        -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0' \
        -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8' \
        -H 'Connection: keep-alive' > nist.gov.txt

    # Extract CVE IDs and format as JSON
    echo "[" > cve_list.json
    cat nist.gov.txt | grep -E "CVE-[0-9]-[0-9]" -o | sort -u | sed 's/.*/{ "cve_id": "&" },/' >> cve_list.json
    sed -i '$ s/,$//' cve_list.json  # Remove the last trailing comma
    echo "]" >> cve_list.json

    echo "Extracted CVEs saved to cve_list.json."

    # Import JSON to MongoDB
    mongoimport --host=$MONGO_HOST --port=$MONGO_PORT --db=$DB1 --collection=cves --jsonArray --file=cve_list.json
    echo "NVD data imported into MongoDB ($DB1)."
}

# Function to fetch vulnerabilities from MITRE
fetch_mitre() {
    echo "Fetching MITRE data..."
    curl -s 'https://cve.mitre.org/data/downloads/allitems.csv' -o allitems.csv
    
    # Skip metadata lines and parse actual CVE entries
    grep "^\"CVE-" allitems.csv | awk -F, '{print "{ \"cve_id\": " $1 ", \"description\": " $3 " }"}' > mitre_data.json
    
    # Wrap in JSON array
    sed -i '1s/^/[/' mitre_data.json
    echo "]" >> mitre_data.json
    
    echo "MITRE data converted to JSON."
    mongoimport --host=$MONGO_HOST --port=$MONGO_PORT --db=$DB2 --collection=cves --jsonArray --file=mitre_data.json
    echo "MITRE data imported into MongoDB ($DB2)."
}   
 # Import JSON to MongoDB
    mongoimport --host=$MONGO_HOST --port=$MONGO_PORT --db=$DB2 --collection=cves --jsonArray --file=mitre_data.json
    echo "MITRE data imported into MongoDB ($DB2)."


# Function to query Shodan with a CVE ID
query_shodan() {
    echo "Enter the CVE ID to query:"
    read CVE_ID

    # Query Shodan using the API key
    RESPONSE=$(shodan search "$CVE_ID" --key $SHODAN_API --limit 5)

    # Save the response in JSON format and import it into MongoDB
    echo $RESPONSE | jq '.' > shodan_response.json
    mongoimport --host=$MONGO_HOST --port=$MONGO_PORT --db=$DB3 --collection=shodan_responses --jsonArray --file=shodan_response.json

    echo "Shodan response saved in MongoDB ($DB3)."
}

# Function to view Shodan responses
view_shodan() {
    echo "Viewing Shodan responses stored in MongoDB..."
    mongo $DB3 --eval 'db.shodan_responses.find().pretty()'
}

# Main menu
while true; do
    echo "Select an option:"
    echo "1. Fetch NVD vulnerabilities"
    echo "2. Fetch MITRE vulnerabilities"
    echo "3. Query Shodan with CVE ID"
    echo "4. View Shodan responses"
    echo "5. Exit"
    read OPTION

    case $OPTION in
        1)
            fetch_nvd
            ;;
        2)
            fetch_mitre
            ;;
        3)
            query_shodan
            ;;
        4)
            view_shodan
            ;;
        5)
            echo "Exiting the tool. Goodbye!"
            break
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done
