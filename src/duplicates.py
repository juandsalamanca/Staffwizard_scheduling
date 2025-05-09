def find_duplicates(lst):
    # Dictionary to store counts of elements
    element_count = {}
    # List to store duplicates
    duplicates = []

    # Count the occurrences of each element
    for item in lst:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1

    # Find elements that appear more than once
    for key, count in element_count.items():
        if count > 1:
            duplicates.append(key)

    return duplicates
