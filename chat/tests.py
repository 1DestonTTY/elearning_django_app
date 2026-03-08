from django.test import TestCase
from django.urls import reverse

class ChatAppTests(TestCase):
    def test_chat_room_view_loads_correctly(self):
        """
        Tests that the chat room page loads successfully and 
        dynamically injects the correct room_name into the HTML.
        """
        #generate the url for a chat room with id 99
        url = reverse('room', args=['99'])
        
        #simulate a user visiting that url
        response = self.client.get(url)
        
        #verify the server respond with 200 OK success code
        self.assertEqual(response.status_code, 200)
        
        #verify that the HTML output actually contains the dynamic room id
        self.assertContains(response, 'Room ID: 99')