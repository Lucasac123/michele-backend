from sqlalchemy.orm import Session
from database import models
from typing import Dict, Any, List
import random

def select_assets(criteria: Dict[str, Any], db: Session) -> Dict[str, Any]:
    theme = criteria.get("theme", "")
    product_type = criteria.get("product_type", "")
    
    # 1. Search for Background/Theme assets
    # Try to find tags matching the theme
    # This is a naive search: strict string match. 
    # In production, we might use fuzzy matching or embedding search.
    
    theme_assets = []
    if theme:
        # Search for tags containing the theme name
        tags = db.query(models.Tag).filter(models.Tag.name.ilike(f"%{theme}%")).all()
        for tag in tags:
            for asset in tag.assets:
                theme_assets.append(asset)
    
    # If no specific theme assets found, maybe fallback or return empty?
    # For now, let's just pick one if available, or empty
    selected_background = None
    if theme_assets:
        # Filter for background type if possible
        bgs = [a for a in theme_assets if a.asset_type == models.AssetType.BACKGROUND or a.asset_type == models.AssetType.OTHER]
        if bgs:
            selected_background = random.choice(bgs)
        else:
            selected_background = random.choice(theme_assets)

    # 2. Search for Frame/Label assets (Product Type)
    frame_assets = db.query(models.Asset).filter(models.Asset.asset_type == models.AssetType.FRAME).all()
    selected_frame = None
    if frame_assets:
         selected_frame = random.choice(frame_assets)

    return {
        "background": selected_background,
        "frame": selected_frame,
        "text_content": criteria.get("text_content"),
        "dimensions": criteria.get("dimensions")
    }
