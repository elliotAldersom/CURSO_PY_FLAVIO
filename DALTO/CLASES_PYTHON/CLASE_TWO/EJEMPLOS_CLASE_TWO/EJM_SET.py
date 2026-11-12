a = set(["hola","causa","que tal","cómo estás"]);

print(a);
print(type(a));


# USANDO FROZENSET PARA INTORDUCIR SETS EN UN SET:
b = frozenset(["que tal","cómo estás"]);

print(b);
print(type(b));

a_1 = frozenset(a)
c = {b,a_1};
print(c);
print(type(c));

print(a_1 > b)
print(a_1.issuperset(b))
print(b < a_1);
print(b.issubset(a_1));
print(a_1.isdisjoint(b))