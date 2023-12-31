from database import SessionLocal
from api.models import APICalls

class APICallManager:

    def __init__(self) -> None:
        self.db = SessionLocal()

    def read(self, filters):
        """
        Returns APICall objects from filters dict object
        :param filters dict, Dict object with kwargs values for filtering APICalls Result set
        return List
        """
        return self.db.query(
            APICalls
        ).filters(**filters)

    def save(self, endpoint, params, result):
        """
        Saves an APICall object on the database given the values
        :param endpoint, str, endpoint value from api call executed
        :param params, dict, params in the request done
        :param result, str, result given by this application
        return APICall object
        """
        db_item = APICalls(
            endpoint=endpoint,
            params=params,
            result=result,
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item