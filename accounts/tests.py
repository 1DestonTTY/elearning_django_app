from django.test import TestCase
from .models import User

class UserAPITest(TestCase):
    def setUp(self):
        #run before every test to set up dummy data
        self.user = User.objects.create_user(
            username='testapiuser',
            password='testpassword123',
            real_name='API Test User',
            email='api@test.com'
        )

    def test_get_users_api(self):
        #test client to visit the api url
        response = self.client.get('/api/users/')
        
        #check if the server respond with a success code 200 OK
        self.assertEqual(response.status_code, 200)
        
        #check if dummy user's data actually showed up in the json response
        self.assertContains(response, 'testapiuser')
        self.assertContains(response, 'API Test User')

        