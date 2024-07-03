from faker import Faker
import psycopg2
import random

fake = Faker(['es_ES', 'fr_FR', 'it_IT', 'de_DE'])

def get_connection():
    db_params = {
        'host': 'localhost',
        'database': 'db100mil',
        'user': 'postgres',
        'password': 'password',
        'port': '5432',
    }
    connection = psycopg2.connect(**db_params)
    connection.autocommit = True
    print("¡Conexión exitosa a la base de datos!")
    return connection, connection.cursor()

def generate_sedes():
    nombre = fake.company()[:20]
    correo = fake.email()[:20]
    return {
        'nombre': nombre,
        'correo': correo
    }

def generate_unique_dni(existing_dnis):
    while True:
        dni = ''.join(random.choice('123456789') for _ in range(8))
        if dni not in existing_dnis:
            existing_dnis.add(dni)
            return dni

def generate_clientes(existing_dnis):
    dni = generate_unique_dni(existing_dnis)
    nombre = fake.first_name()[:10]
    apellido = fake.last_name()[:15]
    return {
        'DNI': dni,
        'nombre': nombre,
        'apellido': apellido
    }

def generate_conductores(existing_dnis, sede_id):
    dni = generate_unique_dni(existing_dnis)
    correo = fake.email()[:20]
    nombre = fake.first_name()[:10]
    apellido = fake.last_name()[:25]
    return {
        'DNI': dni,
        'correo': correo,
        'nombre': nombre,
        'apellido': apellido,
        'sede_id': sede_id
    }

def generate_unique_matricula(existing_matriculas):
    while True:
        matricula = fake.license_plate()[:10]
        if matricula not in existing_matriculas:
            existing_matriculas.add(matricula)
            return matricula

def generate_vehiculos(existing_matriculas, dni):
    matricula = generate_unique_matricula(existing_matriculas)
    marca = fake.company()[:10]
    modelo = fake.word()[:15]
    anio_func = fake.year()
    return {
        'Matricula': matricula,
        'marca': marca,
        'modelo': modelo,
        'anio_func': anio_func,
        'conductor_dni': dni
    }

def generate_estaciones():
    nombre = fake.city()[:15]
    ubicacion = fake.address()[:10]
    return {
        'nombre': nombre,
        'ubicacion': ubicacion
    }

def generate_r_finalizadas(estacion_inicio, estacion_final):
    vehiculo_mat = fake.license_plate()[:10]
    hora_s = fake.time()
    hora_l = fake.time()
    n_embarque_s = random.randint(1, 100)
    n_embarque_l = random.randint(1, 100)
    fecha = fake.date_this_year()
    duracion = None
    ingresos_gen = random.randint(100, 10000)
    distancia = random.randint(1, 1000)
    return {
        'estacion_inicio': estacion_inicio,
        'estacion_final': estacion_final,
        'vehiculo_mat': vehiculo_mat,
        'hora_s': hora_s,
        'hora_l': hora_l,
        'n_embarque_s': n_embarque_s,
        'n_embarque_l': n_embarque_l,
        'fecha': fecha,
        'duracion': duracion,
        'ingresos_gen': ingresos_gen,
        'distancia': distancia
    }

def generate_r_encurso(estacion_inicio):
    fecha = fake.date_this_year()
    n_embarque_s = random.randint(1, 100)
    hora_s = fake.time()
    reporte = fake.text(max_nb_chars=100)
    return {
        'fecha': fecha,
        'estacion_inicio': estacion_inicio,
        'n_embarque_s': n_embarque_s,
        'hora_s': hora_s,
        'reporte': reporte
    }

def generate_unique_boleto_id(existing_boletos):
    while True:
        id_boleto = random.randint(1, 1000000)
        if id_boleto not in existing_boletos:
            existing_boletos.add(id_boleto)
            return id_boleto

def generate_boletos(existing_boletos, ruta_id):
    id_boleto = generate_unique_boleto_id(existing_boletos)
    categoria = random.choice(['vip', 'estandar', 'premium'])[:10]
    n_asiento = random.randint(1, 100)
    costo = random.randint(10, 1000)
    return {
        'id_boleto': id_boleto,
        'ruta_id': ruta_id,
        'categoria': categoria,
        'n_asiento': n_asiento,
        'costo': costo
    }

def generate_compras(boleto_id, ruta_id, cliente_id):
    metodo_pago = random.choice(['Efectivo', 'Tarjeta', 'Transferencia'])[:10]
    return {
        'boleto_id': boleto_id,
        'ruta_id': ruta_id,
        'cliente_id': cliente_id,
        'metodo_pago': metodo_pago
    }

def insert_data(cursor, table, data):
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    cursor.execute(query, tuple(data.values()))

def populate_database():
    try:
        connection, cursor = get_connection()

        unique_dnis = set()
        unique_matriculas = set()
        unique_boletos = set()

        # Poblar la tabla Sedes con 10 tuplas
        for _ in range(10):
            sedes = generate_sedes()
            insert_data(cursor, 'Sedes', sedes)
            cursor.execute("SELECT currval('sedes_id_seq');")
            sede_id = cursor.fetchone()[0]

            # Poblar la tabla Conductores con 10,000 tuplas
            for _ in range(10000):
                try:
                    conductores = generate_conductores(unique_dnis, sede_id)
                    insert_data(cursor, 'Conductores', conductores)

                    # Poblar la tabla Vehiculos con 10,000 tuplas
                    vehiculos = generate_vehiculos(unique_matriculas, conductores['DNI'])
                    insert_data(cursor, 'Vehiculos', vehiculos)
                except psycopg2.IntegrityError as e:
                    print(f"IntegrityError: {e}")
                    connection.rollback()

        # Poblar la tabla Estaciones con 10 tuplas
        for _ in range(10):
            estaciones = generate_estaciones()
            insert_data(cursor, 'Estaciones', estaciones)
            estacion_inicio = estaciones['nombre']

            # Poblar la tabla R_EnCurso con 10,000 tuplas
            for _ in range(10000):
                try:
                    r_encurso = generate_r_encurso(estacion_inicio)
                    insert_data(cursor, 'R_EnCurso', r_encurso)
                    cursor.execute("SELECT currval('r_encurso_id_seq');")
                    ruta_id = cursor.fetchone()[0]

                    # Poblar la tabla Boletos con 1,000,000 tuplas
                    for _ in range(1):
                        try:
                            boletos = generate_boletos(unique_boletos, ruta_id)
                            insert_data(cursor, 'Boletos', boletos)

                            # Poblar la tabla Compras con 1,000,000 tuplas
                            clientes = generate_clientes(unique_dnis)
                            insert_data(cursor, 'Clientes', clientes)
                            compras = generate_compras(boletos['id_boleto'], ruta_id, clientes['DNI'])
                            insert_data(cursor, 'Compras', compras)
                        except psycopg2.IntegrityError as e:
                            print(f"IntegrityError: {e}")
                            connection.rollback()
                except psycopg2.IntegrityError as e:
                    print(f"IntegrityError: {e}")
                    connection.rollback()

        # Poblar la tabla R_Finalizadas con 10,000 tuplas
        for _ in range(100000):
            try:
                estacion_inicio = fake.city()[:15]
                estacion_final = fake.city()[:15]
                r_finalizadas = generate_r_finalizadas(estacion_inicio, estacion_final)
                insert_data(cursor, 'R_Finalizadas', r_finalizadas)
            except psycopg2.IntegrityError as e:
                print(f"IntegrityError: {e}")
                connection.rollback()

        print("Datos insertados con éxito.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    populate_database()
