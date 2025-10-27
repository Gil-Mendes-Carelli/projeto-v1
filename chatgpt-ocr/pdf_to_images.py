from pathlib import Path
from pdf2image import convert_from_path
from typing import List

def pdf_to_images(pdf_path: Path, output_dir: Path, poppler_path: str, dpi: int = 300) -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = convert_from_path(str(pdf_path), dpi=dpi, poppler_path=poppler_path)
    image_paths: List[Path] = []

    for i, page in enumerate(pages, start=1):
        img_path = output_dir / f"{pdf_path.stem}_page_{i}.png"
        page.save(img_path, "PNG")
        print(f"Página {i} salva em: {img_path}")
        image_paths.append(img_path)

    return image_paths
