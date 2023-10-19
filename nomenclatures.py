from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.authiiko()
    try:
        nomenclatures = micro.nomenclature_list(key=key)
    except:
        key = micro.authiiko()
        nomenclatures = micro.nomenclature_list(key=key)

    # new_dict_cat = nomenclature_categories.new_dict_cat
    crud.add_nomenclatures(db=session, nomenclature_list=nomenclatures)


if __name__ == '__main__':
    app()
