"""
create_db.py
Genera la base de datos SQLite 'academico.db' con datos de
materias, docentes, cursos e inscripciones.
Ejecutar ANTES del notebook principal.
"""

import sqlite3
import random
import os

random.seed(99)
DB_PATH = "academico.db"

# Elimina DB previa si existe
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ── Crear tablas ────────────────────────────────────────────
with open("schema.sql", "r", encoding="utf-8") as f:
    cur.executescript(f.read())

# ── Insertar materias ───────────────────────────────────────
materias = [
    (1, "Matemática",        "MAT-01", 4, "Exactas"),
    (2, "Lengua y Literatura","LEN-01", 4, "Humanidades"),
    (3, "Ciencias Naturales", "CIE-01", 3, "Ciencias"),
    (4, "Historia y CCSS",   "HIS-01", 3, "Humanidades"),
    (5, "Inglés",            "ING-01", 3, "Idiomas"),
    (6, "Educación Física",  "EFI-01", 2, "Deportes"),
]
cur.executemany(
    "INSERT INTO materias VALUES (?,?,?,?,?)", materias
)

# ── Insertar docentes ───────────────────────────────────────
docentes = [
    (1, "Prof. Rosa Andrade",    "Matemática",        12, "Licenciatura"),
    (2, "Prof. Marco Salinas",   "Lengua y Literatura",8, "Magíster"),
    (3, "Prof. Elena Figueroa",  "Biología",          15, "Magíster"),
    (4, "Prof. Tomás Guerrero",  "Historia",           6, "Licenciatura"),
    (5, "Prof. Sandra Brito",    "Inglés",            10, "Certificación CELTA"),
    (6, "Prof. Ramiro Cevallos", "Deportes",           9, "Licenciatura"),
]
cur.executemany(
    "INSERT INTO docentes VALUES (?,?,?,?,?)", docentes
)

# ── Insertar cursos (materia × nivel × jornada) ─────────────
niveles  = ["Primero", "Segundo", "Tercero"]
jornadas = ["Matutina", "Vespertina"]
aulas    = ["A-101","A-102","B-201","B-202","C-301","C-302"]

id_curso = 1
for id_mat in range(1, 7):
    for nivel in niveles:
        for jornada in jornadas:
            aula = random.choice(aulas)
            cur.execute(
                "INSERT INTO curso_materia VALUES (?,?,?,?,?,?,?)",
                (id_curso, id_mat, id_mat, nivel, jornada, 35, aula)
            )
            id_curso += 1

# ── Inscripciones (cada estudiante en todos sus cursos) ──────
# Mapeamos nombre de materia → columna del CSV para cargar notas
import csv

columna_nota = {
    "Matemática":         "matematica",
    "Lengua y Literatura":"lenguaje",
    "Ciencias Naturales": "ciencias",
    "Historia y CCSS":    "historia",
    "Inglés":             "ingles",
    "Educación Física":   "educacion_fisica",
}

with open("estudiantes.csv", "r", encoding="utf-8") as f:
    estudiantes = list(csv.DictReader(f))

# Obtener cursos de la BD
cur.execute("SELECT id, id_materia, nivel, jornada FROM curso_materia")
cursos_db = cur.fetchall()

# Mapa rápido: (id_materia, nivel, jornada) → id_curso
mapa_curso = {(r[1], r[2], r[3]): r[0] for r in cursos_db}

# Mapa materia id → nombre
mat_nombre = {m[0]: m[1] for m in materias}

inscripciones = []
for est in estudiantes:
    nivel   = est["nivel"]
    jornada = est["jornada"]
    id_est  = int(est["id_estudiante"])
    for id_mat, nombre_mat in mat_nombre.items():
        id_curso_ins = mapa_curso.get((id_mat, nivel, jornada))
        if id_curso_ins:
            col = columna_nota[nombre_mat]
            nota = float(est[col])
            estado = "Aprobado" if nota >= 14 else "Reprobado"
            inscripciones.append((id_est, id_curso_ins, nota, estado))

cur.executemany(
    "INSERT INTO inscripciones(id_estudiante, id_curso_materia, nota_obtenida, estado) VALUES (?,?,?,?)",
    inscripciones
)

conn.commit()
conn.close()

print(f"Base de datos '{DB_PATH}' creada exitosamente.")
print(f"  Materias insertadas   : {len(materias)}")
print(f"  Docentes insertados   : {len(docentes)}")
print(f"  Cursos generados      : {id_curso - 1}")
print(f"  Inscripciones totales : {len(inscripciones)}")
