from database import engine, session
import requests
import crud
import micro


def app():
    key = micro.authiiko()
    shift_id_list = crud.get_all_payment_shifts(db=session)
    for i in shift_id_list:
        if i.is_added == 0:
            try:
                get_withdraw_shifts = micro.get_shift_withdraw(key=key, session_id=i.id)
            except:
                key = micro.authiiko()
                get_withdraw_shifts = micro.get_shift_withdraw(key=key, session_id=i.id)
            crud.add_withdraw_shifts(db=session, lst=get_withdraw_shifts)
            crud.update_shift_ids(db=session, id=i.id)


if __name__ == '__main__':
    app()
