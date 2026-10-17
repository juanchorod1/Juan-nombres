#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import unicodedata

# ============================================================
#  BANCOS DE NOMBRES SIMPLES POR ORIGEN
#  (sin tildes, sin ñ, sin espacios)
# ============================================================

NOMBRES = {
    "latinos": [
        "santiago", "mateo", "sebastian", "leonardo", "matias", "emiliano",
        "diego", "daniel", "alejandro", "lucas", "nicolas", "samuel",
        "andres", "thiago", "martin", "benjamin", "felipe", "joaquin",
        "valentina", "camila", "isabella", "sofia", "valeria", "mariana",
        "lucia", "gabriela", "daniela", "renata", "antonella", "ximena"
    ],
    "espanoles": [
        "antonio", "manuel", "jose", "francisco", "david", "juan",
        "javier", "daniel", "carlos", "miguel", "rafael", "pablo",
        "alejandro", "sergio", "fernando", "jorge", "luis", "alberto",
        "maria", "carmen", "ana", "isabel", "laura", "marta",
        "lucia", "elena", "sara", "paula", "rosa", "pilar"
    ],
    "ingleses": [
        "james", "john", "robert", "michael", "william", "david",
        "richard", "joseph", "thomas", "charles", "christopher", "daniel",
        "matthew", "anthony", "mark", "donald", "steven", "paul",
        "mary", "patricia", "jennifer", "linda", "elizabeth", "barbara",
        "susan", "jessica", "sarah", "karen", "nancy", "lisa"
    ],
    "franceses": [
        "jean", "pierre", "michel", "andre", "philippe", "louis",
        "nicolas", "henri", "paul", "jacques", "antoine", "julien",
        "marie", "jeanne", "francoise", "monique", "catherine", "nathalie",
        "isabelle", "sophie", "camille", "chloe", "lea", "manon"
    ],
    "alemanes": [
        "hans", "peter", "klaus", "wolfgang", "jurgen", "dieter",
        "manfred", "uwe", "thomas", "andreas", "stefan", "michael",
        "anna", "ursula", "monika", "petra", "sabine", "claudia",
        "susanne", "katrin", "julia", "lena", "lea", "sophie"
    ],
    "italianos": [
        "giuseppe", "giovanni", "antonio", "mario", "luigi", "francesco",
        "angelo", "vincenzo", "pietro", "salvatore", "carlo", "franco",
        "maria", "anna", "giuseppina", "rosa", "angela", "giovanna",
        "teresa", "lucia", "carmela", "caterina", "francesca", "alessia"
    ],
    "portugueses": [
        "joao", "jose", "antonio", "francisco", "carlos", "paulo",
        "pedro", "lucas", "luiz", "marcos", "gabriel", "rafael",
        "maria", "ana", "francisca", "antonia", "adriana", "juliana",
        "marcia", "fernanda", "patricia", "aline", "camila", "beatriz"
    ],
    "brasilenos": [
        "joao", "pedro", "lucas", "gabriel", "matheus", "rafael",
        "bruno", "felipe", "thiago", "diego", "vinicius", "caio",
        "maria", "ana", "julia", "beatriz", "larissa", "camila",
        "fernanda", "leticia", "gabriela", "isabela", "manuela", "sofia"
    ],
}


def limpiar(texto):
    """Convierte a minúsculas y elimina tildes/ñ/símbolos."""
    # Normaliza y quita diacríticos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    # Solo deja letras y números
    texto = "".join(c for c in texto if c.isalnum())
    return texto.lower()


def elegir_origen():
    """Menú para elegir el origen de los nombres."""
    origenes = list(NOMBRES.keys())
    print("\n🌍 Orígenes disponibles:")
    for i, o in enumerate(origenes, 1):
        print(f"  {i}. {o.capitalize()}")
    print(f"  {len(origenes) + 1}. Mezclar todos los orígenes")

    while True:
        try:
            op = int(input("\nElige un origen: "))
            if 1 <= op <= len(origenes):
                return origenes[op - 1]
            elif op == len(origenes) + 1:
                return "mezcla"
            else:
                print("❌ Opción fuera de rango.")
        except ValueError:
            print("❌ Ingresa un número válido.")


def main():
    print("=" * 50)
    print("   GENERADOR DE NOMBRES ALEATORIOS")
    print("=" * 50)

    # 1️⃣ Pedir nombre del archivo
    while True:
        nombre_archivo = input("\n1️⃣  Nombre para guardar el .txt (sin extensión): ").strip()
        if not nombre_archivo:
            print("❌ El nombre no puede estar vacío.")
            continue
        nombre_archivo = "".join(c for c in nombre_archivo if c.isalnum() or c in "_-")
        if not nombre_archivo:
            print("❌ Solo se permiten letras, números, _ y -")
            continue
        archivo = f"{nombre_archivo}.txt"
        break

    # 2️⃣ Pedir cantidad de nombres
    while True:
        try:
            cantidad = int(input("2️⃣  ¿Cuántos nombres quieres generar?: "))
            if cantidad <= 0:
                print("❌ Debe ser mayor que 0.")
                continue
            break
        except ValueError:
            print("❌ Ingresa un número válido.")

    # 3️⃣ Elegir origen
    origen = elegir_origen()

    # 4️⃣ Recolectar la lista base de nombres limpios
    if origen == "mezcla":
        pool = []
        for lista in NOMBRES.values():
            pool.extend(lista)
    else:
        pool = list(NOMBRES[origen])

    pool = [limpiar(n) for n in pool if limpiar(n)]

    # 5️⃣ Generar nombres únicos
    print(f"\n⏳ Generando {cantidad} nombres...\n")

    if cantidad > len(pool):
        # Si piden más que el pool, permitimos variantes con números
        nombres_generados = set(pool)
        while len(nombres_generados) < cantidad:
            base = random.choice(pool)
            sufijo = random.randint(1, 9999)
            nombres_generados.add(f"{base}{sufijo}")
    else:
        nombres_generados = set(random.sample(pool, cantidad))

    nombres_lista = sorted(nombres_generados)

    # 6️⃣ Mostrar todos los nombres
    print("=" * 50)
    print(f"   📋 NOMBRES GENERADOS ({len(nombres_lista)})")
    print("=" * 50)
    for i, n in enumerate(nombres_lista, 1):
        print(f"{i:4d}. {n}")

    # 7️⃣ Guardar archivo (un nombre por línea, sin nada extra)
    ruta = os.path.abspath(archivo)
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(nombres_lista))
    except IOError as e:
        print(f"\n❌ Error al guardar: {e}")
        return

    # 8️⃣ Mostrar dónde se guardó
    print("\n" + "=" * 50)
    print("✅ ARCHIVO GUARDADO CORRECTAMENTE")
    print("=" * 50)
    print(f"📁 Ubicación: {ruta}")
    print(f"📄 Archivo:   {archivo}")
    print(f"🔢 Total:     {len(nombres_lista)} nombres")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa cancelado.")