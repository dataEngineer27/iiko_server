from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    try:
        categories = micro.category_list(key=key)
    except:
        print("Key was expired")
        key = micro.login()
        print("Authenticated again")
        categories = micro.category_list(key=key)

    crud.add_categories(db=session, category_list=categories)
    # category_dict = crud.add_categories(db=session, category_list=categories)
    # return category_dict


if __name__ == '__main__':
    # new_dict_cat = app()
    app()
