from rest_framework.views import status
from wger.core.tests.base_testcase import WorkoutManagerTestCase


class SocialLoginTest(WorkoutManagerTestCase):
    """ Test social login """

    def test_social_login(self):
        """ Tests for social login """

        url = '/api/v2/social_auth'

        # Test for social login

        data = {
            "provider": "twitter",
            "access_token": "4923828459-zuazzO65xcgaZi9rVzYNUFYjETmNUqSuUNB1Qtt",
            "access_token_secret": "Cxb0tuX6jqFsfFNs8kxK3h0Y7yg4FlvcXhENkghgGWSGS"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test for invalid provider
        data = {
            "provider": "invalid-provider",
            "access_token": "4923828459-zuazzO65xcgaZi9rVzYNUFYjETmNUqSuUNB1Qtt",
            "access_token_secret": "Cxb0tuX6jqFsfFNs8kxK3h0Y7yg4FlvcXhENkghgGWSGS"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for an invalid access token
        data = {
            "provider": "twitter",
            "access_token": "4923828459zuazzO65xcgaZi9rVzYNUFYjETmNUqSuUNB1Qtt",
            "access_token_secret": "Cxb0tuX6jqFsfFNs8kxK3h0Y7yg4FlvcXhENkghgGWSGS"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for missing backend
        data = {
            "provider": "instagram",
            "access_token": "ya29.GlsgB_bSQCDlzNkSBiCu1gTMfrEd2wIgXwaL5Cr_JcnYlr2edrtA"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for invalid Http request
        data = {
            "provider": "facebook",
            "access_token": ("EAAnTZBwlORIwBAJtZAuXboX2bKJzMIukSpH434DvAUq"
                             "RkYBuLb7Q6IaWqUMUGZChUPQS3gEtus9JA9viAt0zy5E"
                             "jEFWIj8CDuJx1cexV1I5BXKiRW2HXu7ghgiZBTfaeawz3"
                             "v7aBZBTAB0RYO2JY7PZBb9mSXeAJypzZC6Woll78Q6ZCuI"
                             "79ehRXNekErj1edAb0T2xw9hBVHwZDZD")
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
