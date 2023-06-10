import logging
from json import dumps, loads
from typing import Union
from fastapi import FastAPI, BackgroundTasks
from hubspot.crm.contacts.exceptions import ApiException

from settings import Settings, logger
from schemas import ContactSchema

from contact.contact_controller import ContactController
from api.manager import APICallManager


settings = Settings()
app = FastAPI()


@app.post("/contact/create/hubspot")
def contact_create_hubspot(contact: ContactSchema):
    """
    Endpoint that creates contact given
    :param email, str, email value for contact to store
    :param firstname, str, email value for contact to store
    :param lastname, str, email value for contact to store
    :param phone, str, email value for contact to store
    :param website, str, email value for contact to store

    """
    try:
        contact_syncer = ContactController(settings, BackgroundTasks, logger)
        contact_syncer.create_contact_hubspot(
            contact.email,
            contact.firstname,
            contact.lastname,
            contact.phone,
            contact.website,
        )

        response = {
            "message": "Contact was created",
            "data": contact,
        }

    except ApiException as e:
        logger.error("Exception when creating contact", exc_info=True)
        response = {
            "message": "Contact was not created",
            "detail": loads(e.body)
        }

    finally:
        api_call_manager = APICallManager()
        api_call_manager.save(
            endpoint='/contact/create/hubspot',
            params=contact.dict(),
            result=str(
                response
            )
        )

        return response


@app.post("/contact/sync/hubspot_clickup")
async def contact_sync_hubspot_clickup(background_tasks: BackgroundTasks):
    """
    Syncing endpoint of contacts missing between hubspot and clickup store in database with status_clickup set as false
    """
    contact_syncer = ContactController(settings, background_tasks, logger)
    contact_syncer.sync_contacts_hupspot_clickup()
    response = {
        "message": "Contacts are begin synchronized..., please check info log for more details"
    }

    api_call_manager = APICallManager()
    api_call_manager.save(
        endpoint='/contact/sync/hubspot_clickup',
        params={},
        result=str(
            response
        )
    )
    return response


@app.get("/contact")
def get_contact_hubspot():
    """
    Return HubSpot contacts from .env api key specified, use for debugging propouses
    """
    contact_syncer = ContactController(settings, None, logger)
    contacts = contact_syncer.fetch_contacts_hubspot()

    response = list(map(lambda item: item.properties, contacts))

    api_call_manager = APICallManager()
    api_call_manager.save(
        endpoint='/contact',
        params={},
        result=str(
            response
        )
    )

    return response


@app.get("/task")
def get_task_clickup():
    """
    Return Clickup tasks from .env api key specified, use for debugging propouses
    """
    contact_syncer = ContactController(settings, None, logger)
    tasks = contact_syncer.fetch_tasks_clickup()

    api_call_manager = APICallManager()
    api_call_manager.save(
        endpoint='/task',
        params={},
        result=str(
            tasks
        )
    )

    return tasks
