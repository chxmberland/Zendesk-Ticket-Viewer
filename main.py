#   
#   Author: Benjamin Chamberland
#   Date: Thursday, November 26th
#
#   Description:
#       
#       This program will use Zendesk's RESTful API to GET ticket data from my Zendesk account. It will then process that data
#       and display it in a clean and convenient manner in the shell.
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

# Importinig a custom tickey class
from ticket import Ticket

# Storing the information needed to make requests on an accounts behalf
email = "becha9260@gmail.com"
password = ""
subdomain = "zccbenccodingchallenge"
url = "https://" + subdomain + ".zendesk.com/api/v2/tickets.json"

# Storing all possible ticket fields
ticket_fields = ["allow_attachments",   "allow_channelback",    "assignee_email",   "assignee_id",      "attribute_value_ids",  "brand_id",                 \
                "collaborator_ids",     "collaborators",        "comment",          "created_at",       "custom_fields",        "description",               \
                "due_at",               "email_cc_ids",         "email_ccs",        "external_id",      "follower_ids",         "followers",                \
                "followup_ids",         "forum_topic_id	",      "group_id",         "has_incidents",    "id",                   "is_public",                \
                "macro_id",             "macro_ids",            "metadata",         "organization_id",  "priority",             "problem_id"                \
                "raw_subject",          "recipient",            "requester",        "requester_id",     "safe_update",          "satisfaction_rating"       \
                "sharing_agreement_ids","status",               "subject",          "submitter_id",     "tags",                 "ticket_form_id"            \
                "type",                 "updated_at",           "updated_stamp",    "url",              "via",                  "via_followup_source_id",   \
                "via_id",               "voice_comment"]

# Using Python's requests and HTTPBasicAuth library to abstract the data request from Zendesk's API using basic authentication
response = requests.get(url, auth = HTTPBasicAuth(email, password))

# If the response is valid
if (response.status_code == 200):

    # Using Python's json library to abstract the parsing of the response text to JSON
    response_JSON = json.loads(response.text)


    #Checking to see what fields to see what the user is interested in
    user_input = ""
    fields_of_interest = []

    while user_input.lower().strip() != "view":

        # Getting the users input
        user_input = input("Are there any additional fields you're interested in seeing?    \
                            \n\nType \"fields\" to see a list of possible fields.           \
                            \nType \"view\" to view your tickets."                          \
                            ).lower().strip()

        # Checking to see if it is valid
        if user_input in ticket_fields:

            fields_of_interest.append(user_input)
            print("Great! We'll keep that in mind.")

        # Displaying all of the possible ticket fields on request
        elif user_input == "fields":

            # Printing all possible fields
            for ticket_field in ticket_fields:
                print("\t" + ticket_field)

        # Handling invalid inputs
        elif user_input != "view":

            print("That's not a field.")


    # Getting a list of all of the tickets from the JSON object that was returned
    ticket_list_JSON = response_JSON["tickets"]

    # Creating a second list which will hold ticket objects, as defined by the class on line 29
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

        # Adding any addtional specified fields
        for interest in fields_of_interest:

            t.custom_fields.update({interest : ticket[interest]})

        # Appending the ticket to the list of ticket objects
        ticket_objects.append(t)

# The response is invalid
else:

    # Printing the arror
    print("Error")
