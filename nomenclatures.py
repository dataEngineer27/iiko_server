from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        nomenclatures = micro.nomenclature_list(key=key)
    except:
        key = micro.login()
        nomenclatures = micro.nomenclature_list(key=key)

    crud.add_nomenclatures(db=session, nomenclature_list=nomenclatures)
    micro.logout(key=key)


# if __name__ == '__main__':
#     app()
