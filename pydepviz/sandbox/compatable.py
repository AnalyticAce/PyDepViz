import importlib.metadata as im

def get_package_metadata(package_name):
    try:
        # Get package distribution metadata
        distribution = im.metadata(package_name)
        
        # You can fetch various information like version, dependencies, etc.
        metadata_info = {
            "name": distribution["Name"],
            "version": distribution["Version"],
            "summary": distribution.get("Summary", "No summary available"),
            "author": distribution.get("Author", "No author information"),
            "author_email": distribution.get("Author-email", "No author email"),
            "license": distribution.get("License", "No license info"),
            "dependencies": distribution.get("Requires-Dist", "No dependencies listed"),
            "url": distribution.get("Home-page", "No URL provided"),
            "classifiers": distribution.get("Classifier", "No classifiers available"),
            
        }
        
        return metadata_info
    except KeyError:
        print(f"Package {package_name} not found in the metadata.")
        return None

# Test for a package
package_name = "python-dateutil"
metadata = get_package_metadata(package_name)

if metadata:
    for key, value in metadata.items():
        print(f"{key}: {value}")
