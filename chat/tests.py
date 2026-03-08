from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatAppTests(TestCase):
    def test_chat_room_view_loads_correctly(self):
        #create a temporary user for the test
        user = User.objects.create_user(username='testuser', password='password123')
        
        #log the test client in so it can pass the @login_required guard
        self.client.login(username='testuser', password='password123')

        #generate the url for a chat room with id 99
        url = reverse('room', args=['99'])
        
        #simulate the authenticated user visiting that url
        response = self.client.get(url)
        
        #verify the server responds with 200 OK success code
        self.assertEqual(response.status_code, 200)
        
        #verify that the HTML output actually contains the dynamic room id
        self.assertContains(response, 'Room ID: 99')