
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Lista donde guardo los articulos comestibles
stock = [
    ["1", "Arroz", "Almacen", "Paquete de arroz", 20, 1800],
    ["2", "Fideos", "Almacen", "Paquete de fideos", 15, 1200],
    ["3", "Azucar", "Almacen", "Paquete de azucar", 10, 1500],
    ["4", "Leche", "Lacteos", "Leche larga vida", 8, 1600],
    ["5", "Yerba", "Infusiones", "Paquete de yerba", 12, 3500],
    ["6", "Aceite", "Almacen", "Botella de aceite", 6, 2800]
]


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

    for producto in stock:
        tabla.add_row(
            producto[0],
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

    tabla.add_row("ID", producto[0])
    tabla.add_row("Nombre", producto[1])
    tabla.add_row("Categoria", producto[2])
    tabla.add_row("Descripcion", producto[3])
    tabla.add_row("Cantidad", str(producto[4]))
    tabla.add_row("Precio", "$ " + str(producto[5]))

    console.print(tabla)


# Funcion para buscar un producto por ID
def buscar_producto(identificador):
    for producto in stock:
        if producto[0] == identificador:
            return producto

    return None


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

            # Genero un ID nuevo
            if len(stock) == 0:
                identificador = "1"
            else:
                mayor = 0

                for producto in stock:
                    if int(producto[0]) > mayor:
                        mayor = int(producto[0])

                identificador = str(mayor + 1)

            nombre = ingreso("Ingrese el nombre")
            categoria = ingreso("Ingrese la categoria")
            descripcion = ingreso("Ingrese la descripcion")
            cantidad = ingresar_cantidad()
            precio = ingresar_precio()

            producto = [
                identificador,
                nombre,
                categoria,
                descripcion,
                cantidad,
                precio
            ]

            stock.append(producto)

            console.print(
                "Producto agregado correctamente",
                style="bold green"
            )

            tarjeta(producto)

        # Mostrar productos
        case "2":
            if len(stock) == 0:
                console.print(
                    "No hay productos registrados",
                    style="red"
                )
            else:
                mostrar_stock()

        # Buscar producto por ID
        case "3":
            console.print("BUSCAR PRODUCTO", style="bold green")

            identificador = ingreso("Ingrese el ID")
            producto = buscar_producto(identificador)

            if producto is not None:
                console.print("Producto encontrado", style="green")
                tarjeta(producto)
            else:
                console.print("Producto no encontrado", style="red")

        # Actualizar producto
        case "4":
            console.print("ACTUALIZAR PRODUCTO", style="bold green")

            identificador = ingreso("Ingrese el ID")
            producto = buscar_producto(identificador)

            if producto is not None:
                tarjeta(producto)

                console.print(
                    Panel(
                        "1. Nombre\n"
                        "2. Categoria\n"
                        "3. Descripcion\n"
                        "4. Cantidad\n"
                        "5. Precio\n"
                        "6. Volver al menu",
                        title="Que dato desea modificar?"
                    )
                )

                modificar = input("Elija una opcion: ")

                match modificar:
                    case "1":
                        producto[1] = ingreso("Nuevo nombre")
                        console.print("Nombre actualizado", style="green")

                    case "2":
                        producto[2] = ingreso("Nueva categoria")
                        console.print("Categoria actualizada", style="green")

                    case "3":
                        producto[3] = ingreso("Nueva descripcion")
                        console.print("Descripcion actualizada", style="green")

                    case "4":
                        producto[4] = ingresar_cantidad()
                        console.print("Cantidad actualizada", style="green")

                    case "5":
                        producto[5] = ingresar_precio()
                        console.print("Precio actualizado", style="green")

                    case "6":
                        console.print("Volviendo al menu", style="yellow")

                    case _:
                        console.print("Opcion incorrecta", style="red")

            else:
                console.print(
                    "No existe un producto con ese ID",
                    style="red"
                )

        # Eliminar producto
        case "5":
            console.print("ELIMINAR PRODUCTO", style="bold green")

            identificador = ingreso("Ingrese el ID")
            producto = buscar_producto(identificador)

            if producto is not None:
                tarjeta(producto)

                confirmar = input("Desea eliminarlo? (s/n): ")

                if confirmar.lower() == "s":
                    stock.remove(producto)
                    console.print("Producto eliminado", style="green")
                else:
                    console.print("No se elimino el producto", style="yellow")

            else:
                console.print("Producto no encontrado", style="red")

        # Reporte de stock
        case "6":
            console.print("REPORTE DE STOCK", style="bold green")

            limite = ingresar_cantidad()
            encontrado = False

            tabla = Table(title="Productos con poco stock")
            tabla.add_column("ID", style="cyan")
            tabla.add_column("Nombre", style="green")
            tabla.add_column("Cantidad", justify="right")
            tabla.add_column("Precio", justify="right")

            for producto in stock:
                if producto[4] <= limite:
                    tabla.add_row(
                        producto[0],
                        producto[1],
                        str(producto[4]),
                        "$ " + str(producto[5])
                    )
                    encontrado = True

            if encontrado:
                console.print(tabla)
            else:
                console.print(
                    "No hay productos con esa cantidad de stock o menos",
                    style="yellow"
                )

        # Salir
        case "7":
            console.print(
                "Programa terminado. Gracias por utilizarlo.",
                style="bold yellow"
            )

        case _:
            console.print("Opcion incorrecta", style="bold red")

