##################################################################
# InstaOSINT Tool                                                #
# Fetches details from an Instagram Username                     #
# Can also downloadd all images if account is public             #
# Coded By: LuC1F3R & Inv0k3r                                    #
##################################################################

import argparse
from bs4 import BeautifulSoup
import os
import re
import requests


userAgent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4"}

# Connects and fetches the instargram user profile
def connect ( username ) :
    
    contents = requests.get("https://www.instagram.com/"+username, headers=userAgent)

    if contents.status_code != 200:                             # throws an exception if username doesn't exits or connection error occurs
        print("Connection error or Username not found!")
        
        exit()
    
    return contents.text.encode()


# Fetches the arguments passed in the shell
def parseArguments () :

    parser = argparse.ArgumentParser(description="Instagram OSINT tool")
    parser.add_argument ( "-u", "--username", help = "profile username", required=True, nargs=1 )
    parser.add_argument ( "-d", "--download" , help = "Downloads the users photos if their account is public", action="store_true", required=False )
    parser.add_argument ( "-f", "--file" , help = "Save the details in a file", action="store_true", required=False )
    

    return parser.parse_args()


#Fetches details from the profile and returns a dictionary with the details
def getDetails(html,user):

    dict = { 'Username' : user , 'URL' : "https://www.instagram.com/" + user + '/'}

    dict['Name'] = html.find('title').string.split('(')[0].lstrip()
    if dict['Name'][0] == '@' :
        dict['Name'] = ""

    details = html.find('meta', property="og:description")['content'].split()
    
    dict['Followers'] = details[0]
    dict['Following'] = details[2]
    dict['Posts'] = details[4]

    details = str(html( 'script', type="text/javascript" )[3].contents)

    dict['Website'] = details.split( """external_url":""" )[1].split(",\"")[0].lstrip('\"').rstrip('\"')
    if dict['Website'] == 'null' : 
        dict['Website'] = False

    dict['Is-Business'] = True if details.split("""is_business_account":""")[1].split("\",")[0] == 'true' else False
    if dict['Is-Business'] == True : 
        dict['Business-Type'] = details.split( """business_category_name":""" )[1].split(",\"")[0].lstrip('\"').rstrip('\"')

    dict['Is-Private'] = True if details.split( """is_private":""" )[1].split("\",")[0] == 'true' else False

    dict['Recently-Joined'] = True if details.split( """is_joined_recently":""" )[1].split("\",")[0]=='true' else False
    
    dict['Is-Verified'] = True if details.split( """is_verified":""" )[1].split("\",")[0] == 'true' else False

    dict['Description'] = details.split( """biography":\"""" )[1].split("\",")[0].replace("\\\\n",'\n')
    #dict['Description'] = dict['Description']
        
    dict['DP-URL'] = details.split( """profile_pic_url_hd":""" )[1].split("\",")[0].lstrip('\"').rstrip('\"')
    dict['DP-URL'] = dict['DP-URL'].replace('\\\\u0026','&')
    
    return dict
    
# To print details
def printDetails ( details ):
    for things in details.keys():                  # Prints values in Dictionary ( There for debugging rn )
        print(things+':\t',details[things])
        
# To save details
def saveDetails ( details, name ):
    with open( name + '.txt', 'w' ) as file:
        for things in details.keys():                  # Prints values in Dictionary ( There for debugging rn )
            file.write(things+':\t'+str(details[things])+'\n')


# To download an image from a URL
def downloadImage ( url , name ):
    r = requests.get(url, headers=userAgent)
    if r.status_code == 200:
        with open(name + '.jpg', 'wb') as f:
            for chunk in r:
                f.write(chunk)

# To download images fromm public profile
def downloadData ( code, name, site ):
    links = re.findall( '"((http)s?://.*?)"', code )
    i = 1
    n = 3 if site == False else 4
    for url in links:
        if i > n:
            downloadImage( url[0].replace( '\\\\u0026','&' ) , "./download/" + name + '/' + name + '-' + str(i-n))
        i=i+1



def main():
    args = parseArguments()             # fetches the arguments from shell
    username = args.username[0]     # fetches username


    html = BeautifulSoup( connect( username ), 'html.parser' )      # parses the html document returned
    details = getDetails(html,username)       # fetches details from the username and html document

    if args.file:
        saveDetails( details, username )
    else:
        printDetails( details )
    
    if args.download:
        if not os.path.exists( "download/" + details[ 'Username' ] ):
            os.mkdir("download/" + details[ 'Username' ])
        downloadImage( details[ 'DP-URL' ], "./download/" + details[ 'Username' ] + '/' + details[ 'Username' ])
        downloadData( str(html( 'script', type="text/javascript" )[3].contents ), username, details['Website'] )
        

if __name__ == "__main__":
    if not os.path.exists( "download" ):
            os.mkdir("download")
    main()