import requests
import time
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

NIST_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
API_KEY  = os.getenv("NVD_API_KEY")




DELAY = 0.6 if API_KEY else 6.0


def obtener_nist_cve(cve_id: str) -> dict | None:
    """Consulta la API del NIST para un CVE y retorna los datos parseados."""
    headers = {"apiKey": API_KEY} if API_KEY else {}

    try:
        response = requests.get(NIST_URL, params={"cveId": cve_id}, headers=headers, timeout=30)
        response.raise_for_status()
        vulnerabilities = response.json().get("vulnerabilities", [])
        if not vulnerabilities:
            return None
        return convertir_entrada_nist(vulnerabilities[0]["cve"])
    except Exception as e:
        logger.warning(f"Error consultando NIST para {cve_id}: {e}")
        return None


def convertir_entrada_nist(cve: dict) -> dict:
    """Extrae los campos pedidos"""
    # Descripción en inglés
    descripcion = next(
        (d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"),
        None
    )

    # CVSS v3.1
    v31 = cve.get("metrics", {}).get("cvssMetricV31", [])
    v31 = v31[0] if v31 else {}

    # CVSS v2
    v2 = cve.get("metrics", {}).get("cvssMetricV2", [])
    v2 = v2[0] if v2 else {}

    # CWEs — value de weaknesses
    cwes = [
        d["value"]
        for w in cve.get("weaknesses", [])
        for d in w.get("description", [])
        if d["lang"] == "en"
    ]

    cpes = list(dict.fromkeys(
        match["criteria"]
        for config in cve.get("configurations", [])
        for node in config.get("nodes", [])
        for match in node.get("cpeMatch", [])
        if match.get("vulnerable")
    ))

    return {
        "description":          descripcion,
        # CVSS v3.1
        "cvss_v31_vector":      v31.get("cvssData", {}).get("vectorString"),
        "cvss_v31_base_score":  v31.get("cvssData", {}).get("baseScore"),
        "cvss_v31_severity":    v31.get("cvssData", {}).get("baseSeverity"),
        "cvss_v31_exploit":     v31.get("exploitabilityScore"),
        "cvss_v31_impact":      v31.get("impactScore"),
        # CVSS v2
        "cvss_v2_vector":       v2.get("cvssData", {}).get("vectorString"),
        "cvss_v2_base_score":   v2.get("cvssData", {}).get("baseScore"),
        "cvss_v2_severity":     v2.get("baseSeverity"),
        "cvss_v2_exploit":      v2.get("exploitabilityScore"),
        "cvss_v2_impact":       v2.get("impactScore"),
        # CWE y CPE
        "cwes":                 cwes,
        "cpes":                 cpes,
    }