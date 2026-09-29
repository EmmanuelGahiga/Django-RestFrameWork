from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class HomePageTest(APITestCase):

    def test_apis(self):
        response = self.client.get(
            reverse("details_modify_delete_post", kwargs={"pk": 9})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
