from database import SessionLocal
from contact.models import Contact

class ContactManager:

    def __init__(self) -> None:
        self.db = SessionLocal()

    def read(self, filters: dict = {}):
        """
        Returns Contact objects from filters dict object
        :param filters dict, Dict object with kwargs values for filtering Contacts Result set
        return List
        """
        return self.db.query(
            Contact
        ).filter_by(**filters).all()

    def update(self, filters: dict, new_values: dict):
        """
        Updates an existing contact object in the database given a kwargs dict
        :param filters, dict, values to filter contact required
        :param new_values, dict, values to set on the contact
        """
        contact_object = self.db.query(Contact).filter_by(
            **filters
        ).first()

        for key in new_values:
            setattr(contact_object, key, new_values[key])
            
        self.db.commit()

        return contact_object

    def save(self, email: str, firstname: str, lastname: str, phone: str, website: str, status_clickup: bool):
        """
        Stores a contact object in the database given the values
        :param email, str, email value for contact to store
        :param firstname, str, email value for contact to store
        :param lastname, str, email value for contact to store
        :param phone, str, email value for contact to store
        :param website, str, email value for contact to store
        :param status_clickup, bool, boolean flag for sync with clickup
        """
        contact_object=Contact(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            website=website,
            status_clickup=status_clickup
        )
        self.db.add(contact_object)
        self.db.commit()
        self.db.refresh(contact_object)
        return contact_object