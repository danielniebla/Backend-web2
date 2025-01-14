from mysql.connector import Error
from ..connection import connection,disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/schedules",
    tags=["Horarios"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.post("/addDates")
def addDates(idDoctor:int, fecha:str, hora:str,status:bool):
    connect, cursor = connection()
    try:
        query = ("INSERT INTO horarios (idDoctor, fecha, hora, status) "
                 "SELECT %s, %s, %s, %s FROM dual "
                 "WHERE NOT EXISTS (SELECT 1 FROM horarios WHERE fecha = %s AND hora = %s);")
        val =(idDoctor, fecha, hora, status, fecha, hora)
        cursor.execute(query,val)
        connect.commit()
        #record = cursor.rowcount()
        #if record is not None:
        return {"success": "Insertado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.get("/availableDates")
def availableDates(idDoctor:str, fecha:str):
    connect, cursor = connection()
    try:
        query = ("select * from horarios where idDoctor="+idDoctor+" and status=true and fecha>=CURRENT_DATE()  and fecha=('"+fecha+"') order by hora;")
        print(query)
        #val = (idDoctor)
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idHorario, idDoctor, fecha, hora, status = record
                date_dict = {
                    "id": idHorario,
                    "idDoctor": idDoctor,
                    "fecha": fecha,
                    "hora": hora,
                    "status": status
                }
                dates_list.append(date_dict)

            return {"availableDates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.delete("/deleteDates")
def deleteDates(idHorario:str):
    connect, cursor = connection()
    try:
        query = ("delete from horarios where idhorarios=%s;")
        val = (idHorario,)
        cursor.execute(query, val)
        connect.commit()
        # record = cursor.rowcount()
        # if record is not None:
        return {"success": "Eliminado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


