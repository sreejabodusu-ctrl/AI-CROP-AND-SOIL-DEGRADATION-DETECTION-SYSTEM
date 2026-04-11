def get_solution(prediction):
    solutions = {
        "Healthy": {
            "control": "No action needed.",
            "prevention": "Maintain crop diversity, use companion planting, regular monitoring, and proper sanitation. Keep fields weed-free and ensure balanced fertilization."
        },
        "Aphids": {
            "control": "Use insecticidal soap, neem oil spray, or introduce ladybugs as natural predators. Avoid broad-spectrum insecticides.",
            "prevention": "Plant companion plants like marigolds or nasturtiums, avoid over-fertilizing with nitrogen, and encourage beneficial insects."
        },
        "Whiteflies": {
            "control": "Use yellow sticky traps, neem oil, or systemic insecticides. Ensure good air circulation to prevent infestations.",
            "prevention": "Avoid planting near infested areas, use reflective mulches, and maintain plant health to reduce susceptibility."
        },
        "Caterpillars": {
            "control": "Hand-pick larvae, use Bacillus thuringiensis (Bt) spray, or apply organic pesticides like spinosad.",
            "prevention": "Rotate crops annually, remove plant debris, and use row covers during vulnerable growth stages."
        },
        "Beetles": {
            "control": "Use row covers, hand-picking, or apply diatomaceous earth. For severe infestations, use targeted insecticides.",
            "prevention": "Plant trap crops, maintain field cleanliness, and avoid planting susceptible varieties in known beetle areas."
        },
        "Mites": {
            "control": "Increase humidity, use miticides like sulfur or neem oil. Avoid overuse of water that can promote mite populations.",
            "prevention": "Avoid drought stress, use appropriate irrigation, and introduce predatory mites as biological control."
        },
        "Soil Degradation": {
            "control": "Add organic compost, improve drainage, test soil pH and nutrients, implement crop rotation, and apply cover crops to restore soil structure.",
            "prevention": "Practice sustainable farming, minimize tillage, avoid overuse of chemicals, and maintain soil organic matter. Test soils regularly and rotate crops to preserve fertility."
        },
        "Low Soil Moisture": {
            "control": "Soil moisture low. Apply deep, infrequent irrigation; use mulch; and consider drip irrigation to improve moisture retention.",
            "prevention": "Build organic matter, mulch soil, practice no-till, and schedule watering early morning to reduce evaporation. Monitor moisture with a probe and adjust irrigation accordingly."
        }
    }
    default_solution = {
        "control": "No specific recommendation available for this prediction.",
        "prevention": "Please verify the prediction and ensure the correct crop image was uploaded."
    }
    return solutions.get(prediction, default_solution)