# AntioMarket 

Plataforma digital que conecta productores campesinos de Antioquia con consumidores conscientes, promoviendo el comercio local y el desarrollo sostenible.

## Instalación y Ejecución

### Pasos para ejecutar

1. **Clonar el repositorio**
```bash
git clone <https://github.com/sherrerah3/AntioMarket>
cd AntioMarket/mercado_campesino
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

5. **Ejecutar servidor**
```bash
python manage.py runserver
```

6. **Ejecutar servidor del microservicio en flask**

En una nueva pestaña de la consola:
```bash
cd AntioMarket/flask_servicio
python app.py
```

## Acceso al Sistema

- **URL Principal**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/
- **URL del microservicio en Flask**: http://localhost:5001/api/productos

## Tipos de Usuario

### Cliente
- **Registro**: `/cuentas/registro/cliente/`
- **Funcionalidades**: Explorar productos, agregar al carrito, hacer compras

### Vendedor
- **Registro**: `/cuentas/registro/vendedor/`
- **Funcionalidades**: Gestionar productos, ver estadísticas de ventas

## Tecnologías

- Django 4.2.0
- SQLite (base de datos)
- Bootstrap 5.3
- Font Awesome
- Flask

## Estructura del Proyecto

```
mercado_campesino/
├── cuentas/          # Gestión de usuarios
├── productos/        # Catálogo de productos
├── carrito/          # Carrito de compras
├── reseñas/          # Sistema de reseñas
├── pedidos/          # Gestión de pedidos
└── media/            # Archivos multimedia
```

## Desarrolladores

- Samuel Herrera Hoyos
- Juan José Gómez

**Universidad EAFIT** - Arquitectura de Software