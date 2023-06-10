from integration.helpers import HubspotHelper, ClickupHelper
from contact.manager import ContactManager

class ContactController:
    """
    Controller layer to communicate Integration component with RESTful Layer, it is responsible to fetch, sync and create contacts
    from hubspot and clickup task lists
    """

    def __init__(self, settings, background_task, logger) -> None:
        """
        Constructor for ContactController to initiate dependencies
        """
        self.__hubspot_helper = HubspotHelper(settings.hubspot_access_token)
        self.__clickup_helper = ClickupHelper(settings.clickup_access_token, settings.clickup_list_id)
        self.__contact_manager = ContactManager()
        self.__background_task_manager = background_task
        self.__logger = logger

    def create_contact_hubspot(self, email: str, firstname: str, lastname: str, phone: str, website: str):
        """
        Creates hubspot contact using hupspot helper implementation, and creates a contact object on sqlalchemy orm
        to flag not synced items
        :param email, str, Email value for contact to be stored
        :param firstname, str, firstname value for contact to be stored
        :param lastname, str, lastname value for contact to be stored
        :param phone, str, phone value for contact to be stored
        :param website, str, website value for contact to be stored
        """
        self.__hubspot_helper.create_contact(email, firstname, lastname, phone, website)
        self.__contact_manager.save(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            website=website,
            status_clickup=False
        )
        self.__logger.info(
            f"Contact {email} has been stored on HubSpot"
        )
        
    def sync_contacts_hupspot_clickup(self):
        """
        Wrapper method for sync contacts with clickup from localdatabase filtering status_clickup contacts in true,
        keeps a thread in backgroup until finish all contacts to be synced
        """
        contacts = self.__contact_manager.read(
            {
                "status_clickup": False
            }
        )
        for contact in contacts:
            self.__background_task_manager.add_task(
                self._sync_task_background,
                contact
            )
        

    def _sync_task_background(self, contact):
        """
        Create task on clickup list and updates related object on sqlalchemy model and database
        :param contact, Contact object with values
        """
        try:
            self.__clickup_helper.create_task(
                contact.email,
                contact.firstname,
                contact.lastname,
                contact.phone,
                contact.website
            )
            self.__contact_manager.update(
                {
                    "email" : contact.email,
                    "firstname" : contact.firstname,
                    "lastname" : contact.lastname,
                    "phone" : contact.phone,
                    "website" : contact.website,
                },
                {
                    "status_clickup": True
                }
            )
            self.__logger.info(
                f"Contact {contact.email} has been synced to Clickup's tasks"
            )
        except Exception as e:
            if getattr(e, "message", None) and getattr(e, "details", None):
                self.__logger.error(
                    f"Contact {contact.email} can not be synced because {e.message} details {e.details}"
                )
            else:
                self.__logger.error(
                    f"Contact {contact.email} can not be synced", exc_info=True
                )
        

    def fetch_contacts_hubspot(self):
        """
        Fetch all contacts store in user for api key in .env file
        return List of publicobject
        """
        return self.__hubspot_helper.fetch_contacts()

    def fetch_tasks_clickup(self):
        """
        Fetch all tasks from clickup in the specified list
        return List of dicts
        """
        return self.__clickup_helper.fetch_tasks()
        