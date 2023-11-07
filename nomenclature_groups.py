from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        nomenclature_groups = micro.nomenclature_groups(key=key)
    except:
        key = micro.login()
        nomenclature_groups = micro.nomenclature_groups(key=key)

    crud.add_groups(db=session, group_list=nomenclature_groups)
    micro.logout(key=key)


# if __name__ == '__main__':
#     app()
