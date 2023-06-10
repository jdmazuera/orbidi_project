
import requests
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException


class HubspotHelper:

    def __init__(self, access_token) -> None:
        """
        Constructor for initiate HubSpot Helper
        param: String, access token to connect to HubSpot API
        """
        self.hubspot_api = HubSpot(access_token=access_token)

    def create_contact(self, email: str, firstname: str, lastname: str, phone: str, website: str):
        """
        Creates contact on hubspot platform
        param: email, email from contact to be created
        param: firstname, first name of contact to be created
        param: lastname, last name of contact to be created
        param: phone, phone of contact to be created
        param: website, website of contact to be created
        """

        contact_object = SimplePublicObjectInput(
            properties={
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "phone": phone,
                "website": website,
            }
        )
        response = self.hubspot_api.crm.contacts.basic_api.create(
            simple_public_object_input=contact_object
        )

        return response

    def fetch_contacts(self):
        """
        Fetchs contacts on hubspot platform
        """
        response = self.hubspot_api.crm.contacts.get_all()

        return response


class ClickupHelper:

    def __init__(self, access_token, list_id) -> None:
        self.url = "https://api.clickup.com/api/v2/list/{}/task".format(
            list_id)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }

    def create_task(self, email: str, firstname: str, lastname: str, phone: str, website: str):
        """
        Creates tasks on clickup platform list
        param: email, email from contact to be created
        param: firstname, first name of contact to be created
        param: lastname, last name of contact to be created
        param: phone, phone of contact to be created
        param: website, website of contact to be created
        """
        payload = {
            "name": email,
            "description": f"{firstname} {lastname} {phone} {website}",
        }

        response = requests.post(
            self.url,
            json=payload,
            headers=self.headers,
        )

        response_json = response.json()

        if not response_json.get('id'):
            raise Exception(
                f"Please check payload data, it is not compatible with clickup {response.json()}")

        return response_json

    def fetch_tasks(self):
        """
        Fetchs tasks on clickup platform
        """
        response = requests.get(
            self.url,
            headers=self.headers,
        )

        response_json = response.json()

        return response_json
