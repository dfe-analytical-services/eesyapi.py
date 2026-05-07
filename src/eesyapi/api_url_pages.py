def api_url_pages(page_size: int = 40, page: int = None) -> str:
    """
    Build pagination query string 
    """

    parts = []

    if page is not None:
        parts.append(f"page={page}")

    if page_size is not None:
        parts.append(f"pageSize={page_size}")

    return "&".join(parts)