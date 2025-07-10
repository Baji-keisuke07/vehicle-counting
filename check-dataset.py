import os
import xml.etree.ElementTree as ET

# Path to the Annotations folder
annotations_dir = "./Annotations"

# Set to store unique class names
classes = set()

# Walk through all subdirectories
for root, _, files in os.walk(annotations_dir):
    for file in files:
        if file.endswith(".xml"):
            file_path = os.path.join(root, file)
            try:
                tree = ET.parse(file_path)
                root_tag = tree.getroot()

                for obj in root_tag.findall("object"):
                    class_name = obj.find("name").text
                    classes.add(class_name)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Print all found classes
print("\n🔍 Unique classes found:")
for i, c in enumerate(sorted(classes), 1):
    print(f"{i}. {c}")

print(f"\n✅ Total unique classes: {len(classes)}")





'''

🔍 Unique classes found:
1. animal
2. autorickshaw
3. bicycle
4. bus
5. car
6. caravan
7. motorcycle
8. person
9. rider
10. traffic light
11. traffic sign
12. trailer
13. train
14. truck
15. vehicle fallback



'''
