import psycopg2
import random
from faker import Faker

# Crear una instancia de Faker
fake = Faker()

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname='db1M',
    user='postgres',
    password='password',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()


# Funciones para poblar las tablas
def populate_sedes(num_records):
    for _ in range(num_records):
        nombre = fake.company()[:20]
        correo = fake.email()[:20]
        cursor.execute(
            """
            INSERT INTO Sedes (nombre, correo)
            VALUES (%s, %s)
            """,
            (nombre, correo)
        )


def populate_clientes(num_records):
    dnis = set()
    while len(dnis) < num_records:
        dnis.add(random.randint(10000000, 99999999))

    for dni in dnis:
        nombre = fake.first_name()[:10]
        apellido = fake.last_name()[:15]
        cursor.execute(
            """
            INSERT INTO Clientes (DNI, nombre, apellido)
            VALUES (%s, %s, %s)
            """,
            (dni, nombre, apellido)
        )


def populate_conductores(num_records):
    cursor.execute("SELECT ID FROM Sedes")
    sedes_ids = [row[0] for row in cursor.fetchall()]

    dnis = set()
    while len(dnis) < num_records:
        dnis.add(random.randint(10000000, 99999999))

    for dni in dnis:
        correo = fake.email()[:20]
        nombre = fake.first_name()[:10]
        apellido = fake.last_name()[:25]
        sede_id = random.choice(sedes_ids)
        cursor.execute(
            """
            INSERT INTO Conductores (DNI, correo, nombre, apellido, sede_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (dni, correo, nombre, apellido, sede_id)
        )


def populate_vehiculos(num_records):
    cursor.execute("SELECT DNI FROM Conductores")
    conductores_dnis = [row[0] for row in cursor.fetchall()]

    matriculas = set()
    while len(matriculas) < num_records:
        matriculas.add(random.randint(1000000, 9999999))

    for matricula in matriculas:
        marca = fake.company()[:10]
        modelo = fake.word()[:15]
        anio_func = random.randint(1990, 2023)
        conductor_dni = random.choice(conductores_dnis)
        cursor.execute(
            """
            INSERT INTO Vehiculos (Matricula, marca, modelo, anio_func, conductor_dni)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (matricula, marca, modelo, anio_func, conductor_dni)
        )


def populate_estaciones(num_records):
    unique_names = set()
    while len(unique_names) < num_records:
        unique_names.add(fake.city()[:15])

    for nombre in unique_names:
        ubicacion = fake.state_abbr()[:10]
        cursor.execute(
            """
            INSERT INTO Estaciones (nombre, ubicacion)
            VALUES (%s, %s)
            """,
            (nombre, ubicacion)
        )


def populate_r_encurso(num_records):
    cursor.execute("SELECT nombre FROM Estaciones")
    estaciones_nombres = [row[0] for row in cursor.fetchall()]

    for _ in range(num_records):
        estacion_inicio = random.choice(estaciones_nombres)
        n_embarque_s = random.randint(1, 100)
        hora_s = fake.time()
        reporte = fake.text(max_nb_chars=100)
        cursor.execute(
            """
            INSERT INTO R_EnCurso (fecha, estacion_inicio, n_embarque_s, hora_s, reporte)
            VALUES (CURRENT_DATE, %s, %s, %s, %s)
            """,
            (estacion_inicio, n_embarque_s, hora_s, reporte)
        )


def populate_boletos(num_records):
    cursor.execute("SELECT ID FROM R_EnCurso")
    rutas_ids = [row[0] for row in cursor.fetchall()]

    boletos_ids = set()
    while len(boletos_ids) < num_records:
        boletos_ids.add(random.randint(100000, 999999))

    for id_boleto in boletos_ids:
        ruta_id = random.choice(rutas_ids)
        categoria = f'Categoria {random.randint(1, 3)}'[:10]
        n_asiento = random.randint(1, 50)
        costo = random.randint(10, 100)
        cursor.execute(
            """
            INSERT INTO Boletos (id_boleto, ruta_id, categoria, n_asiento, costo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_boleto, ruta_id, categoria, n_asiento, costo)
        )


def populate_compras(num_records):
    cursor.execute("SELECT id_boleto, ruta_id FROM Boletos")
    boletos = cursor.fetchall()
    cursor.execute("SELECT DNI FROM Clientes")
    clientes_dnis = [row[0] for row in cursor.fetchall()]

    unique_combinations = set()
    for _ in range(num_records):
        while True:
            boleto = random.choice(boletos)
            cliente_id = random.choice(clientes_dnis)
            if (boleto[0], boleto[1], cliente_id) not in unique_combinations:
                unique_combinations.add((boleto[0], boleto[1], cliente_id))
                break
        metodo_pago = fake.credit_card_provider()[:10]
        cursor.execute(
            """
            INSERT INTO Compras (boleto_id, ruta_id, cliente_id, metodo_pago)
            VALUES (%s, %s, %s, %s)
            """,
            (boleto[0], boleto[1], cliente_id, metodo_pago)
        )


def populate_r_finalizadas(num_records):
    cursor.execute("SELECT nombre FROM Estaciones")
    estaciones_nombres = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT Matricula FROM Vehiculos")
    vehiculos_mats = [row[0] for row in cursor.fetchall()]

    for _ in range(num_records):
        estacion_inicio = random.choice(estaciones_nombres)
        estacion_final = random.choice(estaciones_nombres)
        vehiculo_mat = random.choice(vehiculos_mats)
        hora_s = fake.time()
        hora_l = fake.time()
        n_embarque_s = random.randint(1, 100)
        n_embarque_l = random.randint(1, 100)
        fecha = fake.date_this_year()
        duracion = fake.time()
        ingresos_gen = random.randint(1000, 10000)
        distancia = random.randint(10, 500)
        cursor.execute(
            """
            INSERT INTO R_Finalizadas (estacion_inicio, estacion_final, vehiculo_mat, hora_s, hora_l, n_embarque_s, n_embarque_l, fecha, duracion, ingresos_gen, distancia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (estacion_inicio, estacion_final, vehiculo_mat, hora_s, hora_l, n_embarque_s, n_embarque_l, fecha, duracion,
             ingresos_gen, distancia)
        )


# Llamar a las funciones para poblar las tablas
populate_sedes(10)
populate_clientes(1000000)
populate_conductores(10000)
populate_vehiculos(10000)
populate_estaciones(10)
populate_r_encurso(10000)
populate_boletos(1000000)
populate_compras(1000000)
populate_r_finalizadas(10000)

# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

