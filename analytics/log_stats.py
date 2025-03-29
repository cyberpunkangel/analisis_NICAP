import re
import os
from dotenv import load_dotenv
from pathlib import Path
from collections import Counter
import geoip2.database


def get_log_statistics():
    # Cargar archivo .env
    ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=ENV_PATH)

    LOG_PATH = os.getenv("ACCESS_LOG_PATH")
    GEOIP_DB_PATH = os.getenv("GEOIP_DB_PATH")

    if not LOG_PATH or not os.path.exists(LOG_PATH):
        raise ValueError("ACCESS_LOG_PATH inválido o no definido.")
    if not GEOIP_DB_PATH or not os.path.exists(GEOIP_DB_PATH):
        raise ValueError("GEOIP_DB_PATH inválido o no definido.")

    LOG_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+).+?"[A-Z]+\s[^"]+"\s\d+\s\d+\s"[^"]+"\s"(?P<user_agent>[^"]+)"'
    )

    city_country_counter = Counter()
    browser_counter = Counter()

    with geoip2.database.Reader(GEOIP_DB_PATH) as reader, open(
        LOG_PATH, encoding="utf-8"
    ) as f:
        for line in f:
            match = LOG_PATTERN.search(line)
            if match:
                ip = match.group("ip")
                user_agent = match.group("user_agent")

                # Identificar navegador
                if "Chrome" in user_agent and "Edg" not in user_agent:
                    browser = "Chrome"
                elif "Firefox" in user_agent:
                    browser = "Firefox"
                elif "Safari" in user_agent and "Chrome" not in user_agent:
                    browser = "Safari"
                elif "Edge" in user_agent or "Edg" in user_agent:
                    browser = "Edge"
                elif "MSIE" in user_agent or "Trident" in user_agent:
                    browser = "Internet Explorer"
                else:
                    browser = "Otro"

                browser_counter[browser] += 1

                # Buscar ciudad y país
                try:
                    response = reader.city(ip)
                    city = response.city.name or "Desconocido"
                    country = response.country.name or "Desconocido"
                    label = f"{city}, {country}"
                except:
                    label = "Desconocido"

                city_country_counter[label] += 1

    return {
        "locations": city_country_counter.most_common(10),
        "browsers": browser_counter.most_common(),
    }
