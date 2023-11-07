from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        categories = micro.category_list(key=key)
    except:
        key = micro.login()
        categories = micro.category_list(key=key)

    crud.add_categories(db=session, category_list=categories)
    micro.logout(key=key)


# if __name__ == '__main__':
#     # new_dict_cat = app()
#     app()
