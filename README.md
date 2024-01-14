# SIGEF - Sistema Informático para las Elecciones de la FEU

SIGEF (Sistema Informático para las Elecciones de la Federación de Estudiantes Universitarios) es una plataforma desarrollada para gestionar procesos electorales dentro de instituciones educativas. El sistema permite la postulación de candidatos, la participación de la comunidad estudiantil en votaciones, la creación de elecciones tanto a nivel de institución como de facultad, y la visualización de resultados electorales.

## Características Principales

- **Postulación de Candidatos:** Los estudiantes pueden postularse como candidatos para participar en las elecciones.
- **Votación Estudiantil:** Facilita el proceso de votación, permitiendo que las masas estudiantiles emitan sus votos de manera electrónica.
- **Creación de Elecciones:** Los administradores pueden configurar y crear elecciones, ya sea a nivel de institución o de facultad.
- **Visualización de Resultados:** Proporciona herramientas para visualizar de manera clara y accesible los resultados de las elecciones.

## Instalación

### Requisitos Previos

Asegúrate de tener los siguientes requisitos instalados en tu sistema antes de proceder con la instalación:

- [Python](https://www.python.org/): Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- [Pipenv](https://pipenv.pypa.io/): Instala Pipenv, que se utilizará para gestionar el entorno virtual de Python. Puedes instalarlo con el siguiente comando:

  ```bash
  pip install pipenv
  ```

- [Docker](https://www.docker.com/): SIGEF utiliza Docker para gestionar los contenedores. Asegúrate de tener Docker instalado en tu sistema. Puedes seguir las instrucciones de instalación en [docker.com](https://www.docker.com/get-started).

### Configuración del Entorno

Antes de ejecutar SIGEF, necesitarás configurar tu entorno. Copia el archivo `.env.example` y renómbralo a `.env`. Asegúrate de completar los valores necesarios en este archivo.

```env
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
SECRET_KEY=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=
```

### Comandos de Instalación

El proyecto proporciona un conjunto de comandos útiles para la instalación y gestión. Puedes ejecutar estos comandos a través del Makefile:

#### Instalación Inicial

```bash
make setup
```

Este comando creará la red local, construirá los contenedores, ejecutará las migraciones de la base de datos y creará un superusuario.

#### Ejecutar la Aplicación

```bash
make start
```

### Comandos útiles:

#### Realizar Migraciones

```bash
make migrate
```

Ejecuta las migraciones de la base de datos.

#### Crear un Superusuario

```bash
make superuser
```

Crea un superusuario para acceder a la interfaz administrativa.

#### Limpiar Volúmenes (Eliminar Datos de la Base de Datos)

```bash
make clear-volumes
```

Este comando elimina todos los datos almacenados en la base de datos.

#### Acceder a la Consola de la Base de Datos

```bash
make dbshell
```

Este comando abre la consola de la base de datos.

#### Otros Comandos de Gestión

Puedes utilizar otros comandos proporcionados por el Makefile para realizar tareas específicas. Consulta el Makefile para obtener la lista completa.

### Ejecutar Pruebas

El proyecto incluye pruebas que puedes ejecutar con el siguiente comando:

```bash
make test
```

Este comando ejecutará las pruebas del proyecto.

### Ejecutar Pruebas Rápidas (Sin Migraciones)

```bash
make test-fast
```

Este comando ejecutará pruebas sin aplicar migraciones.
