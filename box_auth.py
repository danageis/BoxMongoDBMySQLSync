#!/usr/bin/env python

try:
    import os
    import sys
    import re
    import pickle
    import threading
    import webbrowser
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import boxsdk
except Exception as e:
    print("Error importing Modules:")
    print("\n\t%s\n" % e)
    input("Press Enter to exit...")
    sys.exit(1)

""" GLOBAL VARIABLES """
auth_code = None
httpd = None
server_thread = None
box_user = 'box_user'
BOX_CLIENT_ID = 'mo0n5dbl8rbum3quea3l6u4wdos6lbvr'
BOX_CLIENT_SECRET = 'hVIO11vYfpsPenDM6yS5p6OXttMu1evD'
access_token, refresh_token = None, None
cache = os.path.join(os.getcwd(), 'cache')
if not os.path.isdir(cache): os.mkdir(cache)
auth_store = os.path.join(cache, 'auth.pkl')

""" CLASS DEFINITIONS """
class BoxRedirectHandler(BaseHTTPRequestHandler):
    """Extends base HTTP server class to get Box Auth codes on redirect"""
    def do_GET(self):
        """Handle HTTP GET requests"""
        global auth_code
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Print message to browser after authenticating
        m = re.match(r'^.*&code=(?P<auth_code>.+$)', self.path, re.I)
        if m:
            message = "Authentication Success! You may now close this window."
            auth_code = m.group('auth_code')
        else:
            message = "Waiting for Authentication."
        self.wfile.write(bytes(message, "utf8"))
        return

    def log_message(self, format, *args):
        """Overwrite default logging method to silence HTTPD messages """
        return

""" GLOBAL FUNCTIONS """
def retrieve_tokens():
    """Retrieve access and refresh tokens from local cache file."""
    global access_token, refresh_token
    try:
        with open(auth_store, 'rb') as p:
            tokens = pickle.load(p)
    except FileNotFoundError:
        tokens = [None, None]
    access_token = tokens[0]
    refresh_token = tokens[1]
    return access_token, refresh_token

def store_tokens(access_token, refresh_token):
    """Store access and refresh Box tokens to local cache file."""
    with open(auth_store, 'wb') as p:
        pickle.dump([access_token, refresh_token], p)

def run_server():
    """Run HTTP server to retrieve auth_code for Box SDK."""
    global httpd
    server_addr = ('127.0.0.1', 7777)
    httpd = HTTPServer(server_addr, BoxRedirectHandler)
    httpd.serve_forever()

def start_session():
    """Initialize a Box session using Box API.  """
    global access_token, refresh_token, server_thread, httpd
    # Try to retrieve tokens from keychain
    #   If error during OAuth or no tokens, re-authenticate
    try:
        access_token, refresh_token = retrieve_tokens()
        oauth = boxsdk.OAuth2(client_id = BOX_CLIENT_ID,
                              access_token = access_token,
                              refresh_token = refresh_token,
                              client_secret = BOX_CLIENT_SECRET,
                              store_tokens = store_tokens
                              )
        if None in (access_token, refresh_token):
            raise boxsdk.exception.BoxOAuthException('No Tokens')
    except boxsdk.exception.BoxOAuthException:
        # Authenticate with OAuth
        print("Authenticating...".ljust(70), end="", flush=True)
        oauth = boxsdk.OAuth2(client_id=BOX_CLIENT_ID,
                              client_secret=BOX_CLIENT_SECRET,
                              store_tokens = store_tokens
                              )
    
        # Start HTTP server to get auth token from Box.com redirect
        server_thread = threading.Thread(target=run_server)
        server_thread.start()
        auth_url, csrf = oauth.get_authorization_url('http://127.0.0.1:7777')
    
        # Open browser and wait for user authentification
        webbrowser.open(auth_url)
        while not auth_code: pass
    
        # Shutdown HTTP Server
        httpd.shutdown()
        server_thread.join()
        access_token, refresh_token = oauth.authenticate(auth_code)
        httpd.shutdown()
        print("Complete!")

    # Return authenticated client
    return boxsdk.Client(oauth)

if __name__ == "__main__":
    start_session()
    print("Box.com authentication successfull!")
    input("Press Enter to exit...")
