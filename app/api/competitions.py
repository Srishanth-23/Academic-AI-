import requests
import json
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter()

# Replace this with the actual published CSV link from Google Sheets
# Format: https://docs.google.com/spreadsheets/d/e/2PACX-.../pub?output=csv
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT37fVb54jS6C5bONw2C-rYyQ198Y0hA9K_z2m4r7qWbI8qQ2vN7aF_t0L/pub?output=csv" # Placeholder

def parse_csv(csv_text: str) -> List[Dict[str, Any]]:
    # Simple CSV parser since we cannot reliably use pandas/csv on all containers
    lines = csv_text.strip().split('\n')
    if not lines:
        return []
    
    headers = [h.strip() for h in lines[0].split(',')]
    data = []
    
    for i, line in enumerate(lines[1:]):
        # Basic split (will break on commas inside quotes, but good for simple sheets)
        row_values = line.split(',')
        row_dict = {"id": str(i + 1)}
        
        for j, header in enumerate(headers):
            if j < len(row_values):
                val = row_values[j].strip()
                # Handle tags which might be pipe-separated or space-separated
                if header.lower() == 'tags':
                    row_dict[header.lower()] = [t.strip() for t in val.split('|')] if val else []
                else:
                    row_dict[header.lower()] = val
            else:
                row_dict[header.lower()] = ""
                
        data.append(row_dict)
        
    return data

@router.get("/")
async def get_competitions():
    """
    Fetches competition data from a published Google Sheet (CSV format).
    Expected columns: name, org, type, deadline, prize, level, link, description, tags
    """
    try:
        # Instead of auth, the easiest way for users is to File -> Share -> Publish to Web (as CSV)
        # This requires zero auth configuration on the backend and updates automatically.
        response = requests.get(SHEET_CSV_URL)
        response.raise_for_status()
        
        competitions = parse_csv(response.text)
        
        # Format mapping to match frontend expectations
        formatted_comps = []
        for c in competitions:
            # Map sheet columns to frontend type:
            # { id, name, org, type, deadline, prize, link, level, description, tags }
            formatted_comps.append({
                "id": c.get("id"),
                "name": c.get("name") or c.get("title", "Unnamed Competition"),
                "org": c.get("org") or c.get("organization", "Unknown"),
                "type": c.get("type", "Other"),
                "deadline": c.get("deadline", "Rolling"),
                "prize": c.get("prize", "TBD"),
                "link": c.get("link", ""),
                "level": c.get("level", "National"),
                "description": c.get("description", ""),
                "tags": c.get("tags", [])
            })
            
        return {"status": "success", "data": formatted_comps}
        
    except Exception as e:
        print(f"Error fetching sheet: {e}")
        # Return fallback data if sheet fails
        return {"status": "error", "message": "Failed to fetch spreadsheet. Please ensure it is published to web.", "data": []}
