import names

def my_names2():
    new_name=names.get_full_name()
    print(f'{new_name} {len(new_name)-1}')

my_names2()