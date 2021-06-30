##################################################################
# InstaOSINT Tool                                                #
# Fetches details from an Instagram Username                     #
# Can also downloadd all images if account is public             #
# Coded By: LuC1F3R & Inv0k3r                                    #
##################################################################


import urllib.request
from bs4 import BeautifulSoup
import argparse
import re
import os


# Connects and fetches the instargram user profile
def connect ( username ) :
    try:
        contents = urllib.request.urlopen("https://www.instagram.com/"+username)    
    except:                             # throws an exception if username doesn't exits or connection error occurs
        print("Connection error or Username not found!")
        exit()
    
    return contents.read()


# Fetches the arguments passed in the shell
def parse_args () :

    parser = argparse.ArgumentParser(description="Instagram OSINT tool")
    parser.add_argument ( "-u", "--username", help = "profile username", required=True, nargs=1 )
    parser.add_argument ( "-d", "--download" , help = "Downloads the users photos if their account is public", action="store_true", required=False )
    parser.add_argument ( "-f", "--file" , help = "Save the details in a file", action="store_true", required=False )
    

    return parser.parse_args()


#Fetches details from the profile and returns a dictionary with the details
def getdetails(html,user):

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
    if dict['Website'] == 'null' : dict['Website'] = False
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
def print_details ( details ):
    for things in details.keys():                  # Prints values in Dictionary ( There for debugging rn )
        print(things+':\t',details[things])
        
# To save details
def save_details ( details, name ):
    with open( name + '.txt', 'w' ) as file:
        for things in details.keys():                  # Prints values in Dictionary ( There for debugging rn )
            file.write(things+':\t'+str(details[things])+'\n')


# To download an image from a URL
def dw_img ( url , name ):
    urllib.request.urlretrieve( url, name + '.jpg' )

# To download images fromm public profile
def dw_data ( code, name, site ):
    if not os.path.exists( name ):
        os.makedirs( name )
    links = re.findall( '"((http)s?://.*?)"', code )
    i = 1
    n = 3 if site == False else 4
    for url in links:
        if i > n:
            dw_img( url[0].replace( '\\\\u0026','&' ) , name + '\\' + name + '-' + str(i-n))
        i=i+1

args = parse_args()             # fetches the arguments from shell
username = args.username[0]     # fetches username


html = BeautifulSoup( connect( username ), 'html.parser' )      # parses the html document returned
details = getdetails(html,username)       # fetches details from the username and html document

try:
    file = args.file[0]
    if file == 'y' or file == 'Y' :
        save_details( details, username )
    else :   print_details( details )

except:
   print_details( details )
 

try:
    dw = args.download[0]
    if dw == 'y' or dw == 'Y' : 
        dw_data( str(html( 'script', type="text/javascript" )[3].contents ), username, details['Website'] )
        dw_img( details[ 'DP-URL' ], details[ 'Username' ] + '\\' + details[ 'Username' ])
except : pass