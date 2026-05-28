"""
NIVEL 1 — Ejercicios completos
Esquema: Estudiantes / Cursos
"""

import sqlite3
import sys

DB_PATH = "academia.db"


def conectar():
    conexion_bd = sqlite3.connect(DB_PATH)
    conexion_bd.row_factory = sqlite3.Row
    return conexion_bd


# =========================
# SELECT
# =========================

def select_01():
    """Mostrar todos los datos de todos los estudiantes."""
    conexion_bd = conectar()
    cursor_estudiantes = conexion_bd.cursor()

    cursor_estudiantes.execute("SELECT * FROM estudiantes")

    for estudiante in cursor_estudiantes.fetchall():
        print(dict(estudiante))

    conexion_bd.close()


def select_02():
    """Mostrar nombre, apellido y email de estudiantes nacidos después del 2001."""
    conexion_bd = conectar()
    cursor_estudiantes = conexion_bd.cursor()

    cursor_estudiantes.execute(
        "SELECT nombre, apellido, email "
        "FROM estudiantes "
        "WHERE fecha_nacimiento > '2001-12-31'"
    )

    for estudiante in cursor_estudiantes.fetchall():
        print(dict(estudiante))

    conexion_bd.close()


def select_03():
    """Mostrar nombre y créditos de los cursos ordenados por créditos descendente."""
    conexion_bd = conectar()
    cursor_cursos = conexion_bd.cursor()

    cursor_cursos.execute(
        "SELECT nombre, creditos "
        "FROM cursos "
        "ORDER BY creditos DESC"
    )

    for curso in cursor_cursos.fetchall():
        print(dict(curso))

    conexion_bd.close()


def select_04():
    """Mostrar nombre del estudiante, nombre del curso y nota (JOIN)."""
    conexion_bd = conectar()
    cursor_inscripciones = conexion_bd.cursor()

    cursor_inscripciones.execute(
        "SELECT e.nombre AS estudiante, "
        "c.nombre AS curso, "
        "i.nota "
        "FROM estudiantes AS e "
        "INNER JOIN inscripciones AS i "
        "ON e.id = i.estudiante_id "
        "INNER JOIN cursos AS c "
        "ON c.id = i.curso_id"
    )

    for inscripcion in cursor_inscripciones.fetchall():
        print(dict(inscripcion))

    conexion_bd.close()


def select_05():
    """Mostrar cuántos estudiantes hay."""
    conexion_bd = conectar()
    cursor_total = conexion_bd.cursor()

    cursor_total.execute(
        "SELECT COUNT(*) AS total FROM estudiantes"
    )

    print(dict(cursor_total.fetchone()))

    conexion_bd.close()


# =========================
# INSERT
# =========================

def insert_01():
    """Insertar estudiante."""
    conexion_bd = conectar()
    cursor_estudiantes = conexion_bd.cursor()

    cursor_estudiantes.execute(
        """
        INSERT INTO estudiantes(nombre, apellido, email, fecha_nacimiento)
        VALUES('María', 'Torres', 'maria.torres@email.com', '2004-08-12');
        """
    )

    conexion_bd.commit()
    print("[OK] Estudiante insertado.")
    conexion_bd.close()


def insert_02():
    """Insertar curso."""
    conexion_bd = conectar()
    cursor_cursos = conexion_bd.cursor()

    cursor_cursos.execute(
        "INSERT INTO cursos(nombre, creditos) "
        "VALUES('Historia del Arte', 3);"
    )

    conexion_bd.commit()
    print("[OK] Curso insertado.")
    conexion_bd.close()


def insert_03():
    """Insertar inscripción."""
    conexion_bd = conectar()
    cursor_inscripciones = conexion_bd.cursor()

    cursor_inscripciones.execute(
        "INSERT INTO inscripciones(estudiante_id, curso_id) "
        "VALUES(1,3);"
    )

    conexion_bd.commit()
    print("[OK] Inscripción insertada.")
    conexion_bd.close()


def insert_04():
    """Insertar dos estudiantes."""
    conexion_bd = conectar()
    cursor_estudiantes = conexion_bd.cursor()

    cursor_estudiantes.execute(
        """
        INSERT INTO estudiantes(nombre, apellido, email, fecha_nacimiento)
        VALUES
        ('Daniela', 'Flores', 'daniela@email.com', '2003-05-11'),
        ('Andrés', 'Pérez', 'andres@email.com', '2002-09-21');
        """
    )

    conexion_bd.commit()
    print("[OK] Estudiantes insertados.")
    conexion_bd.close()


# =========================
# UPDATE
# =========================

def update_01():
    """Actualizar email."""
    conexion_bd = conectar()
    cursor_estudiantes = conexion_bd.cursor()

    cursor_estudiantes.execute(
        "UPDATE estudiantes "
        "SET email = 'diego.h@email.com' "
        "WHERE id = 2"
    )

    conexion_bd.commit()
    print("[OK] Email actualizado.")
    conexion_bd.close()


def update_02():
    """Actualizar créditos."""
    conexion_bd = conectar()
    cursor_cursos = conexion_bd.cursor()

    cursor_cursos.execute(
        "UPDATE cursos "
        "SET creditos = 5 "
        "WHERE id = 4"
    )

    conexion_bd.commit()
    print("[OK] Créditos actualizados.")
    conexion_bd.close()


def update_03():
    """Actualizar nota."""
    conexion_bd = conectar()
    cursor_inscripciones = conexion_bd.cursor()

    cursor_inscripciones.execute(
        "UPDATE inscripciones "
        "SET nota = 14.5 "
        "WHERE estudiante_id = 5 AND curso_id = 2"
    )

    conexion_bd.commit()
    print("[OK] Nota actualizada.")
    conexion_bd.close()


# =========================
# DELETE
# =========================

def delete_01():
    """Eliminar inscripción."""
    conexion_bd = conectar()
    cursor_inscripciones = conexion_bd.cursor()

    cursor_inscripciones.execute(
        "DELETE FROM inscripciones WHERE id = 5"
    )

    conexion_bd.commit()
    print("[OK] Inscripción eliminada.")
    conexion_bd.close()


def delete_02():
    """Eliminar inscripciones sin nota."""
    conexion_bd = conectar()
    cursor_inscripciones = conexion_bd.cursor()

    cursor_inscripciones.execute(
        "DELETE FROM inscripciones WHERE nota IS NULL"
    )

    conexion_bd.commit()
    print(f"[OK] {cursor_inscripciones.rowcount} inscripción(es) eliminada(s).")
    conexion_bd.close()


def delete_03():
    """Eliminar cursos sin estudiantes inscritos."""
    conexion_bd = conectar()
    cursor_cursos = conexion_bd.cursor()

    cursor_cursos.execute(
        """
        DELETE FROM cursos
        WHERE id NOT IN (
            SELECT curso_id FROM inscripciones
        )
        """
    )

    conexion_bd.commit()
    print(f"[OK] {cursor_cursos.rowcount} curso(s) eliminado(s).")
    conexion_bd.close()


# =========================
# CREAR BASE DE DATOS
# =========================

def crear_db():
    import os

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conexion_bd = sqlite3.connect(DB_PATH)

    conexion_bd.executescript("""
        CREATE TABLE estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            fecha_inscripcion DATE DEFAULT CURRENT_DATE
        );

        CREATE TABLE cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            creditos INTEGER NOT NULL CHECK(creditos > 0)
        );

        CREATE TABLE inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            fecha_inscripcion DATE DEFAULT CURRENT_DATE,
            nota REAL CHECK(nota >= 0 AND nota <= 20),
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        );

        INSERT INTO estudiantes VALUES
            (1, 'Valeria', 'Castro', 'valeria.castro@email.com', '2001-05-12', '2024-04-01'),
            (2, 'Diego', 'Herrera', 'diego.herrera@email.com', '2002-08-19', '2024-04-01'),
            (3, 'Camila', 'Navarro', 'camila.navarro@email.com', '2003-02-25', '2024-04-01'),
            (4, 'Javier', 'Ortega', 'javier.ortega@email.com', '2000-10-30', '2024-04-01'),
            (5, 'Fernanda', 'Ríos', 'fernanda.rios@email.com', '2002-06-14', '2024-04-01');

        INSERT INTO cursos VALUES
            (1, 'Desarrollo Web', 'HTML, CSS y JavaScript', 5),
            (2, 'Redes de Computadoras', 'Conceptos básicos de redes', 4),
            (3, 'Administración de Bases de Datos', 'Gestión de bases de datos relacionales', 4),
            (4, 'Diseño Digital', 'Herramientas y fundamentos de diseño', 3);

        INSERT INTO inscripciones (id, estudiante_id, curso_id, fecha_inscripcion, nota) VALUES
            (1, 1, 1, '2024-04-05', 17.5),
            (2, 1, 2, '2024-04-05', 15.0),
            (3, 2, 1, '2024-04-06', 13.5),
            (4, 2, 3, '2024-04-06', 18.0),
            (5, 3, 2, '2024-04-07', 19.5),
            (6, 3, 3, '2024-04-07', 16.0),
            (7, 4, 1, '2024-04-08', 11.5),
            (8, 4, 4, '2024-04-08', 17.0),
            (9, 5, 2, '2024-04-09', NULL),
            (10, 5, 3, '2024-04-09', NULL);
    """)

    conexion_bd.commit()
    conexion_bd.close()

    print(f"[OK] Base de datos '{DB_PATH}' creada.\n")


if __name__ == "__main__":
    if "--soluciones" in sys.argv:
        crear_db()
        print("Soluciones creadas.")
    else:
        crear_db()
        print("Ejercicios creados.")