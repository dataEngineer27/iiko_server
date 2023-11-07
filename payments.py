from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    shift_list = crud.get_all_shifts(db=session)
    for shift in shift_list:
        if stop_event.is_set():  # Check if stop event is set
            break
        if shift.is_added == 0:
            try:
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            except:
                key = micro.login()
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)

            crud.add_shift_payments(db=session, shift_payments=shift_payments)
            crud.update_shift(db=session, id=shift.id)

    micro.logout(key=key)


# if __name__ == '__main__':
#     app()
