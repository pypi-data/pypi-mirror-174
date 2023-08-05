# gmanka yml

some useful shortcuts for pyyaml

## installation

```bash
pip install gmanka_yml
```

## functions

- [to_str](#to_str)  
- [to_file](#to_file)  
- [read_str](#read_str)  
- [read_file](#read_file)  

## to_str[^](#functions)

converts any data to yml string and returns it

```py
import gmanka_yml as yml

my_dict = {
    'element_1': 1,
    2: 'element_2',
    3: [
        'list_element_1',
        'list_element_2',
    ]
}

print(yml.to_str(my_dict))
```

output:

```yaml
element_1: 1
2: element_2
3:
- list_element_1
- list_element_2
```

## to_file[^](#functions)

same as [to_str](#to_str), but writes data to file instead of returning

```py
yml.to_file(
    data = my_dict,
    file_path = 'file.yml',
)
```

## read_str[^](#functions)

```py
import gmanka_yml as yml

my_str = '''
element_1: 1
2: element_2
3:
- list_element_1
- list_element_2
'''

my_dict = yml.read_str(my_str)

print(my_dict)

print(type(my_dict))
```

output:

```py
{'element_1': 1, 2: 'element_2', 3: ['list_element_1', 'list_element_2']}

<class 'dict'>
```

## read_file[^](#functions)

same as [read_str](#read_str), but reads data from file

```py
print(yml.read_file('file.yml'))
```
