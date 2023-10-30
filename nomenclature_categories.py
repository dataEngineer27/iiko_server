from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.login()
    try:
        categories = micro.category_list(key=key)
    except:
        key = micro.login()
        categories = micro.category_list(key=key)

    crud.add_categories(db=session, category_list=categories)


if __name__ == '__main__':
    # new_dict_cat = app()
    app()
