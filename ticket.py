# Creating a ticket class, which will store the relevant information about a ticket
class Ticket:



    # Defining the properties of a ticket
    def __init__(self, id, type, status, description, created_at, updated_at, custom_fields):

        self.id                     = id
        self.type                   = type
        self.status                 = status
        self.description            = description
        self.created_at             = created_at
        self.updated_at             = updated_at
        self.custom_fields          = {}



    # Printing a simplified version of the data contained within a ticket
    def print_minimized_ticket(self):

        print(self.id,          "\t\t",     \
              self.type,        "\t\t",     \
              self.status,      "\t\t",     \
              self.description, "...\t\t",  \
              self.created_at,  "\t\t",     \
              self.updated_at)



    # Storing the attributes of a ticket in a list
    def get_ticket_attributes_list(self):

        attribute_list = []

        # Looping through each attritbute and it's related vale of a Ticket using Python's inbuilt __dict__ method
        for attribute, value in self.__dict__.items():

            # Taking only the first 30 characters of the description to simplify the viewing (more availble on user request)
            if attribute == "description":
                attribute_list.append(value[0 : 30] + "...")
            
            # If the current attribute is not the description or custom_fields (printed later)
            elif attribute != "custom_fields":
                attribute_list.append(value)

        return attribute_list

