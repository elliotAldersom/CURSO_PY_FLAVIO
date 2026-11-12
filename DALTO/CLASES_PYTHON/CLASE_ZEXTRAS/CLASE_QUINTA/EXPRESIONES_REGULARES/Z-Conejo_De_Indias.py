import re 

regex = r"(?s)(^.+(M|m)+.+$)"
print(re.match(regex , "@mmmmmmmmmMMMM  brais\n MmmmmmMMM" , re.IGNORECASE))
print("\n_________________________________________\n")

text ="""Que tal mi gentee, espero estén 10/10, están listos?"""
regex = r"(?s)[A-Z].+"
result = re.match(regex, text)
print(result)
print(result.start())
print(result.end())
print(result.span())
print(result.group())
print("\n________________________________________\n_")


text ="""Qué tal mi gentee, espero estén 10/10, están listos?"""
regex = r"[A-Z].{2}"
result = re.search(regex, text)
print(result.group())
print(result.start())
print(result.end())
print(result.span())
print(result.group())
print("\n_________________________________________\n")



text ="""Qué tal mi gentee, espero estén 10/10, están listos?"""
regex = r"[A-Za-z].{2}"
result = re.findall(regex, text)
print(result)
print("\n_________________________________________\n")


text ="""Qué tal mi gentee, espero estén 10/10, están listos?"""
regex = r"[A-Za-z].{2}"
result = re.finditer(regex, text)
print(result)
for match in result:
    print(match.span())
print("\n_________________________________________\n")