square_list = [n**2 for n in range(5)]
print(square_list)
square_generator = (n**2 for n in range(5))
print(list(square_generator))

str_ = "qwerty"
print(list(str_))
