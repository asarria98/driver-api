import sqlite3
import json
from fastapi import FastAPI, HTTPException
from driver import Driver

# Crear la instancia de la API
app = FastAPI()

# Función para obtener una conexión a la base de datos
def get_db_connection():
    return sqlite3.connect('../db/Formula1.sqlite')

@app.get("/drivers/{name}")
def get_by_name(name: str):
    # Conectar a la base de datos
    conexion = get_db_connection()
    cursor = conexion.cursor()

    try:
        # Consulta SQL segura usando parámetros
        consulta = "SELECT driverId, surname, nationality FROM drivers WHERE forename = ?"
        cursor.execute(consulta, (name,))
        lista = cursor.fetchall()

        if not lista:
            raise HTTPException(status_code=404, detail="Driver not found")

        # Mapeo de los resultados a diccionarios
        claves = ["id", "Surname", "Nationality"]
        lista_diccionarios = [dict(zip(claves, valor)) for valor in lista]

        # Cerrar la conexión
        conexion.close()

        # Retornar la lista de diccionarios como JSON
        return lista_diccionarios

    except sqlite3.Error as e:
        # Manejo de errores en la consulta a la base de datos
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

    finally:
        # Asegurarse de que la conexión siempre se cierre
        conexion.close()

@app.post("/drivers/")
def create_driver(driver : Driver):

    conexion = get_db_connection()
    consulta = f"""
    INSERT INTO drivers (driverId, driverRef, number, code, forename, surname, dob, nationality, url)
    VALUES ({driver.driverId}, '{driver.driverRef}', {driver.number}, '{driver.code}', 
    '{driver.forename}', '{driver.surname}', '{driver.dob}', '{driver.nationality}', '{driver.url}');
    """    
    cursor = conexion.cursor()

    try:
        cursor.execute(consulta)
        print(f"Driver: {driver.forename} {driver.surname} successfully created.")
        conexion.commit()
        conexion.close()

    except sqlite3.Error as e:
        # Manejo de errores en la consulta a la base de datos
        raise HTTPException(status_code=500, detail="Database error: " + str(e))



