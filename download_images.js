const fs = require('fs');
const { exec } = require('child_process');

const equipment = [
    { "id": "26VNA1", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26vna1/" },
    { "id": "26TPA8", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26tpa8/" },
    { "id": "26SPA6", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26spa6/" },
    { "id": "26SCA4", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26sca4/" },
    { "id": "26SCA5", "url": "https://www.carrier.com/residential/en/us/products/air-conditioners/26sca5/" },
    { "id": "59MN7", "url": "https://www.carrier.com/residential/en/us/products/furnaces/59mn7/" },
    { "id": "59TN6", "url": "https://www.carrier.com/residential/en/us/products/furnaces/59tn6/" },
    { "id": "59TP6", "url": "https://www.carrier.com/residential/en/us/products/furnaces/59tp6/" },
    { "id": "58TP0", "url": "https://www.carrier.com/residential/en/us/products/furnaces/58tp0/" },
    { "id": "58DLA", "url": "https://www.carrier.com/residential/en/us/products/furnaces/58dla/" },
    { "id": "27VNA3", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27vna3/" },
    { "id": "27VNA1", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27vna1/" },
    { "id": "27TPA8", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27tpa8/" },
    { "id": "27SPA6", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27spa6/" },
    { "id": "27SCA5", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27sca5/" },
    { "id": "27VNA0", "url": "https://www.carrier.com/residential/en/us/products/heat-pumps/27vna0/" },
    { "id": "FE5B", "url": "https://www.carrier.com/residential/en/us/products/fan-coils/fe5b/" },
    { "id": "FT5", "url": "https://www.carrier.com/residential/en/us/products/fan-coils/ft5/" },
    { "id": "FJ5", "url": "https://www.carrier.com/residential/en/us/products/fan-coils/fj5/" },
    { "id": "SYSTXCCITC01-C", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/systxccitc01-c/" },
    { "id": "SYSTXCCWIC01-C", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/systxccwic01-c/" },
    { "id": "EB-STATE6ICR-01", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/eb-state6icr-01/" },
    { "id": "TSTATCCEWF-01", "url": "https://www.carrier.com/residential/en/us/products/thermostats/smart-thermostats/tstatccewf-01/" },
    { "id": "DGAPA", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/air-purifiers/air-purifier-dgapa/" },
    { "id": "UVCAP", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/air-purifiers/carbon-air-purifier-uvcap/" },
    { "id": "EZXCAB", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/air-purifiers/ezxcab/" },
    { "id": "HUMCRSTM", "url": "https://www.carrier.com/residential/en/us/products/indoor-air-quality/humidifiers/humcrstm/" },
    { "id": "37MPRA", "url": "https://www.carrier.com/residential/en/us/products/ductless-mini-splits/37mpra/" },
    { "id": "45MPHA", "url": "https://www.carrier.com/residential/en/us/products/ductless-mini-splits/45mpha/" },
    { "id": "48NG", "url": "https://www.carrier.com/residential/en/us/products/combined-heating-cooling/48ng/" },
    { "id": "50VR", "url": "https://www.carrier.com/residential/en/us/products/combined-heating-cooling/50vr/" }
];

const downloadImage = (item) => {
    // Construct the image URL based on the pattern
    // Pattern: [base_url]/images/[id_lowercase]-hero.jpg
    // Note: Some URLs might have trailing slashes which we need to handle
    let baseUrl = item.url.endsWith('/') ? item.url.slice(0, -1) : item.url;
    let idLower = item.id.toLowerCase();

    // Special handling for complex IDs if needed, but let's try strict pattern first
    // For coastal units like 26TPA8***C, the URL usually just uses the base model or a specific slug.
    // The provided URLs in the list seem to be the base product pages.

    // Fix for specific known deviations if any (e.g. thermostats might be different)
    // Based on subagent, thermostat was: .../systxccitc01-c/images/systxccitc01-c-hero.jpg
    // This matches the pattern!

    const imageUrl = `${baseUrl}/images/${idLower}-hero.jpg`;
    const outputPath = `images/${item.id}.jpg`;

    const cmd = `curl -L -A "Mozilla/5.0" "${imageUrl}" -o "${outputPath}" --fail`;

    exec(cmd, (error, stdout, stderr) => {
        if (error) {
            console.error(`Failed to download ${item.id}: ${imageUrl}`);
            // Try fallback: sometimes it's just .jpg without -hero, or different casing
            // But for now, let's just log failures.
        } else {
            console.log(`Downloaded ${item.id}`);
        }
    });
};

equipment.forEach(item => downloadImage(item));
