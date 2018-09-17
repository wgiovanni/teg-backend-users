# Proceso de instalación

> Este README asume que se tiene instalado `python` (3.6.5) y `pip` (18.0).

## Configuración del `virtualenv`

---

1. Abrir terminal.
1. Instalar `virtualenv` con:

    > `pip install virtualenv`

1. Acceder al directorio del proyecto (raíz sugerido) por medio del terminal.
1. Crear el entorno virtual con:

    > `virtualenv <nombre_entorno>`

    Se sugiere llamarlo `env`, quedando el comando como:

    > `virtualenv env`

##Activar el virtualenv de Python

> `$ .\env\Scripts\activate` \
> `(env)$ `

Luego de esto ya estamos dentro de nuestra virtualenv, en el caso de que ya 
no queramos trabajar en otro virtualenv y deseamos desactivar la actual aplicamos:

> `(env)$ deactivate` \
> `$` 

## Configuración para el entorno de `flask`

---

Instalar las extensiones o librerías necesarias. En este caso:

- `flask`.
- `flask-restful`.
- `flask-cors`.
- `pyodbc`.
- `simplejson`.
- `ldap3`.

Se instalan haciendo uso del `pip` del nuevo entorno, esto se hara mediante un 
archivo o fichero en el que estaran todas las extensiones("requirements.txt"):

> `(env)$ pip install -r ./requirements.txt` 

De esta forma se estaran instalando todas las extensiones, la estructura de fichero
donde estan las extensiones seria básicamente:

requirements.txt

> `flask` \
> `flask-restful` \
> `flask-cors` \
> `pyodbc` \
> `simplejson` \
> `ldap3`

# Proceso de inicio del servidor 

> ## **NOTA**: Actualmente este servidor está configurado para únicamente para desarrollo

1. Definir la variable de entorno para el APP.

    > `set FLASK_APP=app.py`

1. Iniciar el servidor (corre por defecto en el puerto `5000`). Ejemplo: 

    > `(env) C:\Users\wilke\Desktop\flask-vue\backend-users>python app.py`

  	> ## **NOTA**: el puerto se toma por defecto (el que usa el flask, en este caso es el 5000), si se quiere tener otro puerto, se le debe colocar en la clase principal (app.py), por ejemplo:

>
    if __name__ == '__main__': 
        app.run(debug=True, host='0.0.0.0', port=int('numero puerto'))
>
Y de esta forma se estará cambiando el puerto.