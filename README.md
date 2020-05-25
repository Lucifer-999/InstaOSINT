# InstaOSINT
An OSINT Investigation Tool for Instagram which will fetch all of the public information available for a person/account with a username.

This information will include: 

  1. Username
  2. Name
  3. No. of Followers
  4. No. of Following Accounts
  5. No. of Posts
  6. Description
  7. Profile Picture URL
  8. Account URL
  9. Is Business Account
 10. Business Type (If Business)
 11. Is Private Account
 12. Is Verified Account
 13. Website (If any)
 14. Is Recently Joined
 15. In case of Public Account, Download Photos
 
 
# Requirments

This script only requires Python 3.8 or higher and an active internet connection.

# Usage

Run the following commands

  1. >pip3 install -r requirements.txt
  2. >python InstaOSINT.py [-h] --username USERNAME [--download DOWNLOAD] [--file FILE]
  
# Help

>python InstaOSINT.py --help

usage: InstaOSINT.py [-h] --username USERNAME [--download DOWNLOAD] [--file FILE]

Instagram OSINT tool

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  profile username
  --download DOWNLOAD  Downloads the users photos if their account is public (Y/N)
  --file FILE          Save the details in a file (Y/N)
  
# Disclaimer

This tool is just for gathering information about an Instagram Account.
I am not responsible for any harm that may be done from this tool.
 
