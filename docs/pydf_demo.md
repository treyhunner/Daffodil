# Python Daffodil (Pydf) Demo

 Python Daffodil (Pydf) is a simple and flexible dataframe package for use with Python.
This page will demonstrate the functionality of Daffodil by showing actual code and results of 
running that code. Daffodil is a good match for many common algorithms in data pipelines and other conversion use cases.
    
For more information about Daffodil, see [https://github.com/raylutz/Pydf/blob/main/README.md]()

This page is the result of using simple "notebook" functionality (md_demo.py)
which will create a markdown "notebook" report by printing a code block and then run and capture the result. The report can
be viewed directly or converted to HTML for use on a static website.

## Create a new empty table



```python
    from Pydf.Pydf import Pydf
    
    my_pydf = Pydf()
    
    md_report += f"The empty my_pydf:\n{my_pydf}\n"
    md_report += f"{bool(my_pydf)=}\n"
    
    # note here that testing my_pydf produces "False" if there is nothing in the array,
    # even though the instance itself exists.
```


The empty my_pydf:

\[0 rows x 0 cols; keyfield=; 0 keys ] (Pydf)

bool(my_pydf)=False
## Append some rows to the pydf object



```python
    # here we append dictionaries to the pydf array.
    # The column header is determined from the first dictionary added if it
    # is not otherwise initialized.
    
    my_pydf.append({'A': 1,  'B': 2, 'C': 3})  
    my_pydf.append({'A': 5,  'C': 7, 'B': 6})  
    my_pydf.append({'C': 10, 'A': 8, 'B': 9})
    
    md_report += f"The appended my_pydf:\n{my_pydf}\n"
    # notice that when each row is appended, the columns are respected,
    # even if the data is provided in a different order.
```



The appended my_pydf:
| A | B | C  |
| -: | -: | -: |
| 1 | 2 |  3 |
| 5 | 6 |  7 |
| 8 | 9 | 10 |

\[3 rows x 3 cols; keyfield=; 0 keys ] (Pydf)

## Read and write individual cells by row,col indices



```python
    # replace value at row 2, col 1 (i.e. 9) with value from row 1, col 0 (i.e. 5)
    # multiplied by the value in cell [2,2] (i.e. 10) resulting in 50 at [2,1].
    # Note that row and column indices start at 0, and are in row, col order (not x,y).
    
    my_pydf[2,1] = my_pydf[1,0] * my_pydf[2,2]

    md_report += f"The modified my_pydf:\n{my_pydf}\n"
```



The modified my_pydf:
| A | B  | C  |
| -: | -: | -: |
| 1 |  2 |  3 |
| 5 |  6 |  7 |
| 8 | 50 | 10 |

\[3 rows x 3 cols; keyfield=; 0 keys ] (Pydf)

## Read columns and rows



```python
    # when accessing a column or row using indices will return a list.
    # Columns can be indexed by number or by column name, which must be a str.
    
    col_2 = my_pydf[:,2]
    row_1 = my_pydf[1]
    col_B = my_pydf[:,'B']

    md_report += f"- {col_2=}\n- {row_1=}\n- {col_B=}\n"
```



- col_2=[3, 7, 10]
- row_1=[5, 6, 7]
- col_B=[2, 6, 50]
## Read rows and columns using methods



```python
    # when using methods to access: columns are returned as lists, 
    # and rows are returned as dicts.
    
    col_2 = my_pydf.icol(2)
    row_1 = my_pydf.irow(1)
    col_B = my_pydf.col('B')

    md_report += f"- {col_2=}\n- {row_1=}\n- {col_B=}\n"
```



- col_2=[3, 7, 10]
- row_1={'A': 5, 'B': 6, 'C': 7}
- col_B=[2, 6, 50]
## Insert a new column "Category" on left, and make it the keyfield

Rows in a Pydf instance can be indexed using an existing column, by specifying that column as the keyfield.
        This will create the keydict kd which creates the index from each value. It must have unique hashable values. 
        The keyfield can be set at the same time the column is added.
        The key dictionary kd is maintained during all pydf manipulations.
        A pydf generated by selecting some rows from the source pydf will maintain the same keyfield, and .keys()
        method will return the subset of keys that exist in that pydf.

```python
    # Add a column on the left (icol=0) and set it as the keyfield.

    my_pydf.insert_icol(icol=0, 
            col_la=['house', 'car', 'boat'], 
            colname='Category', 
            keyfield='Category')

    md_report += f"my_pydf:\n{my_pydf}\n"
```



my_pydf:
| Category | A | B  | C  |
| -------: | -: | -: | -: |
|    house | 1 |  2 |  3 |
|      car | 5 |  6 |  7 |
|     boat | 8 | 50 | 10 |

\[3 rows x 4 cols; keyfield=Category; 3 keys ] (Pydf)

## Select a record by the key:

Selecting one record by the key will return a dictionary.

```python
    da = my_pydf.select_record_da('car')

    md_report += f"Result:\n\n- {da=}\n"
```



Result:

- da={'Category': 'car', 'A': 5, 'B': 6, 'C': 7}
## Append more records from a lod

When records are appended from a lod (list of dict), they are appended as rows,
    the columns are respected, and the kd is updated. Using a pydf
    instance is about 1/3 the size of an equivalent lod because the dictionary
    keys are not repeated for each row in the array.

```python
    lod = [{'Category': 'mall',  'A': 11,  'B': 12, 'C': 13},
           {'Category': 'van',   'A': 14,  'B': 15, 'C': 16},
           {'A': 17,  'C': 19, 'Category': 'condo', 'B': 18},
          ]

    my_pydf.append(lod)  
    
    md_report += f"The appended my_pydf:\n{my_pydf}\n"
```



The appended my_pydf:
| Category | A  | B  | C  |
| -------: | -: | -: | -: |
|    house |  1 |  2 |  3 |
|      car |  5 |  6 |  7 |
|     boat |  8 | 50 | 10 |
|     mall | 11 | 12 | 13 |
|      van | 14 | 15 | 16 |
|    condo | 17 | 18 | 19 |

\[6 rows x 4 cols; keyfield=Category; 6 keys ] (Pydf)

## Update records

updating records mutates the existing pydf instance, and works
        like a database table. The keyvalue in the designated keyfield
        determines which record is updated. This uses the append()
        method because appending respects the keyfield, if it is defined.

```python
    lod = [{'Category': 'car',  'A': 25,  'B': 26, 'C': 27},
           {'Category': 'house', 'A': 31,  'B': 32, 'C': 33},
          ]

    my_pydf.append(lod)  
    
    md_report += f"The updated my_pydf:\n{my_pydf}\n"
```



The updated my_pydf:
| Category | A  | B  | C  |
| -------: | -: | -: | -: |
|    house | 31 | 32 | 33 |
|      car | 25 | 26 | 27 |
|     boat |  8 | 50 | 10 |
|     mall | 11 | 12 | 13 |
|      van | 14 | 15 | 16 |
|    condo | 17 | 18 | 19 |

\[6 rows x 4 cols; keyfield=Category; 6 keys ] (Pydf)

## Add a column "is_vehicle"



```python
    my_pydf.insert_col(colname='is_vehicle', col_la=[0,1,1,0,1,0], icol=1)

    md_report += f"The updated my_pydf:\n{my_pydf}\n"
```



The updated my_pydf:
| Category | is_vehicle | A  | B  | C  |
| -------: | ---------: | -: | -: | -: |
|    house |          0 | 31 | 32 | 33 |
|      car |          1 | 25 | 26 | 27 |
|     boat |          1 |  8 | 50 | 10 |
|     mall |          0 | 11 | 12 | 13 |
|      van |          1 | 14 | 15 | 16 |
|    condo |          0 | 17 | 18 | 19 |

\[6 rows x 5 cols; keyfield=Category; 6 keys ] (Pydf)

## pydf bool

For pydf, bool() simply determines if the pydf exists and is not empty.
        This functionality makes it easy to use `if pydf:` to test if the
        pydf is not None and is not empty. This does not evaluate the __content__
        of the array, only whether contents exists in the array. Thus,
        an array with 0, False, or '' still is regarded as having contents.
        In contrast, Pandas raises an error if you try: ```bool(df)```.
        Normally, a lol structure that has an internal empty list is True,
        i.e. `bool([[]])` will evaluate as true while `bool(Pydf(lol=[[]]))` is False.

```python
    md_report += f"- {bool(my_pydf)=}\n"
    md_report += f"- {bool(Pydf(lol=[]))=}\n"
    md_report += f"- {bool(Pydf(lol=[[]]))=}\n"
    md_report += f"- {bool(Pydf(lol=[[0]]))=}\n"
    md_report += f"- {bool(Pydf(lol=[['']]))=}\n"
    md_report += f"- {bool(Pydf(lol=[[False]]))=}\n\n"
```



- bool(my_pydf)=True
- bool(Pydf(lol=[]))=False
- bool(Pydf(lol=[[]]))=False
- bool(Pydf(lol=[[0]]))=True
- bool(Pydf(lol=[['']]))=True
- bool(Pydf(lol=[[False]]))=True

## pydf attributes



```python
    md_report += f"- {len(my_pydf)=}\n"
    md_report += f"- {my_pydf.len()=}\n"
    md_report += f"- {my_pydf.shape()=}\n"
    md_report += f"- {my_pydf.columns()=}\n"
    md_report += f"- {my_pydf.keys()=}\n"
```



- len(my_pydf)=6
- my_pydf.len()=6
- my_pydf.shape()=(6, 5)
- my_pydf.columns()=['Category', 'is_vehicle', 'A', 'B', 'C']
- my_pydf.keys()=['house', 'car', 'boat', 'mall', 'van', 'condo']
## get_existing_keys

check a list of keys to see if they are defined in the pydf instance

```python
    existing_keys_ls = my_pydf.get_existing_keys(['house', 'boat', 'RV'])
    md_report += f"- {existing_keys_ls=}\n"
```



- existing_keys_ls=['house', 'boat']
## select_records_pydf

select multiple records using a list of keys and create a new pydf instance. 
        Also orders the records according to the list provided.

```python
    wheels_pydf = my_pydf.select_records_pydf(['van', 'car'])
    md_report += f"wheels_pydf:\n{wheels_pydf}\n"
```



wheels_pydf:
| Category | is_vehicle | A  | B  | C  |
| -------: | ---------: | -: | -: | -: |
|      van |          1 | 14 | 15 | 16 |
|      car |          1 | 25 | 26 | 27 |

\[2 rows x 5 cols; keyfield=Category; 2 keys ] (Pydf)

## select_by_dict

select_by_dict offers a way to select for all exact matches to dict,
        or if inverse is set, the set that does not match.

```python
    vehicles_pydf  = my_pydf.select_by_dict({'is_vehicle':1})
    buildings_pydf = my_pydf.select_by_dict({'is_vehicle':0})
    # or
    buildings_pydf = my_pydf.select_by_dict({'is_vehicle':1}, inverse=True)

    md_report += f"vehicles_pydf:\n{vehicles_pydf}\nbuildings_pydf:\n{buildings_pydf}\n"
```



vehicles_pydf:
| Category | is_vehicle | A  | B  | C  |
| -------: | ---------: | -: | -: | -: |
|      car |          1 | 25 | 26 | 27 |
|     boat |          1 |  8 | 50 | 10 |
|      van |          1 | 14 | 15 | 16 |

\[3 rows x 5 cols; keyfield=Category; 3 keys ] (Pydf)

buildings_pydf:
| Category | is_vehicle | A  | B  | C  |
| -------: | ---------: | -: | -: | -: |
|    house |          0 | 31 | 32 | 33 |
|     mall |          0 | 11 | 12 | 13 |
|    condo |          0 | 17 | 18 | 19 |

\[3 rows x 5 cols; keyfield=Category; 3 keys ] (Pydf)

## use `select_where` to select rows where column 'C' is over 20



```python
    high_c_pydf = my_pydf.select_where(lambda row: bool(row['C'] > 20))

    md_report += f"high_c_pydf:\n{high_c_pydf}\n"
```



high_c_pydf:
| Category | is_vehicle | A  | B  | C  |
| -------: | ---------: | -: | -: | -: |
|    house |          0 | 31 | 32 | 33 |
|      car |          1 | 25 | 26 | 27 |

\[2 rows x 5 cols; keyfield=Category; 2 keys ] (Pydf)

## convert to pandas DataFrame



```python
    my_df = my_pydf.to_pandas_df()

    md_report += f"\nConverted DataFrame:\n```\n{my_df}\n```\n"
```




Converted DataFrame:
```
  Category  is_vehicle   A   B   C
0    house           0  31  32  33
1      car           1  25  26  27
2     boat           1   8  50  10
3     mall           0  11  12  13
4      van           1  14  15  16
5    condo           0  17  18  19
```
## Add index column 'idx' to the dataframe at the left, starting at 0.



```python
    my_pydf.insert_idx_col(colname='idx') #, icol=0, startat=0)

    md_report += f"\nModified pydf:\n{my_pydf}\n\n"
```




Modified pydf:
| idx | Category | is_vehicle | A  | B  | C  |
| --: | -------: | ---------: | -: | -: | -: |
|   0 |    house |          0 | 31 | 32 | 33 |
|   1 |      car |          1 | 25 | 26 | 27 |
|   2 |     boat |          1 |  8 | 50 | 10 |
|   3 |     mall |          0 | 11 | 12 | 13 |
|   4 |      van |          1 | 14 | 15 | 16 |
|   5 |    condo |          0 | 17 | 18 | 19 |

\[6 rows x 6 cols; keyfield=Category; 6 keys ] (Pydf)

