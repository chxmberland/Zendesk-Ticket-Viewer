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

    def print_ticket():

        fart = True
        # Define how to print a ticket here