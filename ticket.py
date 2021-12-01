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
    def print_ticket(self):
        
        # Storing the additional fields in a variable
        custom_fields_str = ""
        for attribute, value in self.custom_fields.items():
            custom_fields_str += attribute + ":\n" +    \
                                 "---------------\n" +  \
                                 str(value) +           \
                                 "\n\n\n"

        print("\n\nTicket id:\n",             
              "---------------\n",      
              self.id,                  
              "\n\n\n",
              "Ticket type:\n",
              "---------------\n",
              self.type,
              "\n\n\n",
              "Ticket status:\n",
              "---------------\n",
              self.status,
              "\n\n\n",
              "Ticket description:\n",
              "---------------\n",
              self.description,
              "\n\n\n",
              "Created at:\n",
              "---------------\n",
              self.created_at,
              "\n\n\n",
              "Updated at:\n",
              "---------------\n",
              self.updated_at, 
              "\n\n\n",
              "---------------\n",
              "Custom Fields: \n",
              "---------------\n\n",
              self.custom_fields,
              "\n\n" 
              )



    # Storing the attributes of a ticket in a list
    def get_ticket_attributes_list(self):

        attribute_list = []

        # Looping through each attritbute and it's related vale of a Ticket using Python's inbuilt __dict__ method
        for attribute, value in self.__dict__.items():

            # Handling null values
            if value == None:
                attribute_list.append("No value!")

            # Taking only the first 30 characters of the description to simplify the viewing (more availble on user request)
            elif attribute == "description":
                attribute_list.append(value[0 : 30] + "...")
            
            # If the current attribute is not the description or custom_fields (printed later)
            elif attribute != "custom_fields":
                attribute_list.append(value)

        return attribute_list

