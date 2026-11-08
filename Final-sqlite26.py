import sqlite3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
conexion = None

try:
    conexion = sqlite3.connect("articulos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            descripcion TEXT,
            cantidad INTEGER,
            precio REAL
        )
    """)

    conexion.commit()

except sqlite3.Error as error:

    if conexion is not None:
        conexion.rollback()

    console.print(
        f"Error al conectar con la base de datos: {error}",
        style="bold red"
    )

    raise SystemExit(1)


# Funcion para pedir datos y evitar que queden vacios
def ingreso(campo):
    dato = input(campo + ": ").strip()

    while dato == "":
        console.print("El campo no puede estar vacio", style="bold red")
        dato = input(campo + ": ").strip()

    return dato


# Funcion para ingresar una cantidad valida
def ingresar_cantidad():
    cantidad = input("Ingrese la cantidad: ")

    while not cantidad.isdigit():
        console.print("Debe ingresar un numero entero", style="red")
        cantidad = input("Ingrese la cantidad: ")

    return int(cantidad)


# Funcion para ingresar un precio valido
def ingresar_precio():
    precio = input("Ingrese el precio sin centavos: ")

    while not precio.isdigit():
        console.print("El precio debe ser un numero", style="red")
        precio = input("Ingrese el precio sin centavos: ")

    return int(precio)


# Funcion para mostrar los productos en una tabla
def mostrar_stock():
    tabla = Table(title="Stock de articulos comestibles")

    tabla.add_column("ID", style="cyan")
    tabla.add_column("Nombre", style="green")
    tabla.add_column("Categoria", style="yellow")
    tabla.add_column("Descripcion")
    tabla.add_column("Cantidad", justify="right")
    tabla.add_column("Precio", justify="right")

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    for producto in productos:
        tabla.add_row(
            str(producto[0]),
            producto[1],
            producto[2],
            producto[3],
            str(producto[4]),
            "$ " + str(producto[5])
        )

    console.print(tabla)



# Funcion para mostrar un solo producto
def tarjeta(producto):
    tabla = Table(title="Datos del producto")

    tabla.add_column("Campo", style="cyan")
    tabla.add_column("Informacion", style="green")

    tabla.add_row("ID", str(producto[0]))
    tabla.add_row("Nombre", producto[1])
    tabla.add_row("Categoria", producto[2])
    tabla.add_row("Descripcion", producto[3])
    tabla.add_row("Cantidad", str(producto[4]))
    tabla.add_row("Precio", "$ " + str(producto[5]))

    console.print(tabla)



# Funcion para buscar un producto por ID
def buscar_producto(identificador):
    cursor.execute(
        "SELECT * FROM productos WHERE id = ?",
        (identificador,)
    )

    producto = cursor.fetchone()

    return producto

def main():
    opcion = ""

    # El menu se repite hasta elegir salir
    while opcion != "7":

        console.print(
            Panel(
                "[bold yellow]1.[/] Agregar producto\n"
                "[bold yellow]2.[/] Mostrar productos\n"
                "[bold yellow]3.[/] Buscar producto por ID\n"
                "[bold yellow]4.[/] Actualizar producto\n"
                "[bold yellow]5.[/] Eliminar producto\n"
                "[bold yellow]6.[/] Reporte de stock\n"
                "[bold yellow]7.[/] Salir",
                title="[bold green]MENU DE ARTICULOS COMESTIBLES[/]",
                border_style="green"
            )
        )

        opcion = input("Elija una opcion: ")

        match opcion:
            # Agregar producto
            case "1":
                console.print("AGREGAR PRODUCTO", style="bold green")

                nombre = ingreso("Ingrese el nombre")
                categoria = ingreso("Ingrese la categoria")
                descripcion = ingreso("Ingrese la descripcion")
                cantidad = ingresar_cantidad()
                precio = ingresar_precio()

                cursor.execute("""
                    INSERT INTO productos
                    (nombre, categoria, descripcion, cantidad, precio)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, categoria, descripcion, cantidad, precio))

                conexion.commit()

                identificador = cursor.lastrowid

                producto = buscar_producto(identificador)

                tarjeta(producto)

            
                # Mostrar productos
            case "2":
                    cursor.execute("SELECT COUNT(*) FROM productos")
                    cantidad = cursor.fetchone()[0]

                    if cantidad == 0:
                        console.print(
                            "No hay productos registrados.",
                            style="bold red"
                        )
                    else:
                        mostrar_stock()
            
                # Buscar producto
            case "3":
                    console.print("BUSCAR PRODUCTO", style="bold green")

                    identificador = input("Ingrese el ID del producto: ")

                    producto = buscar_producto(identificador)

                    if producto is not None:
                        tarjeta(producto)
                    else:
                        console.print(
                            "Producto no encontrado.",
                            style="bold red"
                        )

            
                # Modificar producto
            case "4":
                    console.print("MODIFICAR PRODUCTO", style="bold green")

                    identificador = input("Ingrese el ID del producto: ")

                    producto = buscar_producto(identificador)

                    if producto is not None:

                        tarjeta(producto)

                        console.print("¿Que desea modificar?")
                        console.print("1. Nombre")
                        console.print("2. Categoria")
                        console.print("3. Descripcion")
                        console.print("4. Cantidad")
                        console.print("5. Precio")
                        console.print("6. Volver")

                        opcion_modificar = input("Elija una opcion: ")

                        match opcion_modificar:

                            case "1":
                                nuevo = ingreso("Ingrese el nuevo nombre")
                                cursor.execute(
                                    "UPDATE productos SET nombre = ? WHERE id = ?",
                                    (nuevo, identificador)
                                )

                            case "2":
                                nuevo = ingreso("Ingrese la nueva categoria")
                                cursor.execute(
                                    "UPDATE productos SET categoria = ? WHERE id = ?",
                                    (nuevo, identificador)
                                )

                            case "3":
                                nuevo = ingreso("Ingrese la nueva descripcion")
                                cursor.execute(
                                    "UPDATE productos SET descripcion = ? WHERE id = ?",
                                    (nuevo, identificador)
                                )

                            case "4":
                                nuevo = ingresar_cantidad()
                                cursor.execute(
                                    "UPDATE productos SET cantidad = ? WHERE id = ?",
                                    (nuevo, identificador)
                                )

                            case "5":
                                nuevo = ingresar_precio()
                                cursor.execute(
                                    "UPDATE productos SET precio = ? WHERE id = ?",
                                    (nuevo, identificador)
                                )

                            case "6":
                                console.print("Volviendo al menu.")

                            case _:
                                console.print("Opcion incorrecta.", style="bold red")

                        if opcion_modificar in ["1", "2", "3", "4", "5"]:
                            conexion.commit()

                            producto = buscar_producto(identificador)

                            console.print(
                                "Producto modificado correctamente.",
                                style="bold green"
                            )

                            tarjeta(producto)

                    else:
                        console.print("Producto no encontrado.", style="bold red")


                # Eliminar producto
            case "5":
                    console.print("ELIMINAR PRODUCTO", style="bold green")

                    identificador = input("Ingrese el ID del producto: ")

                    producto = buscar_producto(identificador)

                    if producto is not None:

                        tarjeta(producto)

                        confirmar = input(
                            "¿Desea eliminar este producto? (s/n): "
                        )

                        if confirmar.lower() == "s":

                            cursor.execute(
                                "DELETE FROM productos WHERE id = ?",
                                (identificador,)
                            )

                            conexion.commit()

                            console.print(
                                "Producto eliminado correctamente.",
                                style="bold green"
                            )

                        else:
                            console.print(
                                "Eliminacion cancelada.",
                                style="bold yellow"
                            )

                    else:
                        console.print(
                            "Producto no encontrado.",
                            style="bold red"
                        )
            
            
                # Reporte de stock
            case "6":
                    console.print("REPORTE DE STOCK", style="bold green")

                    limite = ingresar_cantidad()

                    cursor.execute("""
                        SELECT * FROM productos
                        WHERE cantidad <= ?
                    """, (limite,))

                    productos = cursor.fetchall()

                    if len(productos) == 0:
                        console.print(
                            "No hay productos con esa cantidad de stock.",
                            style="bold yellow"
                        )

                    else:
                        tabla = Table(title="Productos con stock bajo")

                        tabla.add_column("ID", style="cyan")
                        tabla.add_column("Nombre", style="green")
                        tabla.add_column("Categoria", style="yellow")
                        tabla.add_column("Descripcion")
                        tabla.add_column("Cantidad", justify="right")
                        tabla.add_column("Precio", justify="right")

                        for producto in productos:
                            tabla.add_row(
                                str(producto[0]),
                                producto[1],
                                producto[2],
                                producto[3],
                                str(producto[4]),
                                "$ " + str(producto[5])
                            )

                        console.print(tabla)
            

                # Salir
            case "7":
                    console.print(
                        "Programa terminado. Gracias por utilizarlo.",
                        style="bold yellow"
                    )

            case _:
                    console.print("Opcion incorrecta", style="bold red")

try:
    main()

except sqlite3.Error as error:
    conexion.rollback()
    console.print(
        f"Error en la base de datos: {error}",
        style="bold red"
    )

finally:
    conexion.close()
    console.print("Conexion cerrada correctamente.", style="yellow")
