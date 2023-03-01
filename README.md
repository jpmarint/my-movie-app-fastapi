# Movie App API

API Restful para un manager de películas construida con FastAPI.

## Instalación
### Requisitos previos
- Python 3.11.1
- Virtual environment
  
### Clonar el repositorio
Para clonar el repositorio, ejecuta el siguiente comando en la terminal:

```
git clone https://github.com/jpmarint/my-movie-app-fastapi.git
```

### Crear un entorno virtual
Antes de instalar los paquetes necesarios para correr la aplicación, se recomienda crear un entorno virtual. Para crearlo, ejecuta los siguientes comandos:

**Windows**
```
py -3 -m venv venv
venv\Scripts\activate.bat
```

**Linux**
```
python3 -m venv venv
source venv/bin/activate
```

### Instalar las dependencias
Para instalar las dependencias, ejecuta el siguiente comando:

```
pip install -r requirements.txt
```
### Configurar las variables de entorno
Crea un archivo .env y dentro incluye esta línea para usarlo como llave para la encriptación de los JWT:
```
SECRET_KEY=mi_clave_secreta
```
---
## Ejecutar la aplicación
Para ejecutar la aplicación, asegúrate de estar en el directorio raíz del proyecto y ejecuta el siguiente comando:

```
uvicorn main:app --reload
```

## Uso
Abre tu navegador web y visita la URL http://localhost:8000/docs para interactuar con la API a través de la interfaz Swagger UI. 

Igual aquí te dejo la lista de endpoints

### Autenticación
- **POST /login:** Permite a los usuarios iniciar sesión y obtener un token de autenticación JWT.
### Películas
- **GET /movies:** Devuelve todas las películas registradas en la aplicación.
- **POST /movies:** Permite crear una nueva película.
- **GET /movies/{id}:** Muestra una película específica.
- **PUT /movies/{id}:** Permite actualizar los datos de una película existente.
- **DELETE /movies/{id}:** Permite eliminar una película existente.
- **GET /movies/:** Permite buscar películas por categoría.
### Inicio
- **GET /:** Muestra un mensaje de bienvenida y/o instrucciones de uso.

## Contribuir
Si quieres contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama 
   ```
   'git checkout -b feature/nombre-de-la-funcionalidad'.
   ```
3. Realiza los cambios necesarios y haz commit de los mismos 
   ```
   git commit -m "Descripción de los cambios"
   ```
4. Haz push a la rama 
   ```
   git push origin feature/nombre-de-la-funcionalidad
   ```
5. Abre un **pull request**.