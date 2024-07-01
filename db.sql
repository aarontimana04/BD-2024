CREATE TABLE Sedes (
	ID SERIAL PRIMARY KEY,
	nombre VARCHAR(20),
	correo VARCHAR(20)
);

CREATE TABLE Clientes (
	DNI INT PRIMARY KEY,
	nombre VARCHAR(10),
	apellido VARCHAR(15)
);

CREATE TABLE Conductores (
	DNI INT PRIMARY KEY,
	correo VARCHAR(20),
	nombre VARCHAR(10),
	apellido VARCHAR(25),
	sede_id INT,
	FOREIGN KEY (sede_id) REFERENCES Sedes(ID)
);

CREATE TABLE Vehiculos (
	Matricula INT PRIMARY KEY,
	marca VARCHAR(10),
	modelo VARCHAR(15),
	anio_func INT,
	conductor_dni INT,
	FOREIGN KEY (conductor_dni) REFERENCES Conductores(DNI)
);

CREATE TABLE Estaciones (
	nombre VARCHAR(15) PRIMARY KEY,
	ubicacion VARCHAR(10)
);

CREATE TABLE R_Finalizadas (
	ID SERIAL PRIMARY KEY,
	estacion_inicio VARCHAR(15),
	estacion_final VARCHAR(15),
	vehiculo_mat INT,
	hora_s TIME,
	hora_l TIME,
	n_embarque_s INT,
	n_embarque_l INT,
	fecha DATE,
	duracion TIME,
	ingresos_gen INT,
	distancia INT,
	FOREIGN KEY (estacion_inicio) REFERENCES Estaciones(nombre),
	FOREIGN KEY (estacion_final) REFERENCES Estaciones(nombre)
);

CREATE TABLE R_EnCurso (
	ID SERIAL PRIMARY KEY,
	fecha DATE,
	estacion_inicio VARCHAR(15),
	n_embarque_s INT,
	hora_s TIME,
	reporte VARCHAR(100),
	FOREIGN KEY (estacion_inicio) REFERENCES Estaciones(nombre)
);

CREATE TABLE Boletos (
	id_boleto INT,
	ruta_id INT,
	categoria VARCHAR(10),
	n_asiento INT,
	costo INT,
	FOREIGN KEY (ruta_id) REFERENCES R_EnCurso(ID),
	PRIMARY KEY(id_boleto, ruta_id)
);
-- mod
CREATE TABLE Compras(
	boleto_id INT,
	ruta_id INT,
	cliente_id INT,
	metodo_pago VARCHAR(10),
	FOREIGN KEY (boleto_id, ruta_id) REFERENCES Boletos(id_boleto, ruta_id),
	FOREIGN KEY (cliente_id) REFERENCES Clientes(DNI),
	PRIMARY KEY (boleto_id, ruta_id, cliente_id)
);

--

DROP TABLE clientes;
DROP TABLE sedes;
DROP TABLE conductores;
DROP TABLE vehiculos;
DROP TABLE estaciones;
DROP TABLE r_finalizadas;
DROP TABLE r_encurso;
DROP TABLE boletos;
DROP TABLE compras;

