from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.login()
    try:
        nomenclatures = micro.nomenclature_list(key=key)
    except:
        key = micro.login()
        nomenclatures = micro.nomenclature_list(key=key)

    crud.add_nomenclatures(db=session, nomenclature_list=nomenclatures)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
