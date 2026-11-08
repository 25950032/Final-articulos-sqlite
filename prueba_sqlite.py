
import sqlite3

conexion = sqlite3.connect("articulos.db")

try:
    cursor = conexion.cursor()

    # Modificar el precio
    cursor.execute("""
        UPDATE productos
        SET precio = ?
        WHERE id = ?
    """, (2000, 1))

    conexion.commit()

    print("Precio actualizado.")

    # Eliminar con confirmacion
    confirmar = input("¿Desea eliminar el producto Arroz? (s/n): ")

    if confirmar.lower() == "s":

        cursor.execute("""
            DELETE FROM productos
            WHERE id = ?
        """, (1,))

        conexion.commit()

        print("Producto eliminado correctamente.")

    else:
        print("Eliminacion cancelada.")

    # Consultar productos
    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    for producto in productos:
        print(producto)

except sqlite3.Error as error:
    conexion.rollback()
    print("Error:", error)

finally:
    conexion.close()
