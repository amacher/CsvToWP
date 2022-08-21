"""
!!!!!!!!WARNING!!!!!!
This is a test version and only used for a quick local install test, it may not work fully as you're expecting.
This is not a final ready to use version, just something to get started with.
FULLY TEST LOCALLY AND THROUGHLY BEFORE USING IN PRODUCTION.
!!!!!!!!WARNING!!!!!!
"""
import mysql.connector
import csv
import re

mydb = mysql.connector.connect(
    host = "localhost",
    port = 111, #add your port number here
    user = "user",
    password = "password",
    database = "wpsite",
)

#To find the highest number post, this should be the one just added.
#use this to to link the category to the post
sql_command = "SELECT MAX(ID) FROM wp_posts;"
my_cursor = mydb.cursor()
my_cursor.execute(sql_command)
highestID = my_cursor.fetchall()[0][0]

#Open CSV file:
#Read the file
with open('<path>/site.csv') as file:
    csvreader = csv.reader(file)
    #header = next(csvreader)
    for row in csvreader:
        #Save to Database
        # #Pull date from to fill in the date areas
        sql_command = "INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, guid, post_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #Naming by the post name in WordPress
        #id = highestID+1 #let the DB add the numbers add if you need to control the numbering
        post_author = 1 
        # postDate = "2022-05-08 08:47:01" # if hard coded such as the original file didn't have a date to pull
        post_date = row[0]
        post_date_gmt = post_date
        post_content = row[2]
        post_title = row[1]
        post_excerpt = '' #NEEDED: You can add code to truncate the post_content; test how to format it through WP first.
        post_status = 'publish' #'publish', 'future' or 'draft' draft will save in the draft folder then you can look at change then publish, a way to keep track if you want to manual look at each file copied over.
        #comment_status = '' #Not Needed
        #ping_status = '' #Not Needed
        #post_password = 'password' #Not Needed
        # #Convert title to post name (no spaces convert to '-'all lower case) NOT FULLY TESTED!!
        postNameConvert = re.sub("\s+", "-", post_title).lower() #need to go back and merge the converters
        post_name =  re.sub('[^A-Za-z0-9^-]+', '', postNameConvert) #converting the title for web safe name 
        to_ping = ''  #NEEDED: pass empty unless you have need
        pinged = ''  #NEEDED: pass empty unless you have need
        post_modified = post_date
        post_modified_gmt = post_date
        post_content_filtered = "" #NEEDED:pass empty unless you have need
        #post_parent = '' #Not Needed
        guid = "http://localhost:111/testSite/?p="+str(highestID+1) #url stardard path if you changed how the names are saved you may need to change.
        #menu_order = '' #Not Needed
        post_type = "post" #you can make it 'page' here or pass through.
        #post_mime_type = '' #Not Needed
        #comment_count = '' #Not Needed
       
        values = (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, guid, post_type)
        my_cursor = mydb.cursor()
        my_cursor.execute(sql_command, values)
        mydb.commit()

        # Link the post to the category
        #Save to Database
        sql_command = "INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) VALUES (%s, %s)"
        #Post Number
        object_id = highestID+1
        #term_order = '' #Not needed, could be if you have multiplies and want in a certain order???
        #Category Number; VARIABLE
        #Add If statments if you need to check for different catagories. 
        term_taxonomy_id = 2 #Category number, check in Database wp_terms or click the cat in WP for 'tag_ID=#'
        values = (object_id, term_taxonomy_id)
        my_cursor = mydb.cursor()
        my_cursor.execute(sql_command, values)
        mydb.commit()