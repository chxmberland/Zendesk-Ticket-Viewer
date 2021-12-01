# This file performs unit tests on important functions

# The main code to be tested
import funcs  
import ticket       

# The test framework
import unittest



class Test_Auth(unittest.TestCase):

    # Testing invalid inputs
    def test_try_bad_input(self):

        # Providinig invalid inputs
        user_subdomain = "not_a_subdomain"
        user_email = "not_an_email"
        user_pass = "not_a_password"

        # Passing them to the function
        authenticated, response = funcs.try_authentication(user_subdomain, user_email, user_pass)

         # Return values of False and None incicate the user was not authenticated
        self.assertEqual((authenticated, response), (False, None))

    # Testing null inputs
    def test_try_null_input(self):

        # Providinig null inputs
        user_subdomain = None
        user_email = None
        user_pass = None

        # Passing them to the function
        authenticated, response = funcs.try_authentication(user_subdomain, user_email, user_pass)

         # Return values of False and None incicate the user was not authenticated
        self.assertEqual((authenticated, response), (False, None))



class Test_Display_Tickets(unittest.TestCase):

    # Testing invalid inputs
    def test_try_empty_input(self):

        # Providinig invalid inputs
        attribute_matrix = []
        ticket_objects = []

        # Calling the function and picking up any system output
        check_displayed = funcs.display_tickets(attribute_matrix, ticket_objects)

         # Should return False, since there are no tickets related to the users account
        self.assertEqual(check_displayed, False)

    # Testing null inputs
    def test_try_null_input(self):

        # Providinig invalid inputs
        attribute_matrix = None
        ticket_objects = None

        # Calling the function and picking up any system output
        check_displayed = funcs.display_tickets(attribute_matrix, ticket_objects)

        # Should return False, since there are no tickets related to the users account
        self.assertEqual(check_displayed, False)



class Test_Ticket_Objects(unittest.TestCase):

    def test_null_attributes(self):

        # Testing to see if a null object can be created
        t = ticket.Ticket(
            None,
            None,
            None,
            None,
            None,
            None,
            None
        )

        attributes = t.get_ticket_attributes_list()

        # Should just be a list of null values
        self.assertEqual(attributes, ["No value!", "No value!", "No value!", "No value!", "No value!", "No value!"])




# Running the unit tests
if __name__ == '__main__':
    unittest.main()