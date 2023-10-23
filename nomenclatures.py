from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    try:
        nomenclatures = micro.nomenclature_list(key=key)
    except:
        print("Key was expired")
        key = micro.login()
        print("Authenticated again")
        nomenclatures = micro.nomenclature_list(key=key)

    # new_dict_cat = nomenclature_categories.new_dict_cat
    crud.add_nomenclatures(db=session, nomenclature_list=nomenclatures)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
