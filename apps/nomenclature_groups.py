from database import session
import micro
import crud


def app():
    key = micro.authiiko()
    try:
        nomenclature_groups = micro.nomenclature_groups(key=key)
    except:
        key = micro.authiiko()
        nomenclature_groups = micro.nomenclature_groups(key=key)

    crud.add_groups(db=session, group_list=nomenclature_groups)


if __name__ == '__main__':
    app()
