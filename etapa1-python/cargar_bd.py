import json
import pg8000
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host":     os.getenv("DB_HOST"),
    "port":     int(os.getenv("DB_PORT")),
}


def to_float(value):
    if value is None or value == "N/A":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def cargar_vulnerabilidades(cur):
    with open("etapa1-python/output/vulnerabilidades.json", encoding="utf-8") as f:
        vulnerabilidades = json.load(f)

    insertados = 0
    omitidos = 0

    for v in vulnerabilidades:
        v31 = v.get("cvss_v31") or {}
        v2  = v.get("cvss_v2")  or {}

        try:
            cur.execute("""
                INSERT INTO vulnerabilities (
                    cve_id, in_cisa, in_nuclei,
                    cisa_vendor, cisa_product, cisa_vulnerability_name,
                    cisa_date_added, cisa_ransomware_use,
                    nuclei_name, nuclei_severity,
                    description,
                    cvss_v31_base_score, cvss_v31_base_severity, cvss_v31_vector_string,
                    cvss_v31_exploitability_score, cvss_v31_impact_score,
                    cvss_v2_base_score, cvss_v2_base_severity, cvss_v2_vector_string,
                    cvss_v2_exploitability_score, cvss_v2_impact_score,
                    cwes, cpes
                ) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                ) ON CONFLICT (cve_id) DO NOTHING
            """, (
                v.get("cve_id"),
                v.get("in_cisa"),
                v.get("in_nuclei"),
                v.get("cisa_vendor"),
                v.get("cisa_product"),
                v.get("cisa_vulnerability_name"),
                v.get("cisa_date_added"),
                v.get("cisa_ransomware_use"),
                v.get("nuclei_name"),
                v.get("nuclei_severity"),
                v.get("description"),
                to_float(v31.get("base_score")),
                v31.get("base_severity"),
                v31.get("vector_string"),
                to_float(v31.get("exploitability_score")),
                to_float(v31.get("impact_score")),
                to_float(v2.get("base_score")),
                v2.get("base_severity"),
                v2.get("vector_string"),
                to_float(v2.get("exploitability_score")),
                to_float(v2.get("impact_score")),
                ",".join(v.get("cwes") or []),
                ",".join(v.get("cpes") or []),
            ))
            insertados += 1
        except Exception as e:
            print(f"Error en {v.get('cve_id')}: {e}")
            insertados -= 1
            omitidos += 1

    print(f"vulnerabilities → Insertados: {insertados} | Omitidos: {omitidos}")


def cargar_cwe_stats(cur):
    with open("etapa1-python/output/cve_vs_cwe.json", encoding="utf-8") as f:
        cwe_data = json.load(f)

    insertados = 0
    for cwe_id, count in cwe_data.items():
        try:
            cur.execute("""
                INSERT INTO cwe_stats (cwe_id, cve_count)
                VALUES (%s, %s)
                ON CONFLICT (cwe_id) DO UPDATE SET cve_count = EXCLUDED.cve_count
            """, (cwe_id, count))
            insertados += 1
        except Exception as e:
            print(f"Error en {cwe_id}: {e}")

    print(f"cwe_stats → Insertados: {insertados}")


def cargar_cpe_ranking(cur):
    with open("etapa1-python/output/ranking_cpe.json", encoding="utf-8") as f:
        cpe_data = json.load(f)

    cur.execute("TRUNCATE TABLE cpe_ranking")

    insertados = 0
    for vendor_product, count in cpe_data.items():
        try:
            cur.execute("""
                INSERT INTO cpe_ranking (vendor_product, cve_count)
                VALUES (%s, %s)
            """, (vendor_product, count))
            insertados += 1
        except Exception as e:
            print(f"Error en {vendor_product}: {e}")

    print(f"cpe_ranking → Insertados: {insertados}")


def cargar():
    conn = pg8000.connect(**DB_CONFIG)
    cur = conn.cursor()

    cargar_vulnerabilidades(cur)
    conn.commit()

    cargar_cwe_stats(cur)
    conn.commit()

    cargar_cpe_ranking(cur)
    conn.commit()

    cur.close()
    conn.close()
    print("Carga completada.")


if __name__ == "__main__":
    cargar()
