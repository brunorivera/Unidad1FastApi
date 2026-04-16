# app/modules/clientes/routers.py
from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional
from . import schemas, services

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# POST /clientes → Crear cliente
@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def alta_cliente(cliente: schemas.ClienteCreate):
    return services.crear(cliente)


# GET /clientes → Listar con filtros avanzados
@router.get("/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK)
def listar_clientes(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, le=50, description="Máximo de resultados"),
    solo_activos: bool = Query(False, description="Solo clientes activos"),
    nombre: Optional[str] = Query(None, description="Buscar por nombre (parcial)"),
):
    return services.obtener_todos(skip, limit, solo_activos, nombre)


# GET /clientes/{id} → Detalle
@router.get("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def detalle_cliente(id: int = Path(..., gt=0)):
    cliente = services.obtener_por_id(id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cliente no encontrado")
    return cliente


# PUT /clientes/{id} → Reemplazo total
@router.put("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def actualizar_cliente(cliente: schemas.ClienteCreate, id: int = Path(..., gt=0)):
    actualizado = services.actualizar_total(id, cliente)
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cliente no encontrado")
    return actualizado


# PATCH /clientes/{id} → Actualización parcial
@router.patch("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def actualizar_parcial_cliente(cliente: schemas.ClienteUpdate, id: int = Path(..., gt=0)):
    actualizado = services.actualizar_parcial(id, cliente)
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cliente no encontrado")
    return actualizado


# PUT /clientes/{id}/desactivar → Borrado lógico
@router.put("/{id}/desactivar", response_model=schemas.ClienteRead,
            status_code=status.HTTP_200_OK)
def desactivar_cliente(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cliente no encontrado")
    return desactivado