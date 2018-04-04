import xml.etree.ElementTree as ET

tree = ET.parse('sample_xml.xml')
root = tree.getroot()

print("Root tag:", root.tag)
print("Root[2] tag:", root[2].tag)

ballot = root[2]

for item in ballot:
    print("Title:", item[0].text)
    candidates = item[1]
    for candidate in candidates:
        print("\tCandidate:", candidate.text)


