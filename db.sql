CREATE TABLE Sedes (
	ID SERIAL PRIMARY KEY,
	nombre VARCHAR(20) NOT NULL,
	correo VARCHAR(20) NOT NULL
);

CREATE TABLE Clientes (
	DNI INT PRIMARY KEY NOT NULL,
	nombre VARCHAR(10) NOT NULL,
	apellido VARCHAR(15) NOT NULL
);

CREATE TABLE Conductores (
	DNI INT PRIMARY KEY NOT NULL,
	correo VARCHAR(20) NOT NULL,
	nombre VARCHAR(10) NOT NULL,
	apellido VARCHAR(25) NOT NULL,
	sede_id INT NOT NULL,
	FOREIGN KEY (sede_id) REFERENCES Sedes(ID)
);

CREATE TABLE Vehiculos (
	Matricula VARCHAR(10) PRIMARY KEY NOT NULL,
	marca VARCHAR(10) NOT NULL,
	modelo VARCHAR(15) NOT NULL,
	anio_func INT NOT NULL,
	conductor_dni INT NOT NULL,
	FOREIGN KEY (conductor_dni) REFERENCES Conductores(DNI)
);

CREATE TABLE Estaciones (
	nombre VARCHAR(15) PRIMARY KEY NOT NULL,
	ubicacion VARCHAR(10) NOT NULL
);

CREATE TABLE R_Finalizadas (
	ID SERIAL PRIMARY KEY,
	estacion_inicio VARCHAR(15) NOT NULL,
	estacion_final VARCHAR(15) NOT NULL,
	vehiculo_mat VARCHAR(10) NOT NULL,
	hora_s TIME NOT NULL,
	hora_l TIME NOT NULL,
	n_embarque_s INT NOT NULL,
	n_embarque_l INT NOT NULL,
	fecha DATE NOT NULL,
	duracion TIME NOT NULL,
	ingresos_gen INT NOT NULL,
	distancia INT NOT NULL,
	FOREIGN KEY (estacion_inicio) REFERENCES Estaciones(nombre),
	FOREIGN KEY (estacion_final) REFERENCES Estaciones(nombre)
);

CREATE TABLE R_EnCurso (
	ID SERIAL PRIMARY KEY,
	fecha DATE NOT NULL,
	estacion_inicio VARCHAR(15) NOT NULL,
	n_embarque_s INT NOT NULL,
	hora_s TIME NOT NULL,
	reporte VARCHAR(100) NOT NULL,
	FOREIGN KEY (estacion_inicio) REFERENCES Estaciones(nombre)
);

CREATE TABLE Boletos (
	id_boleto INT NOT NULL,
	ruta_id INT NOT NULL,
	categoria VARCHAR(10) NOT NULL,
	n_asiento INT NOT NULL,
	costo INT NOT NULL,
	FOREIGN KEY (ruta_id) REFERENCES R_EnCurso(ID),
	PRIMARY KEY(id_boleto, ruta_id)
);

CREATE TABLE Compras(
	boleto_id INT NOT NULL,
	ruta_id INT NOT NULL,
	cliente_id INT NOT NULL,
	metodo_pago VARCHAR(10) NOT NULL,
	FOREIGN KEY (boleto_id, ruta_id) REFERENCES Boletos(id_boleto, ruta_id),
	FOREIGN KEY (cliente_id) REFERENCES Clientes(DNI),
	PRIMARY KEY (boleto_id, ruta_id, cliente_id)
);

-----

CREATE OR REPLACE FUNCTION calcular_duracion () RETURNS TRIGGER AS $$
BEGIN
    NEW.duracion := NEW.hora_l - NEW.hora_s;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_calcular_duracion
BEFORE INSERT OR UPDATE ON R_Finalizadas
FOR EACH ROW
EXECUTE FUNCTION calcular_duracion();

-----

DROP TABLE clientes;
DROP TABLE sedes;
DROP TABLE conductores;
DROP TABLE vehiculos;
DROP TABLE estaciones;
DROP TABLE r_finalizadas;
DROP TABLE r_encurso;
DROP TABLE boletos;
DROP TABLE compras;
