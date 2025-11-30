# Gym Membership Management System

Una aplicación de línea de comandos completa para gestionar membresías de gimnasio con cálculo de costos, descuentos de grupo y características premium.

## Características

### 1. Selección de Membresía
- **Planes disponibles:**
  - **Basic**: $29.99 - Acceso a equipos de gimnasio y vestuarios básicos
  - **Premium**: $59.99 - Acceso premium a vestuarios y sauna
  - **Family**: $99.99 - Hasta 4 miembros de familia + todos los beneficios Premium + sala familiar

### 2. Características Adicionales
Cada plan de membresía permite agregar características adicionales con costos individuales:
- **Personal Training**: $50.00
- **Group Classes**: $30.00
- **Nutritional Consulting**: $40.00

### 3. Cálculo de Costos
El costo total se calcula así:
```
Costo Total = (Costo Base + Costo Características) - Descuentos + Recargo Premium
```

**Orden de aplicación:**
1. Calcular costo base + características
2. Aplicar descuento de grupo (si aplica)
3. Aplicar descuento de oferta especial (si aplica)
4. Aplicar recargo premium (15% si aplica)

### 4. Descuentos de Grupo
- Se aplica un **descuento del 10%** al costo total si se registran **2 o más miembros** juntos
- Se muestra un mensaje de ahorro potencial al usuario

### 5. Descuentos de Oferta Especial
Basados en el costo total después de descuentos de grupo:
- Si el costo > $200: Descuento de $20
- Si el costo > $400: Descuento de $50
- Solo se aplica el descuento más alto que aplique

### 6. Características de Membresía Premium
Se pueden agregar niveles premium que agregan un **recargo del 15%** al costo total:
- **Exclusive Facilities**: Acceso a instalaciones exclusivas
- **Specialized Training**: Programas de entrenamiento especializados

### 7. Validación de Disponibilidad
- Todos los planes y características se validan antes de procesarse
- Los mensajes de error descriptivos indican el problema específico

### 8. Confirmación del Usuario
Antes de finalizar:
- Se muestra resumen completo de la selección
- Desglose detallado de costos
- Todos los descuentos y recargos aplicados
- El usuario puede confirmar o volver a seleccionar

### 9. Salida
- **Membresía confirmada**: Retorna el costo total como entero positivo
- **Membresía cancelada o datos inválidos**: Retorna -1

## Supuestos

1. **Moneda**: Todos los costos están en USD
2. **Orden de descuentos**: Los descuentos de grupo se aplican primero, luego los descuentos especiales, finalmente el recargo premium
3. **Costo final**: Se retorna como entero positivo (redondeado hacia abajo)
4. **Límite de miembros**: Máximo 10 miembros por grupo
5. **Características duplicadas**: Si se envían características duplicadas, se cuentan múltiples veces
6. **Validación**: Se valida toda entrada antes de procesar

## Estructura del Código

### Clases Principales

#### `MembershipType` (Enum)
Define los tipos de membresía disponibles.

#### `PremiumFeatureLevel` (Enum)
Define los niveles de características premium:
- NONE
- EXCLUSIVE_FACILITIES
- SPECIALIZED_TRAINING

#### `MembershipPlan` (Dataclass)
Representa un plan de membresía con:
- `name`: Nombre del plan
- `base_cost`: Costo base
- `benefits`: Lista de beneficios
- `available`: Disponibilidad

#### `AdditionalFeature` (Dataclass)
Representa una característica adicional:
- `name`: Nombre
- `cost`: Costo
- `available`: Disponibilidad

#### `MembershipSelection` (Dataclass)
Almacena la selección del usuario:
- `plan`: Plan seleccionado
- `additional_features`: Características seleccionadas
- `premium_feature_level`: Nivel premium
- `num_members`: Número de miembros

#### `GymMembershipManager`
Clase principal que gestiona:
- Validación de selecciones
- Cálculos de costo
- Aplicación de descuentos
- Generación de resúmenes

#### `GymMembershipApp`
Interfaz de línea de comandos que:
- Presenta menús
- Obtiene selecciones del usuario
- Muestra resúmenes
- Solicita confirmación

## Uso

### Ejecutar la Aplicación Interactiva

```bash
python gym_membership.py
```

La aplicación guiará al usuario a través de:
1. Selección de plan de membresía
2. Entrada del número de miembros
3. Selección de características adicionales
4. Selección de nivel premium (opcional)
5. Revisión y confirmación

### Ejecutar las Pruebas

```bash
python -m pytest test_gym_membership.py -v
```

O usando unittest:

```bash
python test_gym_membership.py
```

## Ejemplos de Cálculo

### Ejemplo 1: Plan Básico, Sin Características, 1 Miembro
```
Costo Base:              $29.99
Características:         $0.00
Subtotal:               $29.99
Descuento de Grupo:     $0.00
Descuento Especial:     $0.00
Recargo Premium:        $0.00
---
COSTO TOTAL:            $29.99 → 29
```

### Ejemplo 2: Plan Premium, Entrenamiento Personal, 2 Miembros
```
Costo Base:              $59.99
Personal Training:       $50.00
Subtotal:               $109.99
Descuento de Grupo (10%): -$11.00
Después descuento:       $98.99
Descuento Especial:      $0.00
Recargo Premium:         $0.00
---
COSTO TOTAL:             $98.99 → 98
```

### Ejemplo 3: Plan Family, Todas Características, 3 Miembros, Premium
```
Costo Base:              $99.99
Personal Training:       $50.00
Group Classes:           $30.00
Nutritional:             $40.00
Subtotal:               $219.99
Descuento de Grupo (10%): -$22.00
Después descuento:      $197.99
Descuento Especial:      $0.00 (< $200)
Recargo Premium (15%):   $29.70
---
COSTO TOTAL:            $227.69 → 227
```

### Ejemplo 4: Plan Family, Características Múltiples, 2 Miembros
```
Costo Base:              $99.99
Personal Training:       $50.00
Group Classes:           $30.00
Nutritional:             $40.00
Subtotal:               $219.99
Descuento de Grupo (10%): -$22.00
Después descuento:      $197.99
Descuento Especial:      $0.00 (197.99 no > 200)
Recargo Premium:         $0.00
---
COSTO TOTAL:            $197.99 → 197
```

## Suite de Pruebas

La suite de pruebas incluye 100+ casos de prueba organizados en las siguientes categorías:

### TestMembershipValidation
Pruebas de validación de planes de membresía:
- Planes válidos e inválidos
- Disponibilidad de planes
- Manejo de nombres incorrectos

### TestFeaturesValidation
Pruebas de validación de características:
- Características válidas e inválidas
- Listas vacías
- Características duplicadas
- Disponibilidad de características

### TestNumMembersValidation
Pruebas de validación de miembros:
- Rangos válidos (1-10)
- Valores inválidos (0, negativos, > 10)
- Tipos de datos incorrectos

### TestCostCalculations
Pruebas de cálculos base:
- Costos de planes individuales
- Costos de características individuales
- Costos combinados

### TestGroupDiscount
Pruebas de descuento de grupo:
- Sin descuento para 1 miembro
- Descuento del 10% para 2+ miembros
- Precisión de cálculos

### TestSpecialOfferDiscount
Pruebas de descuentos especiales:
- Sin descuento para costos ≤ $200
- $20 de descuento para costos > $200
- $50 de descuento para costos > $400
- Casos límite

### TestPremiumSurcharge
Pruebas de recargo premium:
- Sin recargo para nivel NONE
- Recargo del 15% para otros niveles
- Precisión con valores decimales

### TestTotalCostCalculation
Pruebas de cálculo total:
- Escenarios simples
- Escenarios con múltiples descuentos
- Escenarios complejos con todo
- Conversión a entero

### TestSummaryGeneration
Pruebas de generación de resumen:
- Incluye nombre de plan
- Incluye características
- Incluye información de costos
- Incluye descuentos y recargos

### TestEdgeCases
Pruebas de casos límite:
- Características duplicadas
- Costos muy altos
- Costos cero
- Validez de todos los planes/características

### TestCalculationOrder
Pruebas de orden de aplicación:
- Descuento de grupo antes que especial
- Recargo premium aplicado al final
- Verificación de porcentajes correctos

## Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas
python test_gym_membership.py

# Con pytest
pytest test_gym_membership.py -v

# Solo pruebas específicas
python -m pytest test_gym_membership.py::TestGroupDiscount -v

# Con cobertura
coverage run -m pytest test_gym_membership.py
coverage report
```

## Manejo de Errores

La aplicación maneja gracefully:
- Entrada inválida del usuario
- Planes/características no disponibles
- Errores de cálculo
- Cancelaciones del usuario

Todos los errores se muestran con mensajes descriptivos.

## Extensibilidad

El código está diseñado para ser fácilmente extensible:
- Agregar nuevos planes de membresía a `MEMBERSHIP_PLANS`
- Agregar nuevas características a `ADDITIONAL_FEATURES`
- Agregar nuevos niveles premium a `PremiumFeatureLevel`
- Modificar descuentos en las constantes

Ejemplo:
```python
manager = GymMembershipManager()
manager.membership_plans["Gold"] = MembershipPlan(
    name="Gold",
    base_cost=149.99,
    benefits=["Premium benefits", "Extra perks"],
    available=True
)
```

## Notas Técnicas

- El código utiliza type hints para mayor claridad
- Todas las funciones están documentadas
- Las dataclasses simplifican la gestión de datos
- Las enums garantizan valores válidos
- Los diccionarios facilitan búsquedas rápidas

## Requisitos

- Python 3.7+
- Sin dependencias externas (solo stdlib)

## Autor

Sistema de Gestión de Membresías de Gimnasio - Versión 1.0

## Licencia

Este proyecto está disponible bajo licencia MIT.
