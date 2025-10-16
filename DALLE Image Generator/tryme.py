import os
import uuid
import base64
from pathlib import Path
from typing import List, Optional

from config import get_client


def generate_images(
    prompt: str,
    size: str = "1024x1024",
    n: int = 1,
    transparent: bool = False,
    output_dir: str = "static/images",
) -> List[str]:
    """
    Generate images with gpt-image-1, save them under static/images,
    and return Flask-served URLs like /static/images/<file>.png
    """
    client = get_client()

    # Build the call; DO NOT use response_format for gpt-image-1
    kwargs = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": size,
        "n": n,
    }
    # Optional transparent background for PNGs
    if transparent:
        kwargs["background"] = "transparent"

    result = client.images.generate(**kwargs)

    # Ensure output directory exists
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    urls: List[str] = []
    for item in result.data:
        # gpt-image-1 returns base64, not a URL
        b64 = getattr(item, "b64_json", None)
        if not b64:
            # Safety fallback if SDK ever returns a URL again
            url = getattr(item, "url", None)
            if url:
                urls.append(url)
                continue
            raise ValueError("Image generation returned no b64_json or url")

        img_bytes = base64.b64decode(b64)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = out_path / filename
        with open(filepath, "wb") as f:
            f.write(img_bytes)

        # Flask will serve this under /static/...
        urls.append(f"/static/images/{filename}")

    return urls
