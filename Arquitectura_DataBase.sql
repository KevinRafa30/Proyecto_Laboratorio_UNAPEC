
CREATE DATABASE Laboratorio_UNAPEC;
GO

USE Laboratorio_UNAPEC;
GO

CREATE TABLE Campus (
    IdCampus INT PRIMARY KEY IDENTITY(1,1),
    Descripcion VARCHAR(100) NOT NULL,
    Estado CHAR(1) DEFAULT 'A' -- A: Activo, I: Inactivo
);

CREATE TABLE Edificios (
    IdEdificio INT PRIMARY KEY IDENTITY(1,1),
    Descripcion VARCHAR(100) NOT NULL,
    IdCampus INT NOT NULL,
    Estado CHAR(1) DEFAULT 'A',
    CONSTRAINT FK_Edificio_Campus FOREIGN KEY (IdCampus) REFERENCES Campus(IdCampus)
);

CREATE TABLE Tipos_Aulas (
    IdTipoAula INT PRIMARY KEY IDENTITY(1,1),
    Descripcion VARCHAR(100) NOT NULL,
    Estado CHAR(1) DEFAULT 'A'
);

CREATE TABLE Aulas (
    IdAula INT PRIMARY KEY IDENTITY(1,1),
    Descripcion VARCHAR(100) NOT NULL,
    Capacidad INT NOT NULL,
    CuposReservados INT DEFAULT 0,
    IdEdificio INT NOT NULL,
    IdTipoAula INT NOT NULL,
    Estado CHAR(1) DEFAULT 'A',
    CONSTRAINT FK_Aula_Edificio FOREIGN KEY (IdEdificio) REFERENCES Edificios(IdEdificio),
    CONSTRAINT FK_Aula_Tipo FOREIGN KEY (IdTipoAula) REFERENCES Tipos_Aulas(IdTipoAula)
);

CREATE TABLE Usuarios (
    IdUsuario INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(150) NOT NULL,
    Cedula VARCHAR(11) UNIQUE NOT NULL,
    NoCarnet VARCHAR(20) UNIQUE NOT NULL,
    TipoUsuario VARCHAR(20), 
    Estado CHAR(1) DEFAULT 'A'
);

CREATE TABLE Empleados (
    IdEmpleado INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(150) NOT NULL,
    Cedula VARCHAR(11) UNIQUE NOT NULL,
    TandaLabor VARCHAR(20), 
    FechaIngreso DATE NOT NULL,
    Estado CHAR(1) DEFAULT 'A'
);

CREATE TABLE Reservaciones (
    NoReservacion INT PRIMARY KEY IDENTITY(1,1),
    IdEmpleado INT NOT NULL,
    IdAula INT NOT NULL,
    IdUsuario INT NOT NULL,
    FechaReservacion DATE NOT NULL,
    CantidadHoras INT NOT NULL,
    Comentario TEXT,
    Estado CHAR(1) DEFAULT 'A',
    CONSTRAINT FK_Reserva_Empleado FOREIGN KEY (IdEmpleado) REFERENCES Empleados(IdEmpleado),
    CONSTRAINT FK_Reserva_Aula FOREIGN KEY (IdAula) REFERENCES Aulas(IdAula),
    CONSTRAINT FK_Reserva_Usuario FOREIGN KEY (IdUsuario) REFERENCES Usuarios(IdUsuario)
);
GO