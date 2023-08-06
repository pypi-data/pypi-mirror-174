# Laji-auth client

A Python client for Laji-auth authentication portal.

## Usage

    from laji_auth_client import LajiAuthClient 
    
    client = LajiAuthClient(<laji_auth_url>, <system_id>)
    login_url = client.get_login_url()
    authentication_info = client.get_authentication_info(<token>)

    success = client.log_out(<token>)