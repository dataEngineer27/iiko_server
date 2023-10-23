from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    try:
        nomenclature_groups = micro.nomenclature_groups(key=key)
    except:
        print("Key was expired")
        key = micro.login()
        print("Authenticated again")
        nomenclature_groups = micro.nomenclature_groups(key=key)

    crud.add_groups(db=session, group_list=nomenclature_groups)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
