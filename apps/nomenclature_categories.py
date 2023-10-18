from database import session
import micro
import crud


def app():
    key = micro.authiiko()
    try:
        categories = micro.category_list(key=key)
    except:
        key = micro.authiiko()
        categories = micro.category_list(key=key)

    crud.add_categories(db=session, category_list=categories)
    # category_dict = crud.add_categories(db=session, category_list=categories)
    # return category_dict


if __name__ == '__main__':
    # new_dict_cat = app()
    app()
