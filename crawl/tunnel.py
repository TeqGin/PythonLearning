import requests
import json
import re

def login_and_get_cookie(email, password):
    """
    Logs in to the website and returns the session cookie
    """
    # Login URL
    login_url = "https://www.fgnwct.com/login"
    
    # Prepare form data
    form_data = {
        "email": email,
        "password": password,
        "rememberMe": "1"
    }
    
    # Set headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    
    # Send login request
    response = requests.post(login_url, data=form_data, headers=headers, allow_redirects=False)
    
    # Check if login was successful
    if response.status_code == 200 or response.status_code == 302:
        # Get Set-Cookie header
        if 'Set-Cookie' in response.headers:
            # Extract the Set-Cookie value
            set_cookie = response.headers['Set-Cookie']
            print("Login successful, got cookies")
            return set_cookie
        else:
            print("No Set-Cookie header found in response")
            return None
    else:
        print(f"Login failed with status code: {response.status_code}")
        print(response.text)
        return None

def query_tunnels(set_cookie):
    """
    Queries the tunnels API using the session cookie and returns the vkey and startServer
    """
    # Query URL
    query_url = "https://www.fgnwct.com/queryTunnels?showAll=false&search=&sort=&order=&limit=10&page=1&offset=0"
    
    # Set headers with cookie
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Cookie": "nodeType=F;" + set_cookie
    }
    
    # Send query request
    response = requests.get(query_url, headers=headers)
    
    # Check if query was successful
    if response.status_code == 200:
        try:
            # Parse JSON response
            data = response.json()
            
            # Check if rows exist and are not empty
            if 'rows' in data and data['rows']:
                # Get the first tunnel information
                tunnel = data['rows'][0]
                vkey = tunnel.get('vkey')
                status = tunnel.get('status')
                start_server = tunnel.get('startServer')

                if status == 'ON':
                    print("device online")
                
                if vkey and start_server:
                    print(f"Found tunnel with vkey: {vkey}")
                    return vkey, start_server
                else:
                    print("Missing vkey or startServer in tunnel data")
            else:
                print("No tunnel data found in response")
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            print(response.text)
    else:
        print(f"Query failed with status code: {response.status_code}")
        print(response.text)
    
    return None, None

def construct_npc_command(vkey, start_server):
    """
    Constructs the NPC command string
    """
    if vkey and start_server:
        command = f"nohup npc -server={start_server} -vkey={vkey}"
        # nohup npc -server=l2.bb1a.cn:8024 -vkey=43087d8168 > npc.log 2>&1 &
        print(f"{command}")
        return command
    else:
        print("Cannot construct command: missing vkey or startServer")
        return None

def main(email, password):
    """
    Main function to run the complete process
    """
    # Step 1: Login and get cookie
    set_cookie = login_and_get_cookie(email, password)
    
    if set_cookie:
        # Step 2 & 3: Query tunnels and get vkey and startServer
        vkey, start_server = query_tunnels(set_cookie)
        
        if vkey and start_server:
            # Step 4: Construct NPC command
            command = construct_npc_command(vkey, start_server)
            return command
    
    return None

if __name__ == "__main__":
    # Replace with your actual email and password
    email = "xudafengabc@sina.com"
    password = "60870736a"
    
    result = main(email, password)
    if result:
        print("Successfully completed all tasks")
    else:
        print("Failed to complete all tasks")
