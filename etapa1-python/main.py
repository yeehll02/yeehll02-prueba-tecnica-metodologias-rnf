import json
import time
import logging
import os
from collections import Counter
from statistics import mean, stdev

from fuentes import obtener_cisa_kev, convertir_entrada_cisa, obtener_nuclei_cves, convertir_entrada_nuclei
from nist import obtener_nist_cve, DELAY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = "etapa1-python/output"


def combinar_fuentes(cisa_data, nuclei_data) -> list[dict]:
    """Une CVEs de ambas fuentes en una sola lista."""
    todos = {}

    for cve_id, entry in cisa_data.items():
        todos[cve_id] = {"cve_id": cve_id, **convertir_entrada_cisa(entry), "in_nuclei": False}

    for cve_id, entry in nuclei_data.items():
        nuclei_fields = convertir_entrada_nuclei(entry)
        if cve_id in todos:
            todos[cve_id].update(nuclei_fields)
        else:
            todos[cve_id] = {"cve_id": cve_id, "in_cisa": False, **nuclei_fields}

    return list(todos.values())


def enriquecer_con_nist(vulnerabilidades: list[dict]) -> list[dict]:
    """Por cada CVE consulta NIST y agrega los datos."""
    total = len(vulnerabilidades)
    resultado = []

    for i, vuln in enumerate(vulnerabilidades, 1):
        cve_id = vuln["cve_id"]
        logger.info(f"[{i}/{total}] Consultando NIST: {cve_id}")

        nist = obtener_nist_cve(cve_id)

        if nist:
            vuln["description"]  = nist.get("description")
            vuln["cvss_v31"]     = {
                "base_score":          nist.get("cvss_v31_base_score"),
                "base_severity":       nist.get("cvss_v31_severity"),
                "vector_string":       nist.get("cvss_v31_vector"),
                "exploitability_score": nist.get("cvss_v31_exploit"),
                "impact_score":        nist.get("cvss_v31_impact"),
            }
            vuln["cvss_v2"]      = {
                "base_score":          nist.get("cvss_v2_base_score"),
                "base_severity":       nist.get("cvss_v2_severity"),
                "vector_string":       nist.get("cvss_v2_vector"),
                "exploitability_score": nist.get("cvss_v2_exploit"),
                "impact_score":        nist.get("cvss_v2_impact"),
            }
            vuln["cwes"]         = nist.get("cwes", [])
            vuln["cpes"]         = nist.get("cpes", [])
        else:
            vuln["description"]  = None
            vuln["cvss_v31"]     = None
            vuln["cvss_v2"]      = None
            vuln["cwes"]         = []
            vuln["cpes"]         = []

        resultado.append(vuln)
        time.sleep(DELAY)

    return resultado


def calcular_cve_vs_cwe(vulnerabilidades: list[dict]) -> dict:
    """Cuenta cuántos CVEs únicos tiene cada CWE."""
    contador = Counter()
    for vuln in vulnerabilidades:
        for cwe in set(vuln.get("cwes", [])):  # set evita contar duplicados por CVE
            contador[cwe] += 1
    return dict(contador.most_common())


def calcular_ranking_cpe(vulnerabilidades: list[dict]) -> dict:
    """Ranking de vendor+producto más afectados según CPE (CVEs únicos por plataforma)."""
    contador = Counter()
    for vuln in vulnerabilidades:
        vistos = set()
        for cpe in vuln.get("cpes", []):
            partes = cpe.split(":")
            # cpe:2.3:tipo:vendor:producto:version:...
            if len(partes) >= 5:
                vendor_producto = f"{partes[3]}:{partes[4]}"
                if vendor_producto not in vistos:
                    vistos.add(vendor_producto)
                    contador[vendor_producto] += 1
    return dict(contador.most_common(50))  # top 50


def calcular_tendencias(vulnerabilidades: list[dict]) -> dict:
    """
    Bonus: identifica meses con pico de adiciones en CISA,
    lo que puede indicar un cambio de tendencia en explotabilidad.
    """
    conteo_por_mes: Counter = Counter()
    for vuln in vulnerabilidades:
        fecha = vuln.get("cisa_date_added")
        if fecha:
            mes = fecha[:7]  # "YYYY-MM"
            conteo_por_mes[mes] += 1

    if len(conteo_por_mes) < 2:
        return {"meses": dict(conteo_por_mes), "picos": []}

    valores = list(conteo_por_mes.values())
    promedio = mean(valores)
    desviacion = stdev(valores) if len(valores) > 1 else 0
    umbral = promedio + desviacion

    picos = sorted(
        [mes for mes, cnt in conteo_por_mes.items() if cnt >= umbral],
    )

    return {
        "conteo_mensual": dict(sorted(conteo_por_mes.items())),
        "promedio_mensual": round(promedio, 2),
        "umbral_pico": round(umbral, 2),
        "meses_pico": picos,
    }


def guardar_json(nombre: str, datos):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ruta = f"{OUTPUT_DIR}/{nombre}"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False, default=str)
    logger.info(f"Guardado: {ruta}")


if __name__ == "__main__":
    # 1. Descargar fuentes
    cisa_data   = obtener_cisa_kev()
    nuclei_data = obtener_nuclei_cves()

    # 2. Combinar
    vulnerabilidades = combinar_fuentes(cisa_data, nuclei_data)
    logger.info(f"Total CVEs únicos: {len(vulnerabilidades)}")

    # 3. Enriquecer con NIST
    vulnerabilidades = enriquecer_con_nist(vulnerabilidades)

    # 4. Calcular métricas
    cve_vs_cwe   = calcular_cve_vs_cwe(vulnerabilidades)
    ranking_cpe  = calcular_ranking_cpe(vulnerabilidades)
    tendencias   = calcular_tendencias(vulnerabilidades)

    # 5. Guardar resultados
    guardar_json("vulnerabilidades.json", vulnerabilidades)
    guardar_json("cve_vs_cwe.json",       cve_vs_cwe)
    guardar_json("ranking_cpe.json",      ranking_cpe)
    guardar_json("tendencias.json",       tendencias)

    logger.info("Proceso completado.")