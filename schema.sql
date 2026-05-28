-- ============================================
-- schema.sql - Base de datos Académica
-- Motor: SQLite
-- ============================================

-- 1. Materias
CREATE TABLE IF NOT EXISTS materias (
    id          INTEGER PRIMARY KEY,
    nombre      TEXT    NOT NULL,
    codigo      TEXT    NOT NULL UNIQUE,
    horas_sem   INTEGER NOT NULL,
    area        TEXT    NOT NULL
);

-- 2. Docentes
CREATE TABLE IF NOT EXISTS docentes (
    id              INTEGER PRIMARY KEY,
    nombre          TEXT    NOT NULL,
    especialidad    TEXT    NOT NULL,
    anios_exp       INTEGER NOT NULL,
    formacion       TEXT    NOT NULL
);

-- 3. Cursos (materia × nivel × jornada)
CREATE TABLE IF NOT EXISTS curso_materia (
    id              INTEGER PRIMARY KEY,
    id_materia      INTEGER NOT NULL REFERENCES materias(id),
    id_docente      INTEGER NOT NULL REFERENCES docentes(id),
    nivel           TEXT    NOT NULL CHECK (nivel IN ('Primero','Segundo','Tercero')),
    jornada         TEXT    NOT NULL CHECK (jornada IN ('Matutina','Vespertina')),
    cupo_max        INTEGER NOT NULL,
    aula            TEXT    NOT NULL
);

-- 4. Estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante       INTEGER PRIMARY KEY,
    nombre              TEXT    NOT NULL,
    apellido            TEXT    NOT NULL,
    genero              TEXT    NOT NULL CHECK (genero IN ('M','F')),
    edad                INTEGER NOT NULL,
    ciudad              TEXT    NOT NULL,
    jornada             TEXT    NOT NULL CHECK (jornada IN ('Matutina','Vespertina')),
    nivel               TEXT    NOT NULL CHECK (nivel IN ('Primero','Segundo','Tercero')),
    matematica          REAL    NOT NULL,
    lenguaje            REAL    NOT NULL,
    ciencias            REAL    NOT NULL,
    historia            REAL    NOT NULL,
    ingles              REAL    NOT NULL,
    educacion_fisica    REAL    NOT NULL,
    promedio_general    REAL    NOT NULL,
    asistencia_pct      REAL    NOT NULL,
    clases_asistidas    INTEGER NOT NULL,
    clases_faltadas     INTEGER NOT NULL,
    aprobado            TEXT    NOT NULL CHECK (aprobado IN ('Sí','No'))
);

-- 5. Inscripciones
CREATE TABLE IF NOT EXISTS inscripciones (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante       INTEGER NOT NULL REFERENCES estudiantes(id_estudiante),
    id_curso_materia    INTEGER NOT NULL REFERENCES curso_materia(id),
    nota_obtenida       REAL    NOT NULL,
    estado              TEXT    NOT NULL CHECK (estado IN ('Aprobado','Reprobado'))
);

-- ============================================
-- Índices
-- ============================================
CREATE INDEX IF NOT EXISTS idx_est_nivel    ON estudiantes (nivel);
CREATE INDEX IF NOT EXISTS idx_est_ciudad   ON estudiantes (ciudad);
CREATE INDEX IF NOT EXISTS idx_est_aprobado ON estudiantes (aprobado);
CREATE INDEX IF NOT EXISTS idx_insc_est     ON inscripciones (id_estudiante);
CREATE INDEX IF NOT EXISTS idx_insc_curso   ON inscripciones (id_curso_materia);
