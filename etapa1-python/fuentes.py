import requests
import logging
import json

logger = logging.getLogger(__name__)

CISA_URL   = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
NUCLEI_URL = "https://raw.githubusercontent.com/projectdiscovery/nuclei-templates/main/cves.json"


# ── CISA ──────────────────────────────────────────────────────────

def obtener_cisa_kev() -> dict[str, dict]:
    """Descarga el catálogo CISA KEV. Retorna un dict por cveID."""
    logger.info("Descargando CISA KEV...")
    response = requests.get(CISA_URL, timeout=60)
    response.raise_for_status()

    vulnerabilities = response.json().get("vulnerabilities", [])
    logger.info(f"CISA KEV: {len(vulnerabilities)} vulnerabilidades descargadas.")
    return {v["cveID"]: v for v in vulnerabilities}


def convertir_entrada_cisa(entry: dict) -> dict:
    """Normaliza un registro CISA al formato interno."""
    return {
        "in_cisa":                 True,
        "cisa_date_added":         entry.get("dateAdded"),
        "cisa_due_date":           entry.get("dueDate"),
        "cisa_vendor":             entry.get("vendorProject"),
        "cisa_product":            entry.get("product"),
        "cisa_vulnerability_name": entry.get("vulnerabilityName"),
        "cisa_short_description":  entry.get("shortDescription"),
        "cisa_required_action":    entry.get("requiredAction"),
        "cisa_ransomware_use":     entry.get("knownRansomwareCampaignUse"),
        "cisa_notes":              entry.get("notes"),
        "cisa_cwes":               entry.get("cwes", []), 
    }


# ── NUCLEI ────────────────────────────────────────────────────────

def obtener_nuclei_cves() -> dict[str, dict]:
    """Descarga el listado Nuclei (NDJSON). Retorna un dict por CVE ID."""
    logger.info("Descargando Nuclei CVEs...")
    response = requests.get(NUCLEI_URL, timeout=60)
    response.raise_for_status()

    entries = [json.loads(line) for line in response.text.splitlines() if line.strip()]
    logger.info(f"Nuclei: {len(entries)} entradas descargadas.")

    indexed = {}
    for entry in entries:
        cve_id = _extract_nuclei_cve_id(entry)
        if cve_id:
            indexed[cve_id] = entry

    logger.info(f"Nuclei: {len(indexed)} CVEs únicos")
    return indexed


def convertir_entrada_nuclei(entry: dict) -> dict:
    """Normaliza un registro Nuclei al formato interno."""
    info = entry.get("Info", {})
    classification = info.get("Classification", {})
    return {
        "in_nuclei":        True,
        "nuclei_name":      info.get("Name"),
        "nuclei_severity":  info.get("Severity"),
        "nuclei_description": info.get("Description"),
        "nuclei_cvss_score": classification.get("CVSSScore") or None,
        "nuclei_template":  entry.get("file_path"),
    }


# ──────────────────────────────────────────────────

def _extract_nuclei_cve_id(entry: dict) -> str | None:
    """Extrae el CVE ID de un registro Nuclei."""
    # Campo directo en la raíz
    for key in ("ID", "id"):
        val = entry.get(key, "")
        if val and val.upper().startswith("CVE-"):
            return val.upper()
    return None


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    cisa_data   = obtener_cisa_kev()
    nuclei_data = obtener_nuclei_cves()

    print(f"\nCISA CVEs:   {len(cisa_data)}")
    print(f"Nuclei CVEs: {len(nuclei_data)}")

    print("\n--- Ejemplo CISA ---")
    first_cisa = next(iter(cisa_data))
    print(convertir_entrada_cisa(cisa_data[first_cisa]))

    print("\n--- Ejemplo Nuclei ---")
    first_nuclei = next(iter(nuclei_data))
    print(convertir_entrada_nuclei(nuclei_data[first_nuclei]))