# Gestión de Artículos Comestibles

Sistema de gestión de productos desarrollado en Python y SQLite.

## Descripción

Aplicación de consola que permite administrar artículos comestibles de un comercio. Los datos se almacenan en una base de datos SQLite, permitiendo conservar la información aunque se cierre el programa.

## Tecnologías utilizadas

- Python
- SQLite
- Rich

## Funcionalidades

- Agregar productos.
- Mostrar todos los productos.
- Buscar productos por ID.
- Actualizar información de productos.
- Eliminar productos con confirmación.
- Generar reportes de stock.

## Estructura de los productos

Cada producto contiene:

- ID
- Nombre
- Categoría
- Descripción
- Cantidad
- Precio

## Conceptos aplicados

- Funciones y modularización.
- Condicionales y ciclos.
- Validación de datos.
- Manejo de errores con try-except.
- Consultas SQL parametrizadas.
- Operaciones CRUD.
- Transacciones con commit() y rollback().
- Cierre de conexión con finally.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/25950032/Final-articulos-sqlite.git
```

### 2. Instalar Rich

```bash
pip install rich
```

### 3. Ejecutar el programa

```bash
python Final-sqlite26.py
```

La base de datos `articulos.db` se crea automáticamente si no existe.

## Autora

Proyecto personal de práctica de Python y bases de datos SQLite.
