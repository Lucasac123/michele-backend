import os
from sqlalchemy.orm import Session
from database import models

def scan_and_ingest(directory_path: str, db: Session):
    added_count = 0
    
    # Ensure directory exists
    if not os.path.exists(directory_path):
        return 0

    for root, dirs, files in os.walk(directory_path):
        # Use folder name as a tag (e.g., "Mickey Mouse" folder -> Tag "Mickey Mouse")
        folder_name = os.path.basename(root)
        
        # Get or create tag for folder
        tag = db.query(models.Tag).filter(models.Tag.name == folder_name).first()
        if not tag and folder_name:
            tag = models.Tag(name=folder_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.cdr')):
                full_path = os.path.join(root, file)
                
                # Check if asset exists
                existing = db.query(models.Asset).filter(models.Asset.file_path == full_path).first()
                if not existing:
                    # Guess type based on keywords or folder?
                    # For now default to OTHER, or simple heuristic
                    asset_type = models.AssetType.OTHER
                    lower_name = file.lower()
                    if "frame" in lower_name or "moldura" in lower_name:
                        asset_type = models.AssetType.FRAME
                    elif "background" in lower_name or "fundo" in lower_name:
                        asset_type = models.AssetType.BACKGROUND
                    
                    asset = models.Asset(
                        name=file,
                        file_path=full_path,
                        asset_type=asset_type
                    )
                    
                    if tag:
                        asset.tags.append(tag)
                    
                    db.add(asset)
                    added_count += 1
    
    db.commit()
    return added_count
