# Crop calendar data — week-by-week tasks for common Indian crops
# Extend this dict to add more crops

CROP_CALENDAR = {
    "rice": {
        1:  "Prepare nursery bed. Apply basal dose of compost.",
        2:  "Sow pre-germinated seeds in nursery. Maintain thin water layer.",
        3:  "Check for damping-off disease in nursery. Spray copper fungicide if needed.",
        4:  "Transplanting time — seedlings should be 21 days old. Puddle the main field.",
        5:  "Apply first dose of nitrogen (urea) after transplanting. Maintain 5cm water level.",
        6:  "Weed control — hand weed or apply butachlor herbicide.",
        7:  "Check for leaf folder and stem borer. Spray chlorpyrifos if attack is heavy.",
        8:  "Apply second nitrogen dose. Maintain water level.",
        9:  "Monitor for blast disease — brown spots on leaves. Apply tricyclazole if needed.",
        10: "Apply potassium fertilizer (MOP) to strengthen stems.",
        11: "Panicle initiation stage — keep field flooded. Watch for neck blast.",
        12: "Flowering stage — avoid pesticide spray. Maintain water.",
        13: "Grain filling — reduce irrigation slightly. Watch for BPH (brown plant hopper).",
        14: "Hard dough stage — drain field. Stop irrigation.",
        15: "Harvesting time — moisture should be around 20%. Use sharp sickle or harvester.",
        16: "Threshing and drying. Dry grains to 14% moisture before storage.",
    },
    "cotton": {
        1:  "Deep ploughing and field preparation. Apply FYM (farmyard manure).",
        2:  "Sow treated seeds with imidacloprid seed treatment. Row spacing 60×30 cm.",
        3:  "Gap filling — replant empty spots. First irrigation if dry.",
        4:  "Apply pre-emergence herbicide (pendimethalin). Weed control is critical now.",
        5:  "First nitrogen application (urea). Watch for aphids on young leaves.",
        6:  "Thinning — one healthy plant per hill. Apply DAP.",
        7:  "Spray neem oil for sucking pest control (whitefly, jassids).",
        8:  "Squaring stage — flower buds forming. Apply second nitrogen dose.",
        9:  "Flowering begins. Watch for bollworm eggs on leaves. Set pheromone traps.",
        10: "Spray Bt (Bacillus thuringiensis) for bollworm if egg count is high.",
        11: "Boll development — avoid water stress. Apply micronutrients (zinc sulfate).",
        12: "Watch for pink bollworm. Spray spinosad or emamectin benzoate if needed.",
        13: "Boll opening begins. Stop nitrogen. Reduce irrigation.",
        14: "First picking — pick fully open white bolls only.",
        15: "Second picking after 10–12 days. Check for boll rot after rain.",
        16: "Final picking and field clearing. Deep plough to destroy pest pupae.",
    },
    "maize": {
        1:  "Field preparation — deep plough, apply FYM. Treat seeds with thiram fungicide.",
        2:  "Sow at 60×25 cm spacing. Apply basal DAP and potash.",
        3:  "Germination check — gap fill any missing spots within 5 days.",
        4:  "First weeding. Apply atrazine herbicide before first rain.",
        5:  "First nitrogen top dressing (urea). Earth up soil around plants.",
        6:  "Watch for fall army worm — check whorl for feeding damage. Spray chlorantraniliprole.",
        7:  "Second nitrogen top dressing. Remove tillers (side shoots).",
        8:  "Knee-high stage — critical water requirement. Irrigate if dry.",
        9:  "Tasseling begins. Avoid any stress — this determines yield.",
        10: "Silking stage — pollination happening. Do NOT spray any insecticide now.",
        11: "Cob development. Watch for stem borer. Apply carbofuran granules in whorl.",
        12: "Grain filling — maintain moisture. Apply foliar spray of urea 2%.",
        13: "Milky stage — test kernel by pressing. Reduce irrigation.",
        14: "Dough stage — husks turning dry. Stop irrigation.",
        15: "Physiological maturity — black layer formed at kernel base. Ready to harvest.",
        16: "Harvest when grain moisture is 25–30%. Dry cobs before shelling.",
    },
    "tomato": {
        1:  "Prepare raised nursery beds. Sow seeds and cover with fine soil.",
        2:  "Germination in 5–7 days. Water daily with rose-can. Shade in afternoon.",
        3:  "Thin seedlings to 5 cm apart. Watch for damping off.",
        4:  "Transplant 25-day-old seedlings to main field. Spacing: 60×45 cm.",
        5:  "Apply starter fertilizer (DAP). First irrigation after transplanting.",
        6:  "Staking — drive bamboo stakes. Train plants upward.",
        7:  "Watch for whitefly and aphids — spray imidacloprid if population is high.",
        8:  "First flowering — spray boron 0.1% for fruit set. Avoid excess nitrogen.",
        9:  "Fruit set stage. Watch for early blight — brown spots with rings. Spray mancozeb.",
        10: "Apply calcium nitrate spray to prevent blossom end rot.",
        11: "Green fruit development. Watch for tomato leaf curl virus (TLCV) — remove infected plants.",
        12: "Apply potassium nitrate foliar spray for fruit colour and quality.",
        13: "Fruits turning colour — reduce irrigation. Watch for fruit borer.",
        14: "First harvest of mature red fruits. Harvest every 3–4 days.",
        15: "Continue harvest. Apply foliar nutrition to extend crop life.",
        16: "Final harvest and crop termination. Destroy crop residues.",
    },
    "wheat": {
        1:  "Deep ploughing. Apply FYM. Ensure good seed bed preparation.",
        2:  "Sow treated seeds. Apply basal dose of DAP. Row spacing 22.5 cm.",
        3:  "Pre-emergence irrigation (crown root initiation) — most critical irrigation.",
        4:  "First nitrogen top dressing at tillering stage.",
        5:  "Watch for yellow rust — yellow stripes on leaves. Spray propiconazole if seen.",
        6:  "Second irrigation at tillering. Weed control with clodinafop herbicide.",
        7:  "Second nitrogen top dressing. Watch for aphids on leaves.",
        8:  "Jointing stage — plant growing rapidly. Third irrigation.",
        9:  "Booting stage — flag leaf visible. Apply foliar zinc sulfate.",
        10: "Heading and flowering. Fourth irrigation. Watch for Karnal bunt disease.",
        11: "Milky grain stage — fifth irrigation. Critical for grain filling.",
        12: "Dough stage — reduce irrigation. Watch for stem rust.",
        13: "Grain hardening. Stop irrigation. Watch for terminal heat stress.",
        14: "Crop turns golden yellow — ready for harvest.",
        15: "Harvest using combine or manually. Thresh immediately to avoid field losses.",
        16: "Dry grain to 12% moisture. Store in clean gunny bags with neem leaves.",
    },
}

def get_week_task(crop_name, sowing_date_str):
    """Returns (week_number, task) based on days since sowing."""
    from datetime import datetime
    try:
        sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d")
        days_elapsed = (datetime.now() - sowing_date).days
        if days_elapsed < 0:
            return 0, "Sowing date is in the future. Come back after sowing!"
        week = (days_elapsed // 7) + 1
        crop_key = crop_name.lower().strip()
        calendar = CROP_CALENDAR.get(crop_key)
        if not calendar:
            return week, None
        max_week = max(calendar.keys())
        if week > max_week:
            return week, "Crop cycle complete. Field can be prepared for next crop."
        return week, calendar.get(week, "No specific task this week. Monitor crop regularly.")
    except Exception:
        return 0, None
