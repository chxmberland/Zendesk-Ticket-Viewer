#   
#   Author: Benjamin Chamberland
#   Date: Thursday, November 26th
#
#   Description:
#       
#       This program will use Zendesk's RESTful API to GET ticket data from someones Zendesk account. 
#       It will then process that data and display it in a clean and convenient manner in the shell.
#
#   References:
#
#       GET ticket URL: https://{subdomain}.zendesk.com/api/v2/tickets.json
#       GET ticket cURL: curl https://{subdomain}.zendesk.com/api/v2/tickets.json \ -v -u {email}:{password}
#



# Importing the necessary libraries to make a sucsessful request
import requests
from requests.auth import HTTPBasicAuth

# Importing the necessary libraries to process the request data
import json

# Importing a custom ticket class
from ticket import Ticket

# Importing a library which helps to format tables
from tabulate import tabulate



# GETTING USER PREFERENCES

# Greeting the user
print("\nHello! How are you? Don't bother answering that, I'm a computer." \
    + "\nI'm here to help you view the tickets related to your Zendesk account!" \
    + "\nWe make use of Zendesk's RESTful API which requires authetication on your end, so we'll need some of your information to get started.")

# Requesting the users Zendesk account data until authentication to Zendesk's API is granted
user_authenticated = False
while not user_authenticated:

    user_subdomain =    input("\nPlease enter your personal Zendesk subdomain (it should look like https://\"\{subdomain\}\".zendesk.com): ")
    user_email =        input("Now, the email related to your Zendesk account: ")
    user_pass =         input("Finally, your password (I'll keep it secret): ")
    user_url = "https://" + user_subdomain.strip() + ".zendesk.com/api/v2/tickets.json"

    print("\nGetting your data now...")

    # Using Python's requests and HTTPBasicAuth library to abstract the HTTP request from Zendesk's API using basic authentication
    response = requests.get(user_url, auth = HTTPBasicAuth(user_email, user_pass.strip()))

    # Printing the arror
    if response.status_code != 200:
        print("\nOur program was unable to authenticate you, or Zendesk's API is unavailable." \
            + "\nDouble check your email and password, that's most likely the issue." \
            + "\nIf this error persists, reach out to us at becha9260@gmail.com, and we'll help fix the problem." + "\n")

    # The user was sucsessfully authenticated
    else:

        # Congradulating the user on a sucsessful authenrication
        print("\nNice! Zendesk has given us the go ahead to display your data for you.")
        user_authenticated = True


# Storing all possible fields of a ticket as it's related to an account, as specified by Zendesk's API documentation
ticket_fields = ["allow_attachments",   "allow_channelback",    "assignee_email",   "assignee_id",      "attribute_value_ids",  "brand_id",                 \
                "collaborator_ids",     "collaborators",        "comment",          "created_at",       "custom_fields",        "description",               \
                "due_at",               "email_cc_ids",         "email_ccs",        "external_id",      "follower_ids",         "followers",                \
                "followup_ids",         "forum_topic_id	",      "group_id",         "has_incidents",    "id",                   "is_public",                \
                "macro_id",             "macro_ids",            "metadata",         "organization_id",  "priority",             "problem_id"                \
                "raw_subject",          "recipient",            "requester",        "requester_id",     "safe_update",          "satisfaction_rating"       \
                "sharing_agreement_ids","status",               "subject",          "submitter_id",     "tags",                 "ticket_form_id"            \
                "type",                 "updated_at",           "updated_stamp",    "url",              "via",                  "via_followup_source_id",   \
                "via_id",               "voice_comment"]

# Using Python's json library to abstract the parsing of the response text to JSON
response_JSON = json.loads(response.text)

# Checking to see what ticket properties the user is interested in
user_input = ""
fields_of_interest = []

# Loopinig until the user requests to view tickets
while user_input.lower().strip() != "view":

    # Getting the users input
    user_input = input("\nIs there any specific ticket data you're interested in seeing?                    \
                        \n\nType \"fields\" to see a list of possible fields and data related to tickets.   \
                        \nType \"view\" to view your tickets."                                              \
                        ).lower().strip()

    # Checking to see if the requested field is valid
    if user_input in ticket_fields:

        # Remembering the field the user would like to see
        fields_of_interest.append(user_input)
        print("Great! We'll keep that in mind.")

    # Displaying all of the possible ticket fields on request (user types "fields")
    elif user_input == "fields":

        # Printing all possible fields
        print("\n")
        for ticket_field in ticket_fields:
            print("\t" + ticket_field)
        print("\n")


    # Handling invalid inputs
    elif user_input != "view":

        print("The input is not a ticket field, or an invalid input.")



# PROCESSING TICKET DATA BASED ON USER PREFERENCES

# Getting a list of all of the tickets from the JSON object that was returned
ticket_list_JSON = response_JSON["tickets"]

# Creating a second list which will hold ticket objects, as defined by the Ticket class in ticket.py
ticket_objects = []

# Looping through the tickets in the JSON object
for ticket in ticket_list_JSON:

    # Making the created_at and updated_at fields easier to read
    new_created_at = ticket["created_at"].replace("T", " at ").replace("Z", " ")
    new_updated_at = ticket["created_at"].replace("T", " at ").replace("Z", " ")

    # Instantiating a new ticket based on the properties of the JSON ticket
    t = Ticket(

        # Setting all of the properties of the ticket based on the JSON ticket
        ticket["id"],
        ticket["type"],
        ticket["status"],
        ticket["description"],
        new_created_at,
        new_updated_at,
        None
    )

    # Adding any addtional fields specified by the user
    for interest in fields_of_interest:

        # Storing the field name and it's data in a dictionary related to the Ticket object
        t.custom_fields.update({interest : ticket[interest]})

    # Appending the Ticket object to the list of ticket objects
    ticket_objects.append(t)



# DISPLAYING THE TICKET DATA FOR THE USER

# print(tabulate(ticket_objects))