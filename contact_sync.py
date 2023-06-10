from integration.helpers import HubspotHelper, ClickupHelper
from contact.manager import ContactManager

class ContactSyncer:

    def __init__(self, settings, background_task, logger) -> None:
        self.hubspot_helper = HubspotHelper(settings.hubspot_access_token)
        self.clickup_helper = ClickupHelper(settings.clickup_access_token, settings.clickup_list_id)
        self.contact_manager = ContactManager()
        self.background_task_manager = background_task
        self.logger = logger

    def create_contact_hubspot(self, email: str, firstname: str, lastname: str, phone: str, website: str):
        self.hubspot_helper.create_contact(email, firstname, lastname, phone, website)
        self.contact_manager.save(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            website=website,
            status_clickup=False
        )
        self.logger.info(
            f"Contact {email} has been stored on HubSpot"
        )
        
    def sync_contacts_hupspot_clickup(self):
        
        contacts = self.contact_manager.read(
            {
                "status_clickup": False
            }
        )
        for contact in contacts:
            self.background_task_manager.add_task(
                self._sync_task_background,
                contact
            )
        

    def _sync_task_background(self, contact):
        try:
            self.clickup_helper.create_task(
                contact.email,
                contact.firstname,
                contact.lastname,
                contact.phone,
                contact.website
            )
            self.contact_manager.update(
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
            self.logger.info(
                f"Contact {contact.email} has been synced to Clickup's tasks"
            )
        except Exception as e:
            if getattr(e, "message", None) and getattr(e, "details", None):
                self.logger.error(
                    f"Contact {contact.email} can not be synced because {e.message} details {e.details}"
                )
            else:
                self.logger.error(
                    f"Contact {contact.email} can not be synced", exc_info=True
                )
        

        