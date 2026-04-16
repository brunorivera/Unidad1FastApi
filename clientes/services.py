# app/modules/clientes/services.py
from typing import List, Optional
from .schemas import ClienteCreate, ClienteUpdate, ClienteRead

# Simulación de base de datos en memoria
db_clientes: List[ClienteRead] = [
    ClienteRead(id=1, nombre="Ana García", email="ana@ejemplo.com",
                telefono="+5491112345678", activo=True),
    ClienteRead(id=2, nombre="Carlos López", email="carlos@ejemplo.com",
                telefono="+5491187654321", activo=True),
]
id_counter = 3


def crear(data: ClienteCreate) -> ClienteRead:
    global id_counter
    nuevo = ClienteRead(id=id_counter, **data.model_dump())
    db_clientes.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(
    skip: int = 0,
    limit: int = 10,
    solo_activos: bool = False,   # Filtro avanzado
    nombre: Optional[str] = None  # Filtro avanzado
) -> List[ClienteRead]:
    resultado = db_clientes

    # Regla de negocio: filtrar por activo
    if solo_activos:
        resultado = [c for c in resultado if c.activo]

    # Regla de negocio: filtrar por nombre (búsqueda parcial, sin importar mayúsculas)
    if nombre:
        resultado = [c for c in resultado if nombre.lower() in c.nombre.lower()]

    return resultado[skip: skip + limit]


def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.id == id:
            return c
    return None


def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            actualizado = ClienteRead(id=id, **data.model_dump())
            db_clientes[index] = actualizado
            return actualizado
    return None


def actualizar_parcial(id: int, data: ClienteUpdate) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            # Tomamos los datos actuales y pisamos solo los que vienen en el body
            c_dict = c.model_dump()
            campos_nuevos = data.model_dump(exclude_unset=True)  # Solo los enviados
            c_dict.update(campos_nuevos)
            actualizado = ClienteRead(**c_dict)
            db_clientes[index] = actualizado
            return actualizado
    return None


def desactivar(id: int) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            c_dict = c.model_dump()
            c_dict["activo"] = False
            actualizado = ClienteRead(**c_dict)
            db_clientes[index] = actualizado
            return actualizado
    return None