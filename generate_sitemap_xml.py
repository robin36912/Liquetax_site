import os
from datetime import datetime
from pathlib import Path

base_path = Path("/Users/apple/Documents/public_html")
base_url = "https://liquetax.com"

# Priority settings for different page types
priorities = {
    "index.html": "1.0",
    "about-us.html": "0.9",
    "contact-us.html": "0.8",
    "business-setup": "0.9",
    "registration": "0.9",
    "tax": "0.9",
    "compliances": "0.8",
    "export-import": "0.8",
    "gem": "0.8",
    "more": "0.7",
    "blog": "0.6"
}

def get_priority(path):
    if path.name == "index.html":
        return priorities["index.html"]
    
    parent = path.parent.name
    if parent in priorities:
        return priorities[parent]
    
    return "0.5"

def generate_sitemap():
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    today = datetime.today().strftime('%Y-%m-%d')

    # Process all HTML files
    for root, _, files in os.walk(base_path):
        root_path = Path(root)
        if ".git" in root or "config" in root:
            continue

        for file in files:
            if not file.endswith(".html"):
                continue

            file_path = root_path / file
            rel_path = file_path.relative_to(base_path)

            # Skip certain files
            if file in ["404.html"]:
                continue

            # Create clean URL (without .html)
            if file == "index.html":
                url_path = str(rel_path.parent)
            else:
                url_path = str(rel_path.with_suffix(""))

            # Ensure proper URL formatting
            url_path = url_path.replace("\\", "/")
            if url_path and not url_path.startswith("/"):
                url_path = "/" + url_path
            if not url_path.endswith("/"):
                url_path += "/"

            # Remove index.html from URL
            url_path = url_path.replace("index.html", "")
            
            # Generate URL entry
            url = f"{base_url}{url_path}"
            priority = get_priority(file_path)

            sitemap.extend([
                "  <url>",
                f"    <loc>{url}</loc>",
                f"    <lastmod>{today}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>"
            ])

    sitemap.append("</urlset>")
    return "\n".join(sitemap)

if __name__ == "__main__":
    sitemap_content = generate_sitemap()
    sitemap_path = base_path / "sitemap.xml"
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    
    print(f"✅ Generated sitemap.xml at {sitemap_path}")
