from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

def looks_like_terabox(url: str) -> bool:
    # simple check: contains terabox or netdisk in hostname/path
    try:
        p = urlparse(url)
        host = p.netloc.lower()
        return "terabox" in host or "netdisk" in host or "terabox" in p.path.lower()
    except Exception:
        return False
