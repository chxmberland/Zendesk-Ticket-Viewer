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



# Importing the functions necessary to make the program work from funcs.py
from funcs import *

# GETTING USER PREFERENCES

# Greeting the user
print("\nHello! How are you? Don't bother answering that, I'm a computer." \
    + "\nI'm here to help you view the tickets related to your Zendesk account!" \
    + "\nWe make use of Zendesk's RESTful API which requires authetication on your end, so we'll need some of your information to get started.")

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

# Authenticating the user and requesting data from Zendesks API
authenticated   = False
response        = None
while not authenticated:
    authenticated, response = try_authentication()

# Using Python's JSON library to abstract the parsing of the response text to JSON
response_JSON = json.loads(response.text)

# Checking to see what ticket properties the user is interested in
user_input = ""
fields_of_interest = []

# Getting the users input
valid_inputs = ["fields", "view", ticket_fields]
question = "\nIs there any specific ticket data you're interested in seeing?"                   \
         + "\n\nType \"fields\" to see a list of possible fields and data related to tickets."  \
         + "\nType \"view\" to view your tickets."

# Looping until the user requests to view tickets
while user_input.lower().strip() != "view":

    # Getting the users preferences
    user_input = get_user_pref(valid_inputs, question)

    # Checking to see if the requested field is valid
    if user_input in valid_inputs[2]:

        # Remembering the field the user would like to see
        fields_of_interest.append(user_input)
        print("\nGreat! I'll keep that in mind.")

    # Displaying all of the possible ticket fields on request (user types "fields")
    elif user_input == "fields":

        # Printing all possible fields
        print("\n")
        for ticket_field in ticket_fields:
            print("\t" + ticket_field)
        print("\n")



# PROCESSING TICKET DATA BASED ON USER PREFERENCES

# Getting the JSONN data
ticket_list_JSON = response_JSON["tickets"]

# Creating ticket data from the JSON returned by Zendesk's API
ticket_objects = create_tickets(ticket_list_JSON, fields_of_interest)



# DISPLAYING THE TICKET DATA FOR THE USER

# Creating an iterable of ticket attribute lists
attribute_matrix = []
for ticket in ticket_objects:

    # Storing a list of the attributes of each ticket in a larger list for tabulation
    attribute_matrix.append(ticket.get_ticket_attributes_list())

# Displaying the tickets
display_tickets(attribute_matrix)