# test_pydf
# copyright (c) 2024 Ray Lutz

#import os
import sys
import unittest
import numpy as np
import pandas as pd
#from io import BytesIO
from pathlib import Path
sys.path.append('..')

from Pydf.Pydf import Pydf
from Pydf import pydf_utils as utils

class TestPydf(unittest.TestCase):

    maxDiff = None
    
    # initialization
    def test_init_default_values(self):
        pydf = Pydf()
        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.hd, {})
        self.assertEqual(pydf.lol, [])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, {})
        self.assertEqual(pydf._iter_index, 0)

    def test_init_custom_values(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 2], [3, 4]]
        kd = {1: 0, 3: 1}
        dtypes = {'col1': int, 'col2': str}
        expected_lol = [[1, '2'], [3, '4']]
        pydf = Pydf(cols=cols, lol=lol, dtypes=dtypes, name='TestPydf', keyfield='col1')
        self.assertEqual(pydf.name, 'TestPydf')
        self.assertEqual(pydf.keyfield, 'col1')
        self.assertEqual(pydf.hd, hd)
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.kd, kd)
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)

    def test_init_no_cols_but_dtypes(self):
        #cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 2], [3, 4]]
        kd = {1: 0, 3: 1}
        dtypes = {'col1': int, 'col2': str}
        expected_lol = [[1, '2'], [3, '4']]
        pydf = Pydf(lol=lol, dtypes=dtypes, name='TestPydf', keyfield='col1')
        self.assertEqual(pydf.name, 'TestPydf')
        self.assertEqual(pydf.keyfield, 'col1')
        self.assertEqual(pydf.hd, hd)
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.kd, kd)
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)

    # shape
    def test_shape_empty(self):
        # Test shape method with an empty Pydf object
        pydf = Pydf()
        self.assertEqual(pydf.shape(), (0, 0))

    def test_shape_non_empty(self):
        # Test shape method with a non-empty Pydf object
        data = [[1, 'A'], [2, 'B'], [3, 'C']]
        cols = ['Col1', 'Col2']
        pydf = Pydf(lol=data, cols=cols)
        self.assertEqual(pydf.shape(), (3, 2))

    def test_shape_no_colnames(self):
        # Test shape method with a Pydf object initialized without colnames
        data = [[1, 'A'], [2, 'B'], [3, 'C']]
        pydf = Pydf(lol=data)
        self.assertEqual(pydf.shape(), (3, 2))

    def test_shape_empty_data(self):
        # Test shape method with a Pydf object initialized with empty data
        cols = ['Col1', 'Col2']
        pydf = Pydf(cols=cols)
        self.assertEqual(pydf.shape(), (0, 0))

    def test_shape_empty_data_specified(self):
        # Test shape method with a Pydf object initialized with empty data
        cols = ['Col1', 'Col2']
        pydf = Pydf(lol=[], cols=cols)
        self.assertEqual(pydf.shape(), (0, 0))

    def test_shape_empty_data_specified_empty_col(self):
        # Test shape method with a Pydf object initialized with empty data
        cols = ['Col1', 'Col2']
        pydf = Pydf(lol=[[]], cols=cols)
        self.assertEqual(pydf.shape(), (1, 0))

    def test_shape_no_colnames_no_cols(self):
        # Test shape method with a Pydf object initialized without colnames
        data = [[], [], []]
        pydf = Pydf(lol=data)
        self.assertEqual(pydf.shape(), (3, 0))

    def test_shape_colnames_no_cols_empty_rows(self):
        # Test shape method with a Pydf object initialized without colnames
        data = [[], [], []]
        # cols = ['Col1', 'Col2']
        pydf = Pydf(lol=data)
        self.assertEqual(pydf.shape(), (3, 0))

    # __eq__
    
    def test_eq_different_type(self):
        # Test __eq__ method with a different type
        pydf = Pydf()
        other = "not a Pydf object"
        self.assertFalse(pydf == other)

    def test_eq_different_data(self):
        # Test __eq__ method with a Pydf object with different data
        pydf1 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col2'], keyfield='Col1')
        pydf2 = Pydf(lol=[[1, 'X'], [2, 'Y'], [3, 'Z']], cols=['Col1', 'Col2'], keyfield='Col1')
        self.assertFalse(pydf1 == pydf2)

    def test_eq_different_columns(self):
        # Test __eq__ method with a Pydf object with different columns
        pydf1 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col2'], keyfield='Col1')
        pydf2 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col3'], keyfield='Col1')
        self.assertFalse(pydf1 == pydf2)

    def test_eq_different_keyfield(self):
        # Test __eq__ method with a Pydf object with different keyfield
        pydf1 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col2'], keyfield='Col1')
        pydf2 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col2'], keyfield='Col2')
        self.assertFalse(pydf1 == pydf2)

    def test_eq_equal(self):
        # Test __eq__ method with equal Pydf objects
        pydf1 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col2'], keyfield='Col1')
        pydf2 = Pydf(lol=[[1, 'A'], [2, 'B'], [3, 'C']], cols=['Col1', 'Col2'], keyfield='Col1')
        self.assertTrue(pydf1 == pydf2)

    # len(pydf), .len(), .shape(), .num_cols()
    def test_len(self):
        # Test case with an empty dictionary
        my_pydf = Pydf()
        assert len(my_pydf) == 0
        assert my_pydf.len() == 0
        assert my_pydf.num_cols() == 0
        assert my_pydf.shape() == (0, 0)

        # Test case with a dictionary containing one key-value pair
        my_pydf.append({'a': 1, 'b': 2, 'c': 3})
        assert len(my_pydf) == 1
        assert my_pydf.len() == 1
        assert my_pydf.num_cols() == 3
        assert my_pydf.shape() == (1, 3)

        # Test case with a dictionary containing multiple key-value pairs
        my_pydf.append({'a': 4, 'b': 5, 'c': 6})
        my_pydf.append({'a': 7, 'b': 8, 'c': 9})
        assert len(my_pydf) == 3
        assert my_pydf.len() == 3
        assert my_pydf.num_cols() == 3
        assert my_pydf.shape() == (3, 3)

        # Test case with a dictionary containing keys of mixed types
        my_pydf.append({'a': 1, 2: 'b', 'c': True})
        assert len(my_pydf) == 4
        assert my_pydf.len() == 4
        assert my_pydf.num_cols() == 3
        assert my_pydf.shape() == (4, 3)


    # calc_cols
    def test_calc_cols_include_cols(self):
        # Test calc_cols method with include_cols parameter
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types)
        included_cols = pydf.calc_cols(include_cols=['Col1', 'Col3'])
        self.assertEqual(included_cols, ['Col1', 'Col3'])

    def test_calc_cols_exclude_cols(self):
        # Test calc_cols method with exclude_cols parameter
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types)
        excluded_cols = pydf.calc_cols(exclude_cols=['Col2'])
        self.assertEqual(excluded_cols, ['Col1', 'Col3'])

    def test_calc_cols_include_types(self):
        # Test calc_cols method with include_types parameter
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types)
        included_types = pydf.calc_cols(include_types=[int])
        self.assertEqual(included_types, ['Col1'])

    def test_calc_cols_exclude_types(self):
        # Test calc_cols method with exclude_types parameter
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types)
        excluded_types = pydf.calc_cols(exclude_types=[str])
        self.assertEqual(excluded_types, ['Col1', 'Col3'])

    def test_calc_cols_complex(self):
        # Test calc_cols method with multiple parameters
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types)
        selected_cols = pydf.calc_cols(include_cols=['Col1', 'Col2'],
                                       exclude_cols=['Col2'],
                                       include_types=[int, bool])
        self.assertEqual(selected_cols, ['Col1'])

    # rename_cols
    def test_rename_cols(self):
        # Test rename_cols method to rename columns
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types)
        
        # Rename columns using the provided dictionary
        from_to_dict = {'Col1': 'NewCol1', 'Col3': 'NewCol3'}
        pydf.rename_cols(from_to_dict)
        
        # Check if columns are renamed correctly
        expected_columns = ['NewCol1', 'Col2', 'NewCol3']
        self.assertEqual(pydf.columns(), expected_columns)

        # Check if dtypes are updated correctly
        expected_types = {'NewCol1': int, 'Col2': str, 'NewCol3': bool}
        self.assertEqual(pydf.dtypes, expected_types)

    def test_rename_cols_with_keyfield(self):
        # Test rename_cols method when a keyfield is specified
        data = [
            [1, 'A', True],
            [2, 'B', False],
            [3, 'C', True]
        ]
        columns = ['Col1', 'Col2', 'Col3']
        types = {'Col1': int, 'Col2': str, 'Col3': bool}
        pydf = Pydf(lol=data, cols=columns, dtypes=types, keyfield='Col1')
        
        # Rename columns using the provided dictionary
        from_to_dict = {'Col1': 'NewCol1', 'Col3': 'NewCol3'}
        pydf.rename_cols(from_to_dict)
        
        # Check if keyfield is updated correctly
        self.assertEqual(pydf.keyfield, 'NewCol1')
        

    # set_cols
    def test_set_cols_no_existing_cols(self):
        # Test setting column names when there are no existing columns
        pydf = Pydf()
        new_cols = ['A', 'B', 'C']
        pydf.set_cols(new_cols)
        self.assertEqual(pydf.hd, {'A': 0, 'B': 1, 'C': 2})
    
    def test_set_cols_generate_spreadsheet_names(self):
        # Test generating spreadsheet-like column names
        pydf = Pydf(cols=['col1', 'col2'])
        pydf.set_cols()
        self.assertEqual(pydf.hd, {'A': 0, 'B': 1})
    
    def test_set_cols_with_existing_cols(self):
        # Test setting column names with existing columns
        pydf = Pydf(cols=['col1', 'col2'])
        new_cols = ['A', 'B']
        pydf.set_cols(new_cols)
        self.assertEqual(pydf.hd, {'A': 0, 'B': 1})
    
    def test_set_cols_repair_keyfield(self):
        # Test repairing keyfield if column names are already defined
        pydf = Pydf(cols=['col1', 'col2'], keyfield='col1')
        new_cols = ['A', 'B']
        pydf.set_cols(new_cols)
        self.assertEqual(pydf.keyfield, 'A')
    
    def test_set_cols_update_dtypes(self):
        # Test updating dtypes dictionary with new column names
        pydf = Pydf(cols=['col1', 'col2'], dtypes={'col1': int, 'col2': str})
        new_cols = ['A', 'B']
        pydf.set_cols(new_cols)
        self.assertEqual(pydf.dtypes, {'A': int, 'B': str})
    
    def test_set_cols_error_length_mismatch(self):
        # Test error handling when lengths of new column names don't match existing ones
        pydf = Pydf(cols=['col1', 'col2'])
        new_cols = ['A']  # Length mismatch
        with self.assertRaises(AttributeError):
            pydf.set_cols(new_cols)

    def test_set_cols_sanitize(self):
        # sanitizing function
        pydf = Pydf(cols=['col1', 'col2', 'col3'])
        new_cols = ['A', 'A', '']
        pydf.set_cols(new_cols)
        self.assertEqual(pydf.columns(), ['A', 'A_1', 'col2'])
    
    def test_set_cols_sanitize_dif_prefix(self):
        # sanitizing function, different prefix
        pydf = Pydf(cols=['col1', 'col2', 'col3'])
        new_cols = ['A', 'A', '']
        pydf.set_cols(new_cols, unnamed_prefix='Unnamed')
        self.assertEqual(pydf.columns(), ['A', 'A_1', 'Unnamed2'])
    


    # keys
    def test_keys_no_keyfield(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='', dtypes={'col1': int, 'col2': str})

        result = pydf.keys()

        self.assertEqual(result, [])

    def test_keys_with_keyfield(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        result = pydf.keys()

        self.assertEqual(result, [1, 2, 3])

    def test_keys_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        result = pydf.keys()

        self.assertEqual(result, [])  

    # set_keyfield
    def test_set_keyfield_existing_column(self):
        # Test setting keyfield to an existing column
        pydf = Pydf(lol=[[1, 'a'], [2, 'b']], cols=['ID', 'Value'])
        pydf.set_keyfield('ID')
        self.assertEqual(pydf.keyfield, 'ID')
    
    def test_set_keyfield_empty_string(self):
        # Test setting keyfield to an empty string
        pydf = Pydf(lol=[[1, 'a'], [2, 'b']], cols=['ID', 'Value'], keyfield='ID')
        pydf.set_keyfield('')
        self.assertEqual(pydf.keyfield, '')
    
    def test_set_keyfield_nonexistent_column(self):
        # Test trying to set keyfield to a nonexistent column
        pydf = Pydf(lol=[[1, 'a'], [2, 'b']], cols=['ID', 'Value'])
        with self.assertRaises(KeyError):
            pydf.set_keyfield('nonexistent_column')

    # row_idx_of
    def test_row_idx_of_existing_key(self):
        # Test getting row index of an existing key
        pydf = Pydf(lol=[['1', 'a'], ['2', 'b']], cols=['ID', 'Value'], keyfield='ID')
        self.assertEqual(pydf.row_idx_of('1'), 0)
    
    def test_row_idx_of_nonexistent_key(self):
        # Test getting row index of a nonexistent key
        pydf = Pydf(lol=[['1', 'a'], ['2', 'b']], cols=['ID', 'Value'], keyfield='ID')
        self.assertEqual(pydf.row_idx_of('3'), -1)
    
    def test_row_idx_of_no_keyfield(self):
        # Test getting row index when no keyfield is defined
        pydf = Pydf(lol=[['1', 'a'], ['2', 'b']], cols=['ID', 'Value'])
        self.assertEqual(pydf.row_idx_of('1'), -1)
    
    def test_row_idx_of_no_kd(self):
        # Test getting row index when kd is not available
        pydf = Pydf(lol=[['1', 'a'], ['2', 'b']], cols=['ID', 'Value'], keyfield='ID')
        pydf.kd = None
        self.assertEqual(pydf.row_idx_of('1'), -1)


    # get_existing_keys
    def test_get_existing_keys_with_existing_keys(self):
        # Test case where all keys in keylist exist in kd
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], keyfield='Name')
        existing_keys = pydf.get_existing_keys(['a', 'b', 'd'])
        self.assertEqual(existing_keys, ['a', 'b'])

    def test_get_existing_keys_with_no_existing_keys(self):
        # Test case where no keys in keylist exist in kd
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], keyfield='Name')
        existing_keys = pydf.get_existing_keys(['d', 'e', 'f'])
        self.assertEqual(existing_keys, [])

    def test_get_existing_keys_with_empty_keylist(self):
        # Test case where keylist is empty
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], keyfield='Name')
        existing_keys = pydf.get_existing_keys([])
        self.assertEqual(existing_keys, [])

    def test_get_existing_keys_with_empty_pydf(self):
        # Test case where Pydf is empty
        pydf = Pydf()
        existing_keys = pydf.get_existing_keys(['a', 'b', 'c'])
        self.assertEqual(existing_keys, [])



    # calc cols
    def test_calc_cols_with_include_cols(self):
        # Test case where include_cols is provided
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], dtypes={'ID': int, 'Name': str})
        self.assertEqual(pydf.calc_cols(include_cols=['ID']), ['ID'])

    def test_calc_cols_with_exclude_cols(self):
        # Test case where exclude_cols is provided
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], dtypes={'ID': int, 'Name': str})
        self.assertEqual(pydf.calc_cols(exclude_cols=['ID']), ['Name'])

    def test_calc_cols_with_include_types(self):
        # Test case where include_types is provided
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], dtypes={'ID': int, 'Name': str})
        self.assertEqual(pydf.calc_cols(include_types=[str]), ['Name'])

    def test_calc_cols_with_exclude_types(self):
        # Test case where exclude_types is provided
        pydf = Pydf(lol=[[1, 'a'], [2, 'b'], [3, 'c']], cols=['ID', 'Name'], dtypes={'ID': int, 'Name': str})
        self.assertEqual(pydf.calc_cols(exclude_types=[str]), ['ID'])

    def test_calc_cols_with_empty_pydf(self):
        # Test case where Pydf is empty
        pydf = Pydf()
        self.assertEqual(pydf.calc_cols(), [])
        
    def test_calc_cols_with_include_cols_large(self):
        # Test case where include_cols is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(include_cols=['ID', 'Name', 'Flag']), ['ID', 'Name', 'Flag'])

    def test_calc_cols_with_include_cols_large_include_large(self):
        # Test case where include_cols is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(include_cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4']), ['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4'])

    def test_calc_cols_with_exclude_cols_large_enclude_large(self):
        # Test case where exclude_cols is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(exclude_cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4']), ['Flag4'])

    def test_calc_cols_with_exclude_cols_large(self):
        # Test case where exclude_cols is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(exclude_cols=['ID', 'Name', 'Flag']), ['ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'])

    def test_calc_cols_with_include_types_large(self):
        # Test case where include_types is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(include_types=[int, bool]), ['ID', 'Flag', 'ID2', 'Flag2', 'ID3', 'Flag3', 'ID4', 'Flag4'])

    def test_calc_cols_with_exclude_types_large(self):
        # Test case where exclude_types is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(exclude_types=[int, bool]), ['Name', 'Name2', 'Name3', 'Name4'])
       
    def test_calc_cols_with_exclude_types_large_exclude_nonlist(self):
        # Test case where exclude_types is provided with more than 10 columns
        pydf = Pydf(lol=[[1, 'a', True, 1, 'a', True, 1, 'a', True, 1, 'a', True], 
                         [2, 'b', False, 2, 'b', False, 2, 'b', False, 2, 'b', False], 
                         [3, 'c', True, 3, 'c', True, 3, 'c', True, 3, 'c', True]], 
                         cols=['ID', 'Name', 'Flag', 'ID2', 'Name2', 'Flag2', 'ID3', 'Name3', 'Flag3', 'ID4', 'Name4', 'Flag4'], 
                         dtypes={'ID': int, 'Name': str, 'Flag': bool, 
                                 'ID2': int, 'Name2': str, 'Flag2': bool, 
                                 'ID3': int, 'Name3': str, 'Flag3': bool, 
                                 'ID4': int, 'Name4': str, 'Flag4': bool})
        self.assertEqual(pydf.calc_cols(exclude_types=int), ['Name', 'Flag', 'Name2', 'Flag2', 'Name3', 'Flag3', 'Name4', 'Flag4'])

    # from/to cases
    def test_from_lod(self):
        records_lod = [ {'col1': 1, 'col2': 2}, 
                        {'col1': 11, 'col2': 12}, 
                        {'col1': 21, 'col2': 22}]
                        
        keyfield = 'col1'
        dtypes = {'col1': int, 'col2': int}
        pydf = Pydf.from_lod(records_lod, keyfield=keyfield, dtypes=dtypes)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, keyfield)
        self.assertEqual(pydf.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(pydf.lol, [[1, 2], [11, 12], [21, 22]])
        self.assertEqual(pydf.kd, {1: 0, 11: 1, 21: 2})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)

    def test_from_lod_no_records_but_dtypes(self):
        records_lod = []
                        
        keyfield = 'col1'
        dtypes = {'col1': int, 'col2': int}
        pydf = Pydf.from_lod(records_lod, keyfield=keyfield, dtypes=dtypes)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, keyfield)
        self.assertEqual(pydf.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(pydf.lol, [])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)

    def test_from_lod_no_records_no_dtypes_but_keyfield(self):
        records_lod = []
                        
        keyfield = 'col1'
        dtypes = {}
        pydf = Pydf.from_lod(records_lod, keyfield=keyfield, dtypes=dtypes)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, keyfield)
        self.assertEqual(pydf.hd, {})
        self.assertEqual(pydf.lol, [])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)


    def test_from_lod_no_records_no_dtypes_no_keyfield(self):
        records_lod = []
                        
        keyfield = ''
        dtypes = {}
        pydf = Pydf.from_lod(records_lod, keyfield=keyfield, dtypes=dtypes)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.hd, {})
        self.assertEqual(pydf.lol, [])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)


    def test_from_hllola(self):
        header_list = ['col1', 'col2']
        data_list = [[1, 'a'], [2, 'b'], [3, 'c']]
        hllola = (header_list, data_list)
        keyfield = 'col1'
        dtypes = {'col1': int, 'col2': str}

        pydf = Pydf.from_hllola(hllola, keyfield=keyfield, dtypes=dtypes)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, keyfield)
        self.assertEqual(pydf.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c']])
        self.assertEqual(pydf.kd, {1: 0, 2: 1, 3: 2})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)

    def test_to_hllola(self):
        cols    = ['col1', 'col2']
        lol     = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf    = Pydf(cols=cols, lol=lol)

        expected_hllola = (['col1', 'col2'], [[1, 'a'], [2, 'b'], [3, 'c']])
        actual_hllola = pydf.to_hllola()

        self.assertEqual(actual_hllola, expected_hllola)


    # from_dod
    def test_from_dod_with_keyfield(self):
        # Test case where dod is provided with keyfield specified
        dod = {
            'row_0': {'rowkey': 'row_0', 'data1': 1, 'data2': 2},
            'row_1': {'rowkey': 'row_1', 'data1': 11, 'data2': 22},
        }
        pydf = Pydf.from_dod(dod, keyfield='rowkey')
        self.assertEqual(pydf.columns(), ['rowkey', 'data1', 'data2'])
        self.assertEqual(pydf.lol, [['row_0', 1, 2], ['row_1', 11, 22]])
        self.assertEqual(pydf.keyfield, 'rowkey')

    def test_from_dod_without_keyfield(self):
        # Test case where dod is provided without keyfield in rows
        dod = {
            'row_0': {'data1': 1, 'data2': 2},
            'row_1': {'data1': 11, 'data2': 22},
        }
        pydf = Pydf.from_dod(dod, keyfield='rowkey')
        self.assertEqual(pydf.columns(), ['rowkey', 'data1', 'data2'])
        self.assertEqual(pydf.lol, [['row_0', 1, 2], ['row_1', 11, 22]])

    def test_from_dod_with_dtypes(self):
        # Test case where dod is provided with dtypes specified
        dod = {
            'row_0': {'rowkey': 'row_0', 'data1': 1, 'data2': 2},
            'row_1': {'rowkey': 'row_1', 'data1': 11, 'data2': 22},
        }
        dtypes = {'data1': int, 'data2': float}
        pydf = Pydf.from_dod(dod, keyfield='rowkey', dtypes=dtypes)
        self.assertEqual(pydf.columns(), ['rowkey', 'data1', 'data2'])
        self.assertEqual(pydf.lol, [['row_0', 1, 2.0], ['row_1', 11, 22.0]])

    def test_from_dod_with_empty_dod(self):
        # Test case where an empty dod is provided
        dod = {}
        pydf = Pydf.from_dod(dod)
        self.assertEqual(pydf.columns(), [])
        self.assertEqual(pydf.lol, [])

    # to_dod
    def test_to_dod_with_remove_keyfield_true(self):
        # Test case where keyfield column is removed (default behavior)
        pydf = Pydf(lol=[['1', 'a', True], 
                         ['2', 'b', False]], cols=['ID', 'Name', 'Flag'], keyfield='ID')
        expected_dod = {'1': {'Name': 'a', 'Flag': True}, '2': {'Name': 'b', 'Flag': False}}
        dod = pydf.to_dod()
        self.assertEqual(dod, expected_dod)

    def test_to_dod_with_remove_keyfield_false(self):
        # Test case where keyfield column is retained
        pydf = Pydf(lol=[['1', 'a', True], ['2', 'b', False]], cols=['ID', 'Name', 'Flag'], keyfield='ID')
        expected_dod = {'1': {'ID': '1', 'Name': 'a', 'Flag': True}, '2': {'ID': '2', 'Name': 'b', 'Flag': False}}
        dod = pydf.to_dod(remove_keyfield=False)
        self.assertEqual(dod, expected_dod)

    def test_to_dod_with_empty_pydf(self):
        # Test case where Pydf is empty
        pydf = Pydf()
        expected_dod = {}
        dod = pydf.to_dod()
        self.assertEqual(dod, expected_dod)

    # to_cols_dol()
    def test_to_cols_dol_with_data(self):
        # Test case where Pydf contains data
        pydf = Pydf(lol=[[1, 'a', True], [2, 'b', False]], cols=['ID', 'Name', 'Flag'])
        expected_dol = {'ID': [1, 2], 'Name': ['a', 'b'], 'Flag': [True, False]}
        dol = pydf.to_cols_dol()
        self.assertEqual(dol, expected_dol)

    def test_to_cols_dol_with_empty_pydf(self):
        # Test case where Pydf is empty
        pydf = Pydf()
        expected_dol = {}
        dol = pydf.to_cols_dol()
        self.assertEqual(dol, expected_dol)


    # from_excel_buff
    def test_from_excel_buff(self):
        # Load the test data from file
        subdir = "test_data"
        
        current_dir = Path(__file__).resolve().parent
        self.test_data_dir = current_dir / subdir

        excel_file_path = self.test_data_dir / "excel_test_1.xlsx"
        with excel_file_path.open("rb") as f:
            excel_data = f.read()

        # Test reading Excel data into Pydf
        my_pydf = Pydf.from_excel_buff(excel_data)
        
        # Assert Pydf properties
        self.assertEqual(my_pydf.len(), 3)
        self.assertEqual(my_pydf.num_cols(), 3)
        self.assertEqual(my_pydf.columns(), ['ID', 'Name', 'Age'])
        self.assertEqual(my_pydf.lol, [['1', 'John', '30'], ['2', 'Alice', '25'], ['3', 'Bob', '35']])


    def test_to_csv_file(self):
        # Determine the path to the test data directory
        current_dir = Path(__file__).resolve().parent
        self.test_data_dir = current_dir / "test_data"

        # Create a sample Pydf object
        pydf = Pydf(
            lol=[
                ['ID', 'Name', 'Age'],
                [1, 'John', 30],
                [2, 'Alice', 25],
                [3, 'Bob', 35]
            ],
            keyfield='ID'
        )

        # Define the output CSV file path
        csv_file_path = self.test_data_dir / "test_output.csv"

        # Write Pydf content to CSV file
        output_file_path = pydf.to_csv_file(file_path=str(csv_file_path))

        # Assert that the output file path matches the expected path
        self.assertEqual(output_file_path, str(csv_file_path))

        # Assert that the CSV file has been created
        self.assertTrue(csv_file_path.exists())

        # Optionally, you can also assert the content of the CSV file
        # Here, you can read the content of the CSV file and compare it with the expected content

        # Clean up: Delete the CSV file after the test
        # os.remove(csv_file_path)
        
        
    # from_pandas_df
    def test_from_pandas_df_with_dataframe(self):
        # Mock a Pandas DataFrame with various data types
        df_mock = pd.DataFrame({
            'ID': [1, 2, 3],
            'Name': ['John', 'Alice', 'Bob'],
            'Age': [30, 25, 35],
            'IsAdult': [True, False, True],
            'Grade': [3.5, 4.2, 2.8]
        })

        # Call the method under test
        pydf = Pydf.from_pandas_df(df_mock)

        # Assert that the Pydf object is created with the correct properties
        self.assertEqual(pydf.len(), 3)
        self.assertEqual(pydf.num_cols(), 5)  # Number of columns including all data types
        self.assertEqual(pydf.columns(), ['ID', 'Name', 'Age', 'IsAdult', 'Grade'])
        self.assertEqual(pydf.lol, [
            [1, 'John', 30, True, 3.5],
            [2, 'Alice', 25, False, 4.2],
            [3, 'Bob', 35, True, 2.8]
        ])
        
    def test_from_pandas_df_with_series(self):
        # Mock a Pandas Series
        series_mock = pd.DataFrame([
            {'ID': 1, 'Name': 'John', 'Age': 30},
            {'ID': 2, 'Name': 'Alice', 'Age': 25},
            {'ID': 3, 'Name': 'Bob', 'Age': 35}
        ]).iloc[0]

        # Call the method under test
        pydf = Pydf.from_pandas_df(series_mock)

        # Assert that the Pydf object is created with the correct properties
        self.assertEqual(pydf.len(), 1)
        self.assertEqual(pydf.num_cols(), 3)
        self.assertEqual(pydf.columns(), ['ID', 'Name', 'Age'])
        self.assertEqual(pydf.lol, [[1, 'John', 30]])
        

    def test_from_pandas_df_with_dataframe_using_csv(self):
        # Mock a Pandas DataFrame
        df_mock = pd.DataFrame([
            {'ID': 1, 'Name': 'John', 'Age': 30},
            {'ID': 2, 'Name': 'Alice', 'Age': 25},
            {'ID': 3, 'Name': 'Bob', 'Age': 35}
        ])

        # Call the method under test
        pydf = Pydf.from_pandas_df(df_mock, use_csv=True)

        # Assert that the Pydf object is created with the correct properties
        self.assertEqual(pydf.len(), 3)
        self.assertEqual(pydf.num_cols(), 3)
        self.assertEqual(pydf.columns(), ['ID', 'Name', 'Age'])
        self.assertEqual(pydf.lol, [[1, 'John', 30], [2, 'Alice', 25], [3, 'Bob', 35]])

    def test_from_pandas_df_with_series_using_csv(self):
        # Mock a Pandas Series
        series_mock = pd.DataFrame([
            {'ID': 1, 'Name': 'John',  'Age': 30},
            {'ID': 2, 'Name': 'Alice', 'Age': 25},
            {'ID': 3, 'Name': 'Bob',   'Age': 35}
        ]).iloc[0]

        # Call the method under test
        pydf = Pydf.from_pandas_df(series_mock, use_csv=True)

        # Assert that the Pydf object is created with the correct properties
        self.assertEqual(pydf.len(), 1)
        self.assertEqual(pydf.num_cols(), 3)
        self.assertEqual(pydf.columns(), ['ID', 'Name', 'Age'])
        self.assertEqual(pydf.lol, [[1, 'John', 30]])
        
        
    # test_pydf_to_pandas
    def test_pydf_to_pandas(self):
        # Create a Pydf object with sample data
        pydf = Pydf(
            lol=[
                [1, 'John', 30, True, 3.5],
                [2, 'Alice', 25, False, 4.2],
                [3, 'Bob', 35, True, 2.8]
            ],
            cols=['ID', 'Name', 'Age', 'IsAdult', 'Grade']
        )

        # Convert Pydf to Pandas DataFrame
        df = pydf.to_pandas_df()

        # Expected DataFrame
        expected_df = pd.DataFrame({
            'ID': [1, 2, 3],
            'Name': ['John', 'Alice', 'Bob'],
            'Age': [30, 25, 35],
            'IsAdult': [True, False, True],
            'Grade': [3.5, 4.2, 2.8]
        })

        # Assert that the generated DataFrame is equal to the expected DataFrame
        pd.testing.assert_frame_equal(df, expected_df)

    def test_pydf_to_pandas_using_csv(self):
        # Create a Pydf object with sample data
        pydf = Pydf(
            lol=[
                [1, 'John', 30, True, 3.5],
                [2, 'Alice', 25, False, 4.2],
                [3, 'Bob', 35, True, 2.8]
            ],
            cols=['ID', 'Name', 'Age', 'IsAdult', 'Grade']
        )

        # Convert Pydf to Pandas DataFrame
        df = pydf.to_pandas_df(use_csv=True)

        # Expected DataFrame
        expected_df = pd.DataFrame({
            'ID': [1, 2, 3],
            'Name': ['John', 'Alice', 'Bob'],
            'Age': [30, 25, 35],
            'IsAdult': [True, False, True],
            'Grade': [3.5, 4.2, 2.8]
        })

        # Assert that the generated DataFrame is equal to the expected DataFrame
        pd.testing.assert_frame_equal(df, expected_df)

    # from numpy
    def test_from_numpy_all_integers(self):
        # Create a numpy array of all integers
        npa_int = np.array([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])

        # Call the method under test
        pydf_int = Pydf.from_numpy(npa_int)

        # Assert that the Pydf object is created with the correct properties
        self.assertEqual(pydf_int.len(), 3)
        self.assertEqual(pydf_int.num_cols(), 3)
        self.assertEqual(pydf_int.columns(), [])
        self.assertEqual(pydf_int.lol, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_from_numpy_all_floats(self):
        # Create a numpy array of all floats
        npa_float = np.array([[1.0, 2.5, 3.7],
                               [4.2, 5.6, 6.9],
                               [7.3, 8.1, 9.4]])

        # Call the method under test
        pydf_float = Pydf.from_numpy(npa_float)

        # Assert that the Pydf object is created with the correct properties
        self.assertEqual(pydf_float.len(), 3)
        self.assertEqual(pydf_float.num_cols(), 3)
        self.assertEqual(pydf_float.columns(), [])
        self.assertEqual(pydf_float.lol, [[1.0, 2.5, 3.7], [4.2, 5.6, 6.9], [7.3, 8.1, 9.4]])

    
    def test_from_numpy_with_2d_array(self):
        # Create a 2D numpy array
        npa = np.array([[1, 'John', 30], [2, 'Alice', 25], [3, 'Bob', 35]])

        # Call the from_numpy method
        pydf = Pydf.from_numpy(npa)

        # Check if the Pydf object is created with the correct properties
        
        # Numpy arrays are homogeneous, meaning all elements in a numpy array 
        # must have the same data type. If you attempt to create a numpy array 
        # with elements of different data types, numpy will automatically cast 
        # them to a single data type that can accommodate all elements. This can 
        # lead to loss of information if the original data types are different.

        # For example, if you try to create a numpy array with both integers and 
        # strings, numpy will cast all elements to a common data type, such as Unicode strings.
        
        self.assertEqual(pydf.len(), 3)
        self.assertEqual(pydf.num_cols(), 3)
        self.assertEqual(pydf.columns(), [])
        self.assertEqual(pydf.lol, [['1', 'John', '30'], ['2', 'Alice', '25'], ['3', 'Bob', '35']])

    def test_from_numpy_with_1d_array(self):
        # Create a 1D numpy array
        npa = np.array(['John', 'Alice', 'Bob'])

        # Call the from_numpy method
        pydf = Pydf.from_numpy(npa)
        
        # Check if the Pydf object is created with the correct properties
        self.assertEqual(pydf.len(), 1)
        self.assertEqual(pydf.num_cols(), 3)
        self.assertEqual(pydf.columns(), [])
        self.assertEqual(pydf.lol, [['John', 'Alice', 'Bob']])

    def test_from_numpy_with_keyfield_and_cols(self):
        # Create a 2D numpy array
        npa = np.array([[1, 'John', 30], [2, 'Alice', 25], [3, 'Bob', 35]])

        # Specify keyfield and columns
        keyfield = 'ID'
        cols = ['ID', 'Name', 'Age']

        # Call the from_numpy method
        pydf = Pydf.from_numpy(npa, keyfield=keyfield, cols=cols)

        # Check if the Pydf object is created with the correct properties
        self.assertEqual(pydf.keyfield, keyfield)
        self.assertEqual(pydf.columns(), cols)

    # to_numpy
    def test_to_numpy_all_integers(self):
        # Create a Pydf object with all integers
        pydf_int = Pydf(cols=['A', 'B', 'C'],
                        lol=[[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])

        # Call the method under test
        npa_int = pydf_int.to_numpy()

        # Assert that the numpy array is created with the correct values
        expected_npa_int = np.array([[1, 2, 3],
                                     [4, 5, 6],
                                     [7, 8, 9]])
        self.assertTrue(np.array_equal(npa_int, expected_npa_int))

    def test_to_numpy_all_floats(self):
        # Create a Pydf object with all floats
        pydf_float = Pydf(cols=['X', 'Y', 'Z'],
                          lol=[[1.0, 2.5, 3.7],
                               [4.2, 5.6, 6.9],
                               [7.3, 8.1, 9.4]])

        # Call the method under test
        npa_float = pydf_float.to_numpy()

        # Assert that the numpy array is created with the correct values
        expected_npa_float = np.array([[1.0, 2.5, 3.7],
                                       [4.2, 5.6, 6.9],
                                       [7.3, 8.1, 9.4]])
        self.assertTrue(np.array_equal(npa_float, expected_npa_float))



    # append
    def test_append_without_record(self):
        pydf = Pydf()

        pydf.append({})

        self.assertEqual(pydf, Pydf())

    def test_append_without_keyfield(self):
        pydf = Pydf()
        record_da = {'col1': 1, 'col2': 'b'}

        pydf.append(record_da)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(pydf.lol, [[1, 'b']])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, {})
        self.assertEqual(pydf._iter_index, 0)

    def test_append_list_without_keyfield_but_cols(self):
        pydf = Pydf(cols=['col1', 'col2'])
        record_la = [1, 'b']

        pydf.append(record_la)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(pydf.lol, [[1, 'b']])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, {})
        self.assertEqual(pydf._iter_index, 0)

    def test_append_list_without_keyfield_no_cols(self):
        pydf = Pydf()
        record_la = [1, 'b']

        pydf.append(record_la)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.hd, {})
        self.assertEqual(pydf.lol, [[1, 'b']])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, {})
        self.assertEqual(pydf._iter_index, 0)

    def test_append_with_keyfield(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b']]
        #kd = {1: 0, 2: 1}
        dtypes = {'col1': int, 'col2': str}
        pydf = Pydf(cols=cols, lol=lol, dtypes=dtypes, keyfield='col1')

        record_da = {'col1': 3, 'col2': 'c'}

        pydf.append(record_da)

        self.assertEqual(pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c']])

        # append record with same keyfield will modify in place
        record_da = {'col1': 3, 'col2': 'd'}

        pydf.append(record_da)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, 'col1')
        self.assertEqual(pydf.columns(), cols)
        self.assertEqual(pydf.lol, [[1, 'a'], [2, 'b'], [3, 'd']])
        self.assertEqual(pydf.kd, {1: 0, 2: 1, 3: 2})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)


    def test_extend_without_keyfield(self):
        pydf = Pydf()
        records_lod = [{'col1': 1, 'col2': 'b'}, {'col1': 2, 'col2': 'c'}]

        pydf.extend(records_lod)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(pydf.lol, [[1, 'b'], [2, 'c']])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, {})
        self.assertEqual(pydf._iter_index, 0)

    def test_extend_using_append_without_keyfield(self):
        pydf = Pydf()
        cols = ['col1', 'col2']
        records_lod = [{'col1': 1, 'col2': 'b'}, {'col1': 2, 'col2': 'c'}]

        pydf.append(records_lod)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, '')
        self.assertEqual(pydf.columns(), cols)
        self.assertEqual(pydf.lol, [[1, 'b'], [2, 'c']])
        self.assertEqual(pydf.kd, {})
        self.assertEqual(pydf.dtypes, {})
        self.assertEqual(pydf._iter_index, 0)

    def test_extend_with_keyfield(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b']]
        dtypes = {'col1': int, 'col2': str}
        pydf = Pydf(cols=cols, lol=lol, dtypes=dtypes, keyfield='col1')

        records_lod = [{'col1': 3, 'col2': 'c'}, {'col1': 4, 'col2': 'd'}]

        pydf.extend(records_lod)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, 'col1')
        self.assertEqual(pydf.columns(), cols)
        self.assertEqual(pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])
        self.assertEqual(pydf.kd, {1: 0, 2: 1, 3: 2, 4: 3})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)
        

    def test_extend_using_append_with_keyfield(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 'a'], [2, 'b']]
        dtypes = {'col1': int, 'col2': str}
        pydf = Pydf(cols=cols, lol=lol, dtypes=dtypes, keyfield='col1')

        records_lod = [{'col1': 3, 'col2': 'c'}, {'col1': 4, 'col2': 'd'}]

        pydf.append(records_lod)

        self.assertEqual(pydf.name, '')
        self.assertEqual(pydf.keyfield, 'col1')
        self.assertEqual(pydf.hd, hd)
        self.assertEqual(pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])
        self.assertEqual(pydf.kd, {1: 0, 2: 1, 3: 2, 4: 3})
        self.assertEqual(pydf.dtypes, dtypes)
        self.assertEqual(pydf._iter_index, 0)
        

    def test_concat_without_keyfield(self):
        pydf1 = Pydf()
        pydf2 = Pydf()

        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol1 = [[1, 'a'], [2, 'b']]
        lol2 = [['x', 'y'], ['z', 'w']]
        pydf1 = Pydf(cols=cols, lol=lol1, keyfield='', dtypes={'col1': str, 'col2': str})
        pydf2 = Pydf(cols=cols, lol=lol2, keyfield='', dtypes={'col1': str, 'col2': str})

        pydf1.concat(pydf2)

        self.assertEqual(pydf1.name, '')
        self.assertEqual(pydf1.keyfield, '')
        self.assertEqual(pydf1.hd, hd)
        self.assertEqual(pydf1.lol, [['1', 'a'], ['2', 'b'], ['x', 'y'], ['z', 'w']])
        self.assertEqual(pydf1.kd, {})
        self.assertEqual(pydf1.dtypes, {'col1': str, 'col2': str})
        self.assertEqual(pydf1._iter_index, 0)

    def test_concat_without_keyfield_self_empty(self):
        pydf1 = Pydf()
        pydf2 = Pydf()

        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol1 = []
        lol2 = [['x', 'y'], ['z', 'w']]
        pydf1 = Pydf(           lol=lol1, keyfield='')
        pydf2 = Pydf(cols=cols, lol=lol2, keyfield='')

        pydf1.concat(pydf2)

        self.assertEqual(pydf1.name, '')
        self.assertEqual(pydf1.keyfield, '')
        self.assertEqual(pydf1.hd, hd)
        self.assertEqual(pydf1.lol, [['x', 'y'], ['z', 'w']])
        self.assertEqual(pydf1.kd, {})
        self.assertEqual(pydf1.dtypes, {})
        self.assertEqual(pydf1._iter_index, 0)

    def test_concat_using_append_without_keyfield(self):
        pydf1 = Pydf()
        pydf2 = Pydf()

        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol1 = [[1, 'a'], [2, 'b']]
        lol2 = [['x', 'y'], ['z', 'w']]
        pydf1 = Pydf(cols=cols, lol=lol1, keyfield='', dtypes={'col1': str, 'col2': str})
        pydf2 = Pydf(cols=cols, lol=lol2, keyfield='', dtypes={'col1': str, 'col2': str})

        pydf1.append(pydf2)

        self.assertEqual(pydf1.name, '')
        self.assertEqual(pydf1.keyfield, '')
        self.assertEqual(pydf1.hd, hd)
        self.assertEqual(pydf1.lol, [['1', 'a'], ['2', 'b'], ['x', 'y'], ['z', 'w']])
        self.assertEqual(pydf1.kd, {})
        self.assertEqual(pydf1.dtypes, {'col1': str, 'col2': str})
        self.assertEqual(pydf1._iter_index, 0)

    def test_concat_with_keyfield(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol1 = [[1, 'a'], [2, 'b']]
        lol2 = [[3, 'c'], [4, 'd']]
        pydf1 = Pydf(cols=cols, lol=lol1, keyfield='col1', dtypes={'col1': int, 'col2': str})
        pydf2 = Pydf(cols=cols, lol=lol2, keyfield='col1', dtypes={'col1': int, 'col2': str})

        pydf1.concat(pydf2)

        self.assertEqual(pydf1.name, '')
        self.assertEqual(pydf1.keyfield, 'col1')
        self.assertEqual(pydf1.hd, hd)
        self.assertEqual(pydf1.lol, [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])
        self.assertEqual(pydf1.kd, {1: 0, 2: 1, 3: 2, 4: 3})
        self.assertEqual(pydf1.dtypes, {'col1': int, 'col2': str})
        self.assertEqual(pydf1._iter_index, 0)

    def test_concat_using_append_with_keyfield(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol1 = [[1, 'a'], [2, 'b']]
        lol2 = [[3, 'c'], [4, 'd']]
        pydf1 = Pydf(cols=cols, lol=lol1, keyfield='col1', dtypes={'col1': int, 'col2': str})
        pydf2 = Pydf(cols=cols, lol=lol2, keyfield='col1', dtypes={'col1': int, 'col2': str})

        pydf1.append(pydf2)

        self.assertEqual(pydf1.name, '')
        self.assertEqual(pydf1.keyfield, 'col1')
        self.assertEqual(pydf1.hd, hd)
        self.assertEqual(pydf1.lol, [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])
        self.assertEqual(pydf1.kd, {1: 0, 2: 1, 3: 2, 4: 3})
        self.assertEqual(pydf1.dtypes, {'col1': int, 'col2': str})
        self.assertEqual(pydf1._iter_index, 0)
        

    # remove_key
    def test_remove_key_existing_key(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keyval = 2
        new_pydf = pydf.remove_key(keyval)

        self.assertEqual(new_pydf.name, '')
        self.assertEqual(new_pydf.keyfield, 'col1')
        self.assertEqual(new_pydf.hd, hd)
        self.assertEqual(new_pydf.lol, [[1, 'a'], [3, 'c']])
        self.assertEqual(new_pydf.kd, {1: 0, 3: 1})
        self.assertEqual(new_pydf.dtypes, {'col1': int, 'col2': str})
        self.assertEqual(new_pydf._iter_index, 0)

    def test_remove_key_keyfield_notdefined(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='', dtypes={'col1': int, 'col2': str})

        keyval = 4
        new_pydf = pydf.remove_key(keyval, silent_error=True)

        self.assertEqual(new_pydf.name, '')
        self.assertEqual(new_pydf.keyfield, '')
        self.assertEqual(new_pydf.hd, hd)
        self.assertEqual(new_pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c']])
        self.assertEqual(new_pydf.kd, {})
        self.assertEqual(new_pydf.dtypes, {'col1': int, 'col2': str})
        self.assertEqual(new_pydf._iter_index, 0)

    def test_remove_key_nonexistent_key_silent_error(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keyval = 4
        new_pydf = pydf.remove_key(keyval, silent_error=True)

        self.assertEqual(new_pydf.name, '')
        self.assertEqual(new_pydf.keyfield, 'col1')
        self.assertEqual(new_pydf.hd, hd)
        self.assertEqual(new_pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c']])
        self.assertEqual(new_pydf.kd, {1: 0, 2: 1, 3: 2})
        self.assertEqual(new_pydf.dtypes, {'col1': int, 'col2': str})
        self.assertEqual(new_pydf._iter_index, 0)

    def test_remove_key_nonexistent_key_raise_error(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keyval = 4
        with self.assertRaises(KeyError):
            pydf.remove_key(keyval, silent_error=False)


    # remove_keylist
    def test_remove_keylist_existing_keys(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [ [1, 'a'], 
                [2, 'b'], 
                [3, 'c'], 
                [4, 'd']]
                
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keylist = [2, 4]
        
        new_pydf = pydf.remove_keylist(keylist)

        self.assertEqual(new_pydf.name, '')
        self.assertEqual(new_pydf.keyfield, 'col1')
        self.assertEqual(new_pydf.hd, hd)
        self.assertEqual(new_pydf.lol, [[1, 'a'], [3, 'c']])
        self.assertEqual(new_pydf.kd, {1: 0, 3: 1})
        self.assertEqual(new_pydf.dtypes, {'col1': int, 'col2': str})

    def test_remove_keylist_nonexistent_keys_silent_error(self):
        cols = ['col1', 'col2']
        hd = {'col1': 0, 'col2': 1}
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keylist = [4, 5, 6]
        new_pydf = pydf.remove_keylist(keylist, silent_error=True)

        self.assertEqual(new_pydf.name, '')
        self.assertEqual(new_pydf.keyfield, 'col1')
        self.assertEqual(new_pydf.hd, hd)
        self.assertEqual(new_pydf.lol, [[1, 'a'], [2, 'b'], [3, 'c']])
        self.assertEqual(new_pydf.kd, {1: 0, 2: 1, 3: 2})
        self.assertEqual(new_pydf.dtypes, {'col1': int, 'col2': str})
        self.assertEqual(new_pydf._iter_index, 0)

    def test_remove_keylist_nonexistent_keys_raise_error(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keylist = [4, 5, 6]

        with self.assertRaises(KeyError):
            pydf.remove_keylist(keylist, silent_error=False)

    # select_record_da
    def test_select_record_da_existing_key(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        key = 2
        record_da = pydf.select_record_da(key)

        self.assertEqual(record_da, {'col1': 2, 'col2': 'b'})

    def test_select_record_da_nonexistent_key(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        key = 4
        record_da = pydf.select_record_da(key)

        self.assertEqual(record_da, {})

    def test_select_record_da_no_keyfield(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='', dtypes={'col1': int, 'col2': str})

        key = 'col1'

        with self.assertRaises(RuntimeError):
            pydf.select_record_da(key)

    # iloc / irow
    def test_iloc_existing_row_idx(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        row_idx = 1
        record_da = pydf.iloc(row_idx)

        self.assertEqual(record_da, {'col1': 2, 'col2': 'b'})

    def test_iloc_nonexistent_row_idx(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        row_idx = 4
        record_da = pydf.iloc(row_idx)

        self.assertEqual(record_da, {})

    def test_iloc_negative_row_idx(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        row_idx = -1
        record_da = pydf.irow(row_idx)

        self.assertEqual(record_da, {})

    def test_irow_existing_row_idx(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        row_idx = 1
        record_da = pydf.irow(row_idx)

        self.assertEqual(record_da, {'col1': 2, 'col2': 'b'})

    def test_irow_nonexistent_row_idx(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        row_idx = 4
        record_da = pydf.iloc(row_idx)

        self.assertEqual(record_da, {})

    def test_irow_negative_row_idx(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        row_idx = -1
        record_da = pydf.irow(row_idx)

        self.assertEqual(record_da, {})

    # select_by_dict_to_lod
    def test_select_by_dict_to_lod_existing_selector_da(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        selector_da = {'col2': 'b'}
        result_lod = pydf.select_by_dict_to_lod(selector_da)

        expected_lod = [{'col1': 2, 'col2': 'b'}, {'col1': 4, 'col2': 'b'}]
        self.assertEqual(result_lod, expected_lod)

    def test_select_by_dict_to_lod_nonexistent_selector_da(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        selector_da = {'col2': 'd'}
        result_lod = pydf.select_by_dict_to_lod(selector_da)

        self.assertEqual(result_lod, [])

    def test_select_by_dict_to_lod_with_expectmax(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        selector_da = {'col2': 'b'}
        expectmax = 1
        with self.assertRaises(LookupError):  # You should replace this with the actual exception that should be raised
            pydf.select_by_dict_to_lod(selector_da, expectmax=expectmax)

    # select_by_dict
    def test_select_by_dict_existing_selector_da(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        selector_da = {'col2': 'b'}
        result_pydf = pydf.select_by_dict(selector_da)

        expected_hd = {'col1': 0, 'col2': 1}
        expected_lol = [[2, 'b'], [4, 'b']]
        expected_kd = {2: 0, 4: 1}
        expected_dtypes = {'col1': int, 'col2': str}

        self.assertEqual(result_pydf.name, '')
        self.assertEqual(result_pydf.keyfield, 'col1')
        self.assertEqual(result_pydf.hd, expected_hd)
        self.assertEqual(result_pydf.lol, expected_lol)
        self.assertEqual(result_pydf.kd, expected_kd)
        self.assertEqual(result_pydf.dtypes, expected_dtypes)
        self.assertEqual(result_pydf._iter_index, 0)

    def test_select_by_dict_nonexistent_selector_da(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        selector_da = {'col2': 'd'}
        result_pydf = pydf.select_by_dict(selector_da)

        expected_hd = {'col1': 0, 'col2': 1}
        expected_lol = []
        expected_kd = {}
        expected_dtypes = {'col1': int, 'col2': str}

        self.assertEqual(result_pydf.name, '')
        self.assertEqual(result_pydf.keyfield, 'col1')
        self.assertEqual(result_pydf.hd, expected_hd)
        self.assertEqual(result_pydf.lol, expected_lol)
        self.assertEqual(result_pydf.kd, expected_kd)
        self.assertEqual(result_pydf.dtypes, expected_dtypes)
        self.assertEqual(result_pydf._iter_index, 0)

    def test_select_by_dict_with_expectmax(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        selector_da = {'col2': 'b'}
        expectmax = 1
        with self.assertRaises(LookupError):  # You should replace this with the actual exception that should be raised
            pydf.select_by_dict(selector_da, expectmax=expectmax)

    # select_first_row_by_dict
    def test_select_first_row_by_dict_matching(self):
        # Test case where the first row matching the selector dictionary is found
        pydf = Pydf(lol=[[1, 'John'], [2, 'Jane'], [3, 'Doe']], cols=['ID', 'Name'])
        selected_row = pydf.select_first_row_by_dict({'ID': 2})
        self.assertEqual(selected_row, {'ID':2, 'Name':'Jane'})

    def test_select_first_row_by_dict_no_match(self):
        # Test case where no row matches the selector dictionary
        pydf = Pydf(lol=[[1, 'John'], [2, 'Jane'], [3, 'Doe']], cols=['ID', 'Name'])
        selected_row = pydf.select_first_row_by_dict({'ID': 4})
        self.assertEqual(selected_row, {})

    def test_select_first_row_by_dict_inverse_matching(self):
        # Test case where the first row not matching the selector dictionary is found
        pydf = Pydf(lol=[[1, 'John'], [2, 'Jane'], [3, 'Doe']], cols=['ID', 'Name'])
        selected_row = pydf.select_first_row_by_dict({'ID': 2}, inverse=True)
        self.assertEqual(selected_row, {'ID':1, 'Name':'John'})

    def test_select_first_row_by_dict_empty_pydf(self):
        # Test case where Pydf is empty
        pydf = Pydf(lol=[], cols=['ID', 'Name'])
        selected_row = pydf.select_first_row_by_dict({'ID': 2})
        self.assertEqual(selected_row, {})


    # col / col_to_la
    def test_col_existing_colname(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        colname = 'col2'
        result_la = pydf.col(colname)

        expected_la = ['a', 'b', 'c']
        self.assertEqual(result_la, expected_la)

    def test_col_nonexistent_colname(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        colname = 'col3'
        with self.assertRaises(RuntimeError):
            result_la = pydf.col(colname)
            result_la = result_la # fool linter

        #self.assertEqual(result_la, [])

    def test_col_empty_colname(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        colname = ''
        with self.assertRaises(RuntimeError):
            result_la = pydf.col(colname)
            result_la = result_la # fool linter

        #self.assertEqual(result_la, [])

    def test_col_nonexistent_colname_silent(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        colname = 'col3'
        result_la = pydf.col(colname, silent_error=True)

        self.assertEqual(result_la, [])

    # drop_cols
    def test_drop_cols_existing_cols(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        cols_to_drop = ['col2', 'col3']
        pydf.drop_cols(cols_to_drop)

        expected_hd = {'col1': 0}
        expected_lol = [[1], [2], [3]]

        self.assertEqual(pydf.hd, expected_hd)
        self.assertEqual(pydf.lol, expected_lol)

    def test_drop_cols_nonexistent_cols(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        cols_to_drop = ['col4', 'col5']
        pydf.drop_cols(cols_to_drop)

        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2}
        expected_lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]

        self.assertEqual(pydf.hd, expected_hd)
        self.assertEqual(pydf.lol, expected_lol)

    def test_drop_cols_empty_cols(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        cols_to_drop = []
        pydf.drop_cols(cols_to_drop)

        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2}
        expected_lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]

        self.assertEqual(pydf.hd, expected_hd)
        self.assertEqual(pydf.lol, expected_lol)

    # assign_col
    def test_assign_col_existing_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        colname = 'col2'
        new_values = ['A', 'B', 'C']
        pydf.assign_col(colname, new_values)

        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2}
        expected_lol = [[1, 'A', 'x'], [2, 'B', 'y'], [3, 'C', 'z']]

        self.assertEqual(pydf.hd, expected_hd)
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_col_nonexistent_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        colname = 'col4'
        new_values = ['A', 'B', 'C']
        pydf.assign_col(colname, new_values)

        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2}
        expected_lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]

        self.assertEqual(pydf.hd, expected_hd)
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_col_empty_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        colname = ''
        new_values = ['A', 'B', 'C']
        pydf.assign_col(colname, new_values)

        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2}
        expected_lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]

        self.assertEqual(pydf.hd, expected_hd)
        self.assertEqual(pydf.lol, expected_lol)

    # cols_to_dol
    def test_cols_to_dol_valid_cols(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'b', 'c'], ['b', 'd', 'e'], ['a', 'f', 'g'], ['b', 'd', 'm']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        colname1 = 'col1'
        colname2 = 'col2'
        result_dola = pydf.cols_to_dol(colname1, colname2)

        expected_dola = {'a': ['b', 'f'], 'b': ['d']}
        self.assertEqual(result_dola, expected_dola)

    def test_cols_to_dol_invalid_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'b', 'c'], ['b', 'd', 'e'], ['a', 'f', 'g'], ['b', 'd', 'm']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        colname1 = 'col1'
        colname2 = 'col4'
        result_dola = pydf.cols_to_dol(colname1, colname2)

        self.assertEqual(result_dola, {})

    def test_cols_to_dol_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        colname1 = 'col1'
        colname2 = 'col2'
        result_dola = pydf.cols_to_dol(colname1, colname2)

        self.assertEqual(result_dola, {})

    def test_cols_to_dol_single_column(self):
        cols = ['col1']
        lol = [['a'], ['b'], ['a'], ['b']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str})

        colname1 = 'col1'
        colname2 = 'col2'
        result_dola = pydf.cols_to_dol(colname1, colname2)

        self.assertEqual(result_dola, {})

    # bool
    def test_bool_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        result = bool(pydf)

        self.assertFalse(result)

    def test_bool_nonempty_pydf(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        result = bool(pydf)

        self.assertTrue(result)

    def test_bool_pydf_with_empty_lol(self):
        cols = ['col1', 'col2']
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        result = bool(pydf)

        self.assertFalse(result)

    # len
    def test_len_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        result = len(pydf)

        self.assertEqual(result, 0)

    def test_len_nonempty_pydf(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        result = len(pydf)

        self.assertEqual(result, 3)

    def test_len_pydf_with_empty_lol(self):
        cols = ['col1', 'col2']
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        result = len(pydf)

        self.assertEqual(result, 0)
        
    # columns
    def test_columns_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        result = pydf.columns()

        self.assertEqual(result, [])

    def test_columns_nonempty_pydf(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', 'x'], [2, 'b', 'y'], [3, 'c', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': str})

        result = pydf.columns()

        self.assertEqual(result, ['col1', 'col2', 'col3'])
        
    # clone_empty
    
    def test_clone_empty_from_empty_instance(self):
        old_instance = Pydf()
        result = Pydf.clone_empty(old_instance)

        self.assertEqual(result.name, '')
        self.assertEqual(result.keyfield, '')
        self.assertEqual(result.hd, {})
        self.assertEqual(result.lol, [])
        self.assertEqual(result.kd, {})
        self.assertEqual(result.dtypes, {})
        self.assertEqual(result._iter_index, 0)

    def test_clone_empty_from_nonempty_instance(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        old_instance = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})
        result = Pydf.clone_empty(old_instance)

        self.assertEqual(result.name, old_instance.name)
        self.assertEqual(result.keyfield, old_instance.keyfield)
        self.assertEqual(result.hd, old_instance.hd)
        self.assertEqual(result.lol, [])
        self.assertEqual(result.kd, {})
        self.assertEqual(result.dtypes, old_instance.dtypes)
        self.assertEqual(result._iter_index, 0)

    def test_clone_empty_from_none(self):
        old_instance = None
        result = Pydf.clone_empty(old_instance)

        self.assertEqual(result.name, '')
        self.assertEqual(result.keyfield, '')
        self.assertEqual(result.hd, {})
        self.assertEqual(result.lol, [])
        self.assertEqual(result.kd, {})
        self.assertEqual(result.dtypes, {})
        self.assertEqual(result._iter_index, 0)

    # to_lod
    def test_to_lod_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        result = pydf.to_lod()

        self.assertEqual(result, [])

    def test_to_lod_nonempty_pydf(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        result = pydf.to_lod()

        expected_lod = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}, {'col1': 3, 'col2': 'c'}]
        self.assertEqual(result, expected_lod)

    # select_records
    def test_select_records_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        keys_ls = [1, 2, 3]
        result = pydf.select_records_pydf(keys_ls)

        self.assertEqual(result.name,   '')
        self.assertEqual(result.keyfield, 'col1')
        self.assertEqual(result.hd,     {})
        self.assertEqual(result.lol,    [])
        self.assertEqual(result.kd,     {})
        self.assertEqual(result.dtypes,  {})

    def test_select_records_nonempty_pydf(self):
        cols    = ['col1', 'col2']
        lol = [ [1, 'a'], 
                [2, 'b'], 
                [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        keys_ls = [2, 1]
        result = pydf.select_records_pydf(keys_ls)

        expected_lol = [[2, 'b'], [1, 'a']]
        self.assertEqual(result.name, pydf.name)
        self.assertEqual(result.keyfield, pydf.keyfield)
        self.assertEqual(result.hd, pydf.hd)
        self.assertEqual(result.lol, expected_lol)
        self.assertEqual(result.dtypes, pydf.dtypes)

    def test_select_records_empty_keys(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        dtypes={'col1': int, 'col2': str}
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes=dtypes)

        keys_ls = []
        result = pydf.select_records_pydf(keys_ls)

        self.assertEqual(result.name, '')
        self.assertEqual(result.keyfield, 'col1')
        self.assertEqual(result.hd, {'col1': 0, 'col2': 1})
        self.assertEqual(result.lol, [])
        self.assertEqual(result.kd, {})
        self.assertEqual(result.dtypes, dtypes)

    def test_select_records_pydf_without_inverse(self):
        # Initialize test data
        cols = ['ID', 'Name', 'Age']
        lol = [
            [1, 'John', 30],
            [2, 'Alice', 25],
            [3, 'Bob', 35]
        ]
        pydf = Pydf(lol=lol, cols=cols, keyfield='Name')  # Initialize Pydf with test data

        # Test without inverse
        keys_ls = ['John', 'Alice']  # Define the keys list
        expected_lol =[
            [1, 'John', 30],
            [2, 'Alice', 25],
        ]

        result_pydf = pydf.select_records_pydf(keys_ls)  # Call the method
        self.assertEqual(result_pydf.lol, expected_lol)  # Check if the selected row indices are correct

    def test_select_records_pydf_with_inverse(self):
        # Initialize test data
        cols = ['ID', 'Name', 'Age']
        lol = [
            [1, 'John', 30],
            [2, 'Alice', 25],
            [3, 'Bob', 35]
        ]
        pydf = Pydf(lol=lol, cols=cols, keyfield='Name')  # Initialize Pydf with test data

        # Test with inverse
        keys_ls = ['John', 'Alice']  # Define the keys list
        expected_lol =[
            [3, 'Bob', 35]
        ]
        result_pydf = pydf.select_records_pydf(keys_ls, inverse=True)  # Call the method with inverse=True
        self.assertEqual(result_pydf.lol, expected_lol)  # Check if the selected row indices are correct


    # assign_record
    def test_assign_record_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        record_da = {'col1': 1, 'col2': 'a'}
        pydf.assign_record_da(record_da)

        expected_lol = [[1, 'a']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_nonempty_pydf_add_new_record(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 4, 'col2': 'd'}
        pydf.assign_record_da(record_da)

        expected_lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_nonempty_pydf_update_existing_record(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 2, 'col2': 'x'}
        pydf.assign_record_da(record_da)

        expected_lol = [[1, 'a'], [2, 'x'], [3, 'c']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_missing_keyfield(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col2': 'x'}
        with self.assertRaises(RuntimeError):
            pydf.assign_record_da(record_da)

    def test_assign_record_fields_not_equal_to_columns(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 4, 'col2': 'd', 'col3': 'extra'}
        with self.assertRaises(RuntimeError):
            pydf.assign_record_da(record_da)

    # assign_record_irow
    def test_assign_record_irow_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        record_da = {'col1': 1, 'col2': 'a'}
        pydf.assign_record_da_irow(irow=0, record_da=record_da)

        expected_lol = [[1, 'a']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_irow_nonempty_pydf_add_new_record(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 4, 'col2': 'd'}
        pydf.assign_record_da_irow(irow=3, record_da=record_da)

        expected_lol = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_irow_nonempty_pydf_update_existing_record(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 2, 'col2': 'x'}
        pydf.assign_record_da_irow(irow=1, record_da=record_da)

        expected_lol = [[1, 'a'], [2, 'x'], [3, 'c']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_irow_invalid_irow(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], 
               [2, 'b'], 
               [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 4, 'col2': 'd'}
        
        pydf.assign_record_da_irow(irow=5, record_da=record_da)

        expected_lol = [[1, 'a'], 
                        [2, 'b'], 
                        [3, 'c'],
                        [4, 'd'],
                        ]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_record_irow_missing_record_da(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        pydf.assign_record_da_irow(irow=1, record_da=None)

        expected_lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        self.assertEqual(pydf.lol, expected_lol)

   # update_record_irow
    def test_update_record_irow_empty_pydf(self):
        cols = []
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={})

        record_da = {'col1': 1, 'col2': 'a'}
        pydf.update_record_da_irow(irow=0, record_da=record_da)

        self.assertEqual(pydf.lol, [])

    def test_update_record_irow_nonempty_pydf_update_existing_record(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 2, 'col2': 'x', 'col3': 'extra'}
        pydf.update_record_da_irow(irow=1, record_da=record_da)

        expected_lol = [[1, 'a'], [2, 'x'], [3, 'c']]
        self.assertEqual(pydf.lol, expected_lol)

    def test_update_record_irow_invalid_irow(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        record_da = {'col1': 4, 'col2': 'd'}
        pydf.update_record_da_irow(irow=5, record_da=record_da)

        self.assertEqual(pydf.lol, lol)

    def test_update_record_irow_missing_record_da(self):
        cols = ['col1', 'col2']
        lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        pydf.update_record_da_irow(irow=1, record_da=None)

        expected_lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        self.assertEqual(pydf.lol, expected_lol)

    # def test_update_record_irow_missing_hd(self):
        # cols = ['col1', 'col2']
        # hd = {'col1': 0, 'col2': 1}
        # lol = [[1, 'a'], [2, 'b'], [3, 'c']]
        # pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str})

        # record_da = {'col1': 2, 'col2': 'x'}
        # pydf.update_record_da_irow(irow=1, record_da=record_da)

        # self.assertEqual(pydf.lol, lol)

    # icol_to_la
    def test_icol_to_la_valid_icol(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        result_la = pydf.icol_to_la(1)

        expected_la = ['a', 'b', 'c']
        self.assertEqual(result_la, expected_la)

    def test_icol_to_la_invalid_icol(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        result_la = pydf.icol_to_la(3)

        self.assertEqual(result_la, [])

    def test_icol_to_la_empty_pydf(self):
        pydf = Pydf()

        result_la = pydf.icol_to_la(0)

        self.assertEqual(result_la, [])

    def test_icol_to_la_empty_column(self):
        cols = ['col1', 'col2', 'col3']
        lol = []
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        result_la = pydf.icol_to_la(0)

        self.assertEqual(result_la, [])

    def test_icol_to_la_unique(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'a', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        result_la = pydf.icol_to_la(1, unique=True)

        expected_la = ['a', 'b']
        self.assertEqual(result_la, expected_la)
        

    def test_icol_to_la_omit_nulls_true_with_null(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, '', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        result_la = pydf.icol_to_la(1, omit_nulls=True)

        expected_la = ['a', 'b']
        self.assertEqual(result_la, expected_la)
        

    def test_icol_to_la_omit_nulls_false_with_null(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, '', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        result_la = pydf.icol_to_la(1, omit_nulls=False)

        expected_la = ['a', 'b', '']
        self.assertEqual(result_la, expected_la)
        

    # assign_icol
    def test_assign_icol_valid_icol_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        col_la = [4, 'd', False]
        pydf.assign_icol(icol=1, col_la=col_la)

        expected_lol = [[1, 4, True], [2, 'd', False], [3, False, True]]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_icol_valid_icol_default(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], 
               [2, 'b', False], 
               [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        pydf.assign_icol(icol=1, default='x')

        expected_lol = [[1, 'x', True], 
                        [2, 'x', False], 
                        [3, 'x', True]]
        self.assertEqual(pydf.lol, expected_lol)

    def test_assign_icol_valid_append_icol_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ [1, 'a', True], 
                [2, 'b', False], 
                [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        col_la = [4, 'd', False]
        pydf.assign_icol(icol=-1, col_la=col_la)

        expected_lol = [[1, 'a', True, 4], 
                        [2, 'b', False, 'd'], 
                        [3, 'c', True, False]]
        self.assertEqual(pydf.lol, expected_lol)

    # def test_assign_icol_invalid_icol_col_la(self):
        # cols = ['col1', 'col2', 'col3']
        # hd = {'col1': 0, 'col2': 1, 'col3': 2}
        # lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        # pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        # col_la = [4, 'd', False]
        # pydf.assign_icol(icol=3, col_la=col_la)

        # self.assertEqual(pydf.lol, lol)

    def test_assign_icol_empty_pydf(self):
        pydf = Pydf()

        col_la = [4, 'd', False]
        pydf.assign_icol(icol=1, col_la=col_la)

        self.assertEqual(pydf.lol, [])

    # insert_icol
    def test_insert_icol_valid_icol_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        col_la = [4, 'd', False]
        pydf.insert_icol(icol=1, col_la=col_la)

        expected_lol = [[1, 4, 'a', True], [2, 'd', 'b', False], [3, False, 'c', True]]
        self.assertEqual(pydf.lol, expected_lol)

    def test_insert_icol_valid_append_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        col_la = [4, 'd', False]
        pydf.insert_icol(icol=-1, col_la=col_la)

        expected_lol = [[1, 'a', True, 4], [2, 'b', False, 'd'], [3, 'c', True, False]]
        self.assertEqual(pydf.lol, expected_lol)

    def test_insert_icol_invalid_icol_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ [1, 'a', True], 
                [2, 'b', False], 
                [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        col_la = [4, 'd', False]
        pydf.insert_icol(icol=3, col_la=col_la)

        result_lol = [ [1, 'a', True, 4], 
                [2, 'b', False, 'd'], 
                [3, 'c', True,  False]]

        self.assertEqual(pydf.lol, result_lol)

    def test_insert_icol_empty_pydf(self):
        pydf = Pydf()

        col_la = [4, 'd', False]
        pydf.insert_icol(icol=1, col_la=col_la)

        self.assertEqual(pydf.lol, [])

    # insert_col
    def test_insert_col_valid_colname_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols,  lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        colname = 'new_col'
        col_la = [4, 'd', False]
        pydf.insert_col(colname=colname, col_la=col_la, icol=1)

        expected_lol = [[1, 4, 'a', True], [2, 'd', 'b', False], [3, False, 'c', True]]
        expected_hd = {'col1': 0, 'new_col': 1, 'col2': 2, 'col3': 3}
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)
        

    def test_insert_col_existing_colname_col_la(self):
        # insert a column that already exists and it will overwrite the contents of that column
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols,  lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        colname = 'col2'
        col_la = [4, 'd', False]
        pydf.insert_col(colname=colname, col_la=col_la, icol=1)

        expected_lol = [[1, 4, True], [2, 'd', False], [3, False, True]]
        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2}
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)
        

    def test_insert_col_valid_colname_append_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ [1, 'a', True], 
                [2, 'b', False], 
                [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        colname = 'new_col'
        col_la = [4, 'd', False]
        pydf.insert_col(colname=colname, col_la=col_la, icol=-1)

        expected_lol = [[1, 'a', True,  4], 
                        [2, 'b', False, 'd'], 
                        [3, 'c', True,  False]]
        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2, 'new_col': 3}
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)
        

    def test_insert_col_valid_colname_invalid_icol_col_la(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ [1, 'a', True], 
                [2, 'b', False], 
                [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        colname = 'new_col'
        col_la = [4, 'd', False]
        pydf.insert_col(colname=colname, col_la=col_la, icol=3)

        expected_hd = {'col1': 0, 'col2': 1, 'col3': 2, 'new_col': 3}
        expected_lol = [ [1, 'a', True,     4], 
                         [2, 'b', False,    'd'], 
                         [3, 'c', True,     False]]

        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)
        

    def test_insert_col_valid_colname_empty_pydf(self):
        pydf = Pydf()

        colname = 'new_col'
        col_la = [4, 'd', False]
        pydf.insert_col(colname=colname, col_la=col_la, icol=1)

        self.assertEqual(pydf.lol, [])
        self.assertEqual(pydf.hd, {'new_col': 0})
        

    def test_insert_col_empty_colname(self):
        cols = ['col1', 'col2', 'col3']
        hd = {'col1': 0, 'col2': 1, 'col3': 2}
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        pydf.insert_col(colname='', col_la=[4, 'd', False], icol=1)

        self.assertEqual(pydf.lol, lol)
        self.assertEqual(pydf.hd, hd)
        

    # insert_idx_col
    def test_insert_idx_col_valid_icol_startat(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        colname = 'idx'
        pydf.insert_idx_col(colname=colname, icol=1, startat=10)

        expected_lol = [[1, 10, 'a', True], [2, 11, 'b', False], [3, 12, 'c', True]]
        expected_hd = {'col1': 0, 'idx': 1, 'col2': 2, 'col3': 3}
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)
        

    def test_insert_idx_col_valid_icol_default_startat(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        colname = 'idx'
        pydf.insert_idx_col(colname=colname, icol=1)

        expected_lol = [[1, 0, 'a', True], [2, 1, 'b', False], [3, 2, 'c', True]]
        expected_hd = {'col1': 0, 'idx': 1, 'col2': 2, 'col3': 3}
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)

    def test_insert_idx_col_valid_append_default_startat(self):
        pydf = Pydf()

        colname = 'idx'
        pydf.insert_idx_col(colname=colname)

        expected_lol = []
        expected_hd = {'idx': 0}
        self.assertEqual(pydf.lol, expected_lol)
        self.assertEqual(pydf.hd, expected_hd)

    def test_insert_idx_col_empty_colname(self):
        cols = ['col1', 'col2', 'col3']
        hd = {'col1': 0, 'col2': 1, 'col3': 2}
        lol = [[1, 'a', True], [2, 'b', False], [3, 'c', True]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': str, 'col3': bool})

        pydf.insert_idx_col(colname='', icol=1, startat=10)

        self.assertEqual(pydf.lol, lol)
        self.assertEqual(pydf.hd, hd)

    # select_cols
    def test_select_cols_with_cols(self):
        # Test case where columns are selected based on the cols parameter
        pydf = Pydf(lol=[[1, 'a', True], [2, 'b', False], [3, 'c', True]], cols=['ID', 'Name', 'Flag'], dtypes={'ID': int, 'Name': str, 'Flag': bool})
        new_pydf = pydf.select_cols(cols=['ID', 'Flag'])
        self.assertEqual(new_pydf.columns(), ['ID', 'Flag'])
        self.assertEqual(new_pydf.lol,  [[1, True], [2, False], [3, True]])
        
        # verify that the original is unchanged
        self.assertEqual(pydf.columns(), ['ID', 'Name', 'Flag'])
        self.assertEqual(pydf.lol,  [[1, 'a', True], [2, 'b', False], [3, 'c', True]])
        

    def test_select_cols_with_exclude_cols(self):
        # Test case where columns are selected based on the exclude_cols parameter
        pydf = Pydf(lol=[[1, 'a', True], [2, 'b', False], [3, 'c', True]], cols=['ID', 'Name', 'Flag'], dtypes={'ID': int, 'Name': str, 'Flag': bool})
        new_pydf = pydf.select_cols(exclude_cols=['Name'])
        self.assertEqual(new_pydf.columns(), ['ID', 'Flag'])
        self.assertEqual(new_pydf.lol,  [[1, True], [2, False], [3, True]])

    def test_select_cols_with_empty_params(self):
        # Test case where no cols or exclude_cols are provided
        pydf = Pydf(lol=[[1, 'a', True], [2, 'b', False], [3, 'c', True]], cols=['ID', 'Name', 'Flag'], dtypes={'ID': int, 'Name': str, 'Flag': bool})
        new_pydf = pydf.select_cols()
        self.assertEqual(new_pydf, pydf)

    def test_select_cols_with_empty_pydf(self):
        # Test case where Pydf is empty
        pydf = Pydf()
        new_pydf = pydf.select_cols(cols=['ID', 'Name'])
        self.assertEqual(new_pydf.columns(), [])


    # unified sum
    def test_sum_all_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': int, 'col3': int})

        result_sum = pydf.sum()
        expected_sum = {'col1': 12, 'col2': 15, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_sum_selected_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': int, 'col3': int})

        result_sum = pydf.sum(colnames_ls=['col1', 'col3'])
        expected_sum = {'col1': 12, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_sum_numeric_only(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 2, 3], ['b', 5, 6], ['c', 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': int, 'col3': int})

        result_sum = pydf.sum(numeric_only=True)
        expected_sum = {'col1': '0.0', 'col2': 15, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_sum_empty_pydf(self):
        pydf = Pydf()

        result_sum = pydf.sum()
        expected_sum = {}
        self.assertEqual(result_sum, expected_sum)

    # unified sum_np
    def test_sum_np_all_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': int, 'col3': int})

        result_sum = pydf.sum_np()
        expected_sum = {'col1': 12, 'col2': 15, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_sum_np_selected_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': int, 'col3': int})

        result_sum = pydf.sum_np(colnames_ls=['col1', 'col3'])
        expected_sum = {'col1': 12, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_sum_np_empty_pydf(self):
        pydf = Pydf()

        result_sum = pydf.sum_np()
        expected_sum = {}
        self.assertEqual(result_sum, expected_sum)


    # pydf_sum
    def test_pydf_sum_all_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': int, 'col3': int})

        result_sum = pydf.pydf_sum()
        expected_sum = {'col1': 12, 'col2': 15, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_pydf_sum_selected_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': int, 'col2': int, 'col3': int})

        result_sum = pydf.pydf_sum(cols=['col1', 'col3'])
        expected_sum = {'col1': 12, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_pydf_sum_include_types_int(self):
        cols = ['col1', 'col2', 'col3']
        dtypes_dict = {'col1': str, 'col2': int, 'col3': int}
        lol = [['a', 2, 3], ['b', 5, 6], ['c', 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes=dtypes_dict)

        reduce_cols = pydf.calc_cols(include_types=int)
        result_sum = pydf.pydf_sum(cols=reduce_cols)
        expected_sum = {'col2': 15, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_pydf_sum_include_types_int_and_float(self):
        cols = ['col1', 'col2', 'col3']
        dtypes_dict = {'col1': str, 'col2': int, 'col3': float}
        lol = [['a', 2, 3.2], ['b', 5, 6.1], ['c', 8, 9.4]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes=dtypes_dict)

        reduce_cols = pydf.calc_cols(include_types=[int, float])
        result_sum = pydf.pydf_sum(cols=reduce_cols)
        expected_sum = {'col1': '', 'col2': 15, 'col3': 18.7}
        self.assertAlmostEqual(result_sum['col2'], expected_sum['col2'], places=2)
        self.assertAlmostEqual(result_sum['col3'], expected_sum['col3'], places=2)
        #self.assertEqual(result_sum, expected_sum)

    def test_pydf_sum_exclude_type_str(self):
        cols = ['col1', 'col2', 'col3']
        dtypes_dict = {'col1': str, 'col2': int, 'col3': int}
        lol = [['a', 2, 3], ['b', 5, 6], ['c', 8, 9]]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes=dtypes_dict)

        reduce_cols = pydf.calc_cols(exclude_types=[str, bool, list])
        result_sum = pydf.pydf_sum(cols=reduce_cols)
        expected_sum = {'col2': 15, 'col3': 18}
        self.assertEqual(result_sum, expected_sum)

    def test_pydf_sum_empty_pydf(self):
        pydf = Pydf()

        result_sum = pydf.pydf_sum()
        expected_sum = {}
        self.assertEqual(result_sum, expected_sum)

    # valuecounts_for_colname
    def test_valuecounts_for_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname('col2')
        expected_valuecounts = {'x': 2, 'y': 1, 'z': 1}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname('col2', sort=True)
        expected_valuecounts = {'x': 2, 'z': 1, 'y': 1}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_reverse_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname('col2', sort=True, reverse=True)
        expected_valuecounts = {'x': 2, 'y': 1, 'z': 1}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_empty_pydf(self):
        pydf = Pydf()

        result_valuecounts = pydf.valuecounts_for_colname('col2')
        expected_valuecounts = {}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    # valuecounts_for_colnames_ls
    def test_valuecounts_for_colnames_ls(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls(['col2', 'col3'])
        expected_valuecounts = {'col2': {'x': 2, 'y': 1, 'z': 1}, 'col3': {'y': 2, 'z': 2}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls(['col2', 'col3'], sort=True)
        expected_valuecounts = {'col2': {'x': 2, 'z': 1, 'y': 1}, 'col3': {'y': 2, 'z': 2}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_reverse_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls(['col2', 'col3'], sort=True, reverse=True)
        expected_valuecounts = {'col2': {'x': 2, 'y': 1, 'z': 1}, 'col3': {'z': 2, 'y': 2}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_empty_pydf(self):
        pydf = Pydf()

        result_valuecounts = pydf.valuecounts_for_colnames_ls(['col2', 'col3'])
        expected_valuecounts = {'col2': {}, 'col3': {}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_all_columns(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls()
        expected_valuecounts = {'col1': {'a': 2, 'b': 1, 'c': 1},
                                'col2': {'x': 2, 'y': 1, 'z': 1},
                                'col3': {'y': 2, 'z': 2}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    # valuecounts_for_colname_selectedby_colname
    def test_valuecounts_for_colname_selectedby_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname_selectedby_colname('col2', 'col1', 'a')
        expected_valuecounts = {'x': 1, 'y': 1}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_selectedby_colname_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname_selectedby_colname('col2', 'col1', 'a', sort=True)
        expected_valuecounts = {'y': 1, 'x': 1}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_selectedby_colname_reverse_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname_selectedby_colname('col2', 'col1', 'a', sort=True, reverse=True)
        expected_valuecounts = {'x': 1, 'y': 1}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_selectedby_colname_not_found(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname_selectedby_colname('col2', 'col1', 'not_found')
        expected_valuecounts = {}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname_selectedby_colname_empty_pydf(self):
        pydf = Pydf()

        result_valuecounts = pydf.valuecounts_for_colname_selectedby_colname('col2', 'col1', 'a')
        expected_valuecounts = {}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    # valuecounts_for_colnames_ls_selectedby_colname
    def test_valuecounts_for_colnames_ls_selectedby_colname(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['c', 'y', 'y'], 
                ['d', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls_selectedby_colname(
            colnames_ls=['col2', 'col3'],
            selectedby_colname='col1',
            selectedby_colvalue='a'
        )
        expected_valuecounts = {'col2': {'x': 1}, 'col3': {'y': 1}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_selectedby_colname_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['c', 'y', 'y'], 
                ['d', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls_selectedby_colname(
            colnames_ls=['col1', 'col2'],
            selectedby_colname='col3',
            selectedby_colvalue='y',
            sort=True
        )
        expected_valuecounts = {'col1': {'a': 1, 'c': 1}, 'col2': {'x': 1, 'y': 1}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_selectedby_colname_reverse_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['a', 'y', 'y'], 
                ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, dtypes={'col1': str, 'col2': str, 'col3': str}, keyfield='')

        result_valuecounts = pydf.valuecounts_for_colnames_ls_selectedby_colname(
            colnames_ls=['col2', 'col3'],
            selectedby_colname='col1',
            selectedby_colvalue='a',
            sort=True,
            reverse=True
        )
        expected_valuecounts = {'col2': {'x': 1, 'y': 1}, 'col3': {'y': 2}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_selectedby_colname_not_found(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['c', 'y', 'y'], 
                ['d', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colnames_ls_selectedby_colname(
            colnames_ls=['col2', 'col3'],
            selectedby_colname='col1',
            selectedby_colvalue='not_found'
        )
        expected_valuecounts = {'col2': {}, 'col3': {}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colnames_ls_selectedby_colname_empty_pydf(self):
        pydf = Pydf()

        result_valuecounts = pydf.valuecounts_for_colnames_ls_selectedby_colname(
            colnames_ls=['col2', 'col3'],
            selectedby_colname='col1',
            selectedby_colvalue='a'
        )
        expected_valuecounts = {'col2': {}, 'col3': {}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    # aluecounts_for_colname1_groupedby_colname2
    def test_valuecounts_for_colname1_groupedby_colname2(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['c', 'y', 'y'], 
                ['d', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname1_groupedby_colname2(
            colname1='col1',
            groupedby_colname2='col2'
        )
        expected_valuecounts = {'x': {'a': 1, 'b': 1}, 'y': {'c': 1}, 'z': {'d': 1}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname1_groupedby_colname2_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['c', 'y', 'y'], 
                ['d', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname1_groupedby_colname2(
            colname1='col1',
            groupedby_colname2='col2',
            sort=True
        )
        expected_valuecounts = {'x': {'a': 1, 'b': 1}, 'y': {'c': 1}, 'z': {'d': 1}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname1_groupedby_colname2_reverse_sort(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['c', 'y', 'y'], 
                ['d', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname1_groupedby_colname2(
            colname1='col1',
            groupedby_colname2='col2',
            sort=True,
            reverse=True
        )
        expected_valuecounts = {'x': {'a': 1, 'b': 1}, 'y': {'c': 1}, 'z': {'d': 1}}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname1_groupedby_colname2_not_found(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_valuecounts = pydf.valuecounts_for_colname1_groupedby_colname2(
            colname1='col1',
            groupedby_colname2='not_found'
        )
        expected_valuecounts = {}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    def test_valuecounts_for_colname1_groupedby_colname2_empty_pydf(self):
        pydf = Pydf()

        result_valuecounts = pydf.valuecounts_for_colname1_groupedby_colname2(
            colname1='col1',
            groupedby_colname2='col2'
        )
        expected_valuecounts = {}
        self.assertEqual(result_valuecounts, expected_valuecounts)

    # groupby
    def test_groupby(self):
        cols = ['col1', 'col2', 'col3']
        lol = [ ['a', 'x', 'y'], 
                ['b', 'x', 'z'], 
                ['a', 'y', 'y'], 
                ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        result_dopydf = pydf.groupby(colname='col2')

        lolx = [ ['a', 'x', 'y'], 
                 ['b', 'x', 'z']]
        loly = [ ['a', 'y', 'y']]
        lolz = [['c', 'z', 'z']]


        pydf_x = Pydf(cols=cols, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str}, lol=lolx)
        pydf_y = Pydf(cols=cols, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str}, lol=loly)
        pydf_z = Pydf(cols=cols, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str}, lol=lolz)


        expected_dopydf = {
            'x': pydf_x,
            'y': pydf_y,
            'z': pydf_z
        }

        for colvalue, expected_pydf in expected_dopydf.items():
            result_pydf = result_dopydf[colvalue]
            self.assertEqual(result_pydf.columns(), expected_pydf.columns())
            self.assertEqual(result_pydf.to_lod(), expected_pydf.to_lod())

    def test_groupby_empty_pydf(self):
        pydf = Pydf()

        result_dopydf = pydf.groupby(colname='col1')

        expected_dopydf = {}
        self.assertEqual(result_dopydf, expected_dopydf)

    def test_groupby_colname_not_found(self):
        cols = ['col1', 'col2', 'col3']
        lol = [['a', 'x', 'y'], ['b', 'x', 'z'], ['a', 'y', 'y'], ['c', 'z', 'z']]
        pydf = Pydf(cols=cols, lol=lol, keyfield='col1', dtypes={'col1': str, 'col2': str, 'col3': str})

        with self.assertRaises(KeyError):
            pydf.groupby(colname='not_found')

    # test __get_item__
    def test_getitem_single_row_0(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[0]
        expected_lol = [[1, 2, 3]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_1(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1]
        expected_lol = [[4, 5, 6]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_2(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[2]
        expected_lol = [[7, 8, 9]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_minus_1(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[-1]
        expected_lol = [[7, 8, 9]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_minus_2(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[-2]
        expected_lol = [[4, 5, 6]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_cell_01(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[0,1]
        expected_lol = [[2]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_cell_10(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1,0]
        expected_lol = [[4]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_cell_11(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1,1]
        expected_lol = [[5]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_with_cols(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1, :]
        expected_lol = [[4, 5, 6]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_col(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, 1]
        expected_lol = [[2], [5], [8]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_colname(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, 'B']
        expected_lol = [[2], [5], [8]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_col_with_rows(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, 1:2]
        expected_lol = [[2], [5], [8]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_col_with_reduced_rows(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[0:2, 1:2]
        expected_lol = [[2], [5]]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_rows_and_cols(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1:3, 0:2]
        expected_result = Pydf(lol=[[4, 5], [7, 8]], cols=['A', 'B'])
        self.assertEqual(result, expected_result)

    def test_getitem_col_idx_list(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, [0,2]]
        expected_result = Pydf(lol=[[1, 3], [4, 6], [7, 9]], cols=['A', 'C'])
        
        # print(f"{result=}\n")
        # print(f"{expected_result=}\n")
        self.assertEqual(result, expected_result)

    def test_getitem_col_name_list(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, ['A','C']]
        expected_result = Pydf(lol=[[1, 3], [4, 6], [7, 9]], cols=['A', 'C'])
        self.assertEqual(result, expected_result)

    def test_getitem_row_idx_list(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[[0,2]]
        expected_result = Pydf(lol=[[1, 2, 3], [7, 8, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(result, expected_result)

    def test_getitem_row_name_list(self):
        self.pydf_instance = Pydf(lol=[['a', 1, 2, 3], ['b', 4, 5, 6], ['c', 7, 8, 9]], 
                                    cols=['k', 'A', 'B', 'C'], keyfield='k')
        result = self.pydf_instance[['a','c']]
        expected_result = Pydf(lol=[['a', 1, 2, 3], ['c', 7, 8, 9]], cols=['k', 'A', 'B', 'C'], keyfield='k')
        self.assertEqual(result, expected_result)

    # getitem retmode==val
    def test_getitem_single_row_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[1]
        expected_val = [4, 5, 6]
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_minus_1(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[-1]
        expected_lol = [7, 8, 9]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_minus_2(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[-2]
        expected_lol = [4, 5, 6]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_cell_01_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[0,1]
        expected_val = 2
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_10_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[1,0]
        expected_val = 4
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_11_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[1,1]
        expected_val = 5
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_with_cols_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[1, :]
        expected_val = [4, 5, 6]
        self.assertEqual(result, expected_val)

    def test_getitem_single_col_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[:, 1]
        expected_val = [2, 5, 8]
        self.assertEqual(result, expected_val)

    def test_getitem_single_colname_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[:, 'B']
        expected_val = [2, 5, 8]
        self.assertEqual(result, expected_val)

    def test_getitem_single_col_with_rows_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[:, 1:2]
        expected_val = [2, 5, 8]
        self.assertEqual(result, expected_val)

    def test_getitem_single_col_with_reduced_rows_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[0:2, 1:2]
        expected_val = [2, 5]
        self.assertEqual(result, expected_val)

    def test_getitem_rows_and_cols_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[1:3, 0:2]
        expected_result = Pydf(lol=[[4, 5], [7, 8]], cols=['A', 'B'])
        self.assertEqual(result, expected_result)

    def test_getitem_col_idx_list_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[:, [0,2]]
        expected_result = Pydf(lol=[[1, 3], [4, 6], [7, 9]], cols=['A', 'C'])
        
        # print(f"{result=}\n")
        # print(f"{expected_result=}\n")
        self.assertEqual(result, expected_result)

    def test_getitem_col_name_list_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[:, ['A','C']]
        expected_result = Pydf(lol=[[1, 3], [4, 6], [7, 9]], cols=['A', 'C'])
        self.assertEqual(result, expected_result)

    def test_getitem_row_idx_list_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'], retmode='val')
        result = self.pydf_instance[[0,2]]
        expected_result = Pydf(lol=[[1, 2, 3], [7, 8, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(result, expected_result)

    def test_getitem_row_name_list_val(self):
        self.pydf_instance = Pydf(lol=[['a', 1, 2, 3], ['b', 4, 5, 6], ['c', 7, 8, 9]], 
                                    cols=['k', 'A', 'B', 'C'], keyfield='k', retmode='val')
        result = self.pydf_instance[['a','c']]
        expected_result = Pydf(lol=[['a', 1, 2, 3], ['c', 7, 8, 9]], cols=['k', 'A', 'B', 'C'], keyfield='k')
        self.assertEqual(result, expected_result)


    # getitem with .to_...()
    def test_getitem_single_row_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1].to_list()
        expected_val = [4, 5, 6]
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_minus_1(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[-1].to_list()
        expected_lol = [7, 8, 9]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_row_minus_2(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[-2].to_list()
        expected_lol = [4, 5, 6]
        self.assertEqual(result.lol, expected_lol)

    def test_getitem_single_cell_01_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[0,1].to_value()
        expected_val = 2
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_10_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1,0].to_value()
        expected_val = 4
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_11_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1,1].to_value()
        expected_val = 5
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_with_cols_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1, :].to_list()
        expected_val = [4, 5, 6]
        self.assertEqual(result, expected_val)

    def test_getitem_single_col_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, 1].to_list()
        expected_val = [2, 5, 8]
        self.assertEqual(result, expected_val)

    def test_getitem_single_colname_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, 'B'].to_list()
        expected_val = [2, 5, 8]
        self.assertEqual(result, expected_val)

    def test_getitem_single_col_with_rows_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[:, 1:2].to_list()
        expected_val = [2, 5, 8]
        self.assertEqual(result, expected_val)

    def test_getitem_single_col_with_reduced_rows_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[0:2, 1:2].to_list()
        expected_val = [2, 5]
        self.assertEqual(result, expected_val)


    def test_getitem_single_row_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1].to_dict()
        expected_val = {'A':4, 'B':5, 'C':6}
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_minus_1(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[-1].to_dict()
        expected_val = {'A':7, 'B':8, 'C':9}
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_minus_2(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[-2].to_dict()
        expected_val = {'A':4, 'B':5, 'C':6}
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_01_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[0,1].to_dict()
        expected_val = {'B':2}
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_10_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1,0].to_dict()
        expected_val = {'A':4}
        self.assertEqual(result, expected_val)

    def test_getitem_single_cell_11_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1,1].to_dict()
        expected_val = {'B':5}
        self.assertEqual(result, expected_val)

    def test_getitem_single_row_with_cols_val(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        result = self.pydf_instance[1, :].to_dict()
        expected_val = {'A':4, 'B':5, 'C':6}
        self.assertEqual(result, expected_val)






    # test transpose
    def test_transpose(self):
        self.pydf_instance = Pydf(lol=[[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10]], cols=['A', 'B', 'C', 'D'], keyfield='A')
        result = self.pydf_instance.transpose(new_keyfield='x', new_cols=['x', 'y', 'z'])
        expected_result = Pydf(lol=[[1, 4, 7], [2, 5, 8], [3, 6, 9], [4, 7, 10]], keyfield='x', cols=['x', 'y', 'z']) 
        self.assertEqual(result, expected_result)


    def test_split_pydf_into_chunks_lopydf(self):
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]],
            cols=['A', 'B', 'C']
            )
        max_chunk_size = 2  # Set the maximum chunk size for testing

        # Call the method to split the Pydf into chunks
        chunks_lopydf = self.pydf_instance.split_pydf_into_chunks_lopydf(max_chunk_size)

        # Check if the length of each chunk is within the specified max_chunk_size
        for chunk in chunks_lopydf:
            self.assertLessEqual(len(chunk), max_chunk_size)

        # Check if the sum of the lengths of all chunks equals the length of the original Pydf
        total_length = sum(len(chunk) for chunk in chunks_lopydf)
        self.assertEqual(total_length, len(self.pydf_instance))

    # __set_item__
    def test_set_item_row_list(self):
        # Assign an entire row using a list
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        self.pydf_instance[1] = {'A': 10, 'B': 20, 'C': 30}
        expected_result = Pydf(lol=[[1, 2, 3], [10, 20, 30], [7, 8, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(self.pydf_instance, expected_result)

    def test_set_item_row_value(self):
        # Assign an entire row using a single value
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        self.pydf_instance[2] = 100
        expected_result = Pydf(lol=[[1, 2, 3], [4, 5, 6], [100, 100, 100]], cols=['A', 'B', 'C'])
        self.assertEqual(self.pydf_instance, expected_result)

    def test_set_item_cell_value(self):
        # Assign a specific cell with a value
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        self.pydf_instance[0, 'B'] = 50
        expected_result = Pydf(lol=[[1, 50, 3], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(self.pydf_instance, expected_result)

    def test_set_item_cell_list(self):
        # Assign a specific cell with a list
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        
        self.pydf_instance[1, 'A'] = [100, 200, 300]
        expected_result = Pydf(lol=[[1, 2, 3], [[100, 200, 300], 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        
        self.longMessage = True
        
        if self.pydf_instance != expected_result:
            print (f"test_set_item_cell_list result:\n{self.pydf_instance}\nexpected{expected_result}")

        self.assertEqual(self.pydf_instance, expected_result)
        
    def test_set_item_row_range_list(self):
        # Assign values in a range of columns in a specific row with a list
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        self.pydf_instance[1, 1:3] = [99, 88]
        expected_result = Pydf(lol=[[1, 2, 3], [4, 99, 88], [7, 8, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(self.pydf_instance, expected_result)

    def test_set_item_row_range_value(self):
        # Assign a single value in a range of columns in a specific row
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        self.pydf_instance[0, 1:3] = 77
        expected_result = Pydf(lol=[[1, 77, 77], [4, 5, 6], [7, 8, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(self.pydf_instance, expected_result)

    def test_set_item_col_list(self):
        # Assign an entire column with a list
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
            )
        #import pdb; pdb.set_trace() #temp
        self.pydf_instance[:, 'B'] = [55, 66, 77]
        expected_result = Pydf(lol=[[1, 55, 3], [4, 66, 6], [7, 77, 9]], cols=['A', 'B', 'C'])
        if self.pydf_instance != expected_result:
            print (f"test_set_item_col_list result:\n{self.pydf_instance}\nexpected{expected_result}")

        self.assertEqual(self.pydf_instance, expected_result)

    def test_set_item_col_range_list(self):
        # Assign values in a range of rows in a specific column with a list
        # Example: Create a Pydf instance with some sample data
        self.pydf_instance = Pydf(
            lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            cols=['A', 'B', 'C']
        )
        self.pydf_instance[1:3, 'B'] = [44, 33]
        expected_result = Pydf(lol=[[1, 2, 3], [4, 44, 6], [7, 33, 9]], cols=['A', 'B', 'C'])
        self.assertEqual(self.pydf_instance, expected_result)

    # select_where
    def test_select_where_basic_condition(self):
        # Test a basic condition where col1 values are greater than 2
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_pydf = pydf.select_where(lambda row: row['col1'] > 2)
        expected_data = Pydf(cols=['col1', 'col2'], lol=[[3, 6]])
        self.assertEqual(result_pydf, expected_data)

    def test_select_where_invalid_condition_runtime_error(self):
        # Test an invalid condition causing a runtime error
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        with self.assertRaises(ZeroDivisionError) as context:
            pydf.select_where(lambda row: 1 / 0)

        self.assertIn("division by zero", str(context.exception))

    def test_select_where_empty_result(self):
        # Test a condition that results in an empty Pydf
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_pydf = pydf.select_where(lambda row: row['col1'] > 10)
        expected_data = Pydf(cols=['col1', 'col2'], lol=[])
        self.assertEqual(result_pydf, expected_data)

    def test_select_where_complex_condition(self):
        # Test a complex condition involving multiple columns
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_pydf = pydf.select_where(lambda row: row['col1'] > 1 and row['col2'] < 6)
        expected_data = Pydf(cols=['col1', 'col2'], lol=[[2, 5]])
        self.assertEqual(result_pydf, expected_data)

    def test_select_where_complex_condition_indexes(self):
        # Test a complex condition involving multiple columns
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_pydf = pydf.select_where(lambda row: bool(list(row.values())[0] > 1 and list(row.values())[1] < 6))
        expected_data = Pydf(cols=['col1', 'col2'], lol=[[2, 5]])
        self.assertEqual(result_pydf, expected_data)

    # select_where_idxs
    def test_select_where_idxs_basic_condition(self):
        # Test a basic condition where col1 values are greater than 2
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_idxs_list = pydf.select_where_idxs(lambda row: row['col1'] > 2)
        expected_data = [2]
        self.assertEqual(result_idxs_list, expected_data)

    def test_select_where_idxs_invalid_condition_runtime_error(self):
        # Test an invalid condition causing a runtime error
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        with self.assertRaises(ZeroDivisionError) as context:
            pydf.select_where_idxs(lambda row: 1 / 0)

        self.assertIn("division by zero", str(context.exception))

    def test_select_where_idxs_empty_result(self):
        # Test a condition that results in an empty Pydf
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_list = pydf.select_where_idxs(lambda row: row['col1'] > 10)
        expected_data = []
        self.assertEqual(result_list, expected_data)

    def test_select_where_idxs_complex_condition(self):
        # Test a complex condition involving multiple columns
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_list = pydf.select_where_idxs(lambda row: row['col1'] > 1 and row['col2'] < 6)
        expected_data = [1]
        self.assertEqual(result_list, expected_data)

    def test_select_where_idxs_complex_condition_indexes(self):
        # Test a complex condition involving multiple columns
        pydf = Pydf(cols=['col1', 'col2'], lol=[[1, 4], [2, 5], [3, 6]])

        result_list = pydf.select_where_idxs(lambda row: bool(list(row.values())[0] > 1 and list(row.values())[1] < 6))
        expected_data = [1]
        self.assertEqual(result_list, expected_data)


    # test test_from_cols_dol
    def test_from_cols_dol_empty_input(self):
        # Test creating Pydf instance from empty cols_dol
        cols_dol = {}
        result_pydf = Pydf.from_cols_dol(cols_dol)
        expected_pydf = Pydf()
        self.assertEqual(result_pydf, expected_pydf)

    def test_from_cols_dol_basic_input(self):
        # Test creating Pydf instance from cols_dol with basic data
        cols_dol = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
        result_pydf = Pydf.from_cols_dol(cols_dol)
        expected_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        self.assertEqual(result_pydf, expected_pydf)

    def test_from_cols_dol_with_keyfield(self):
        # Test creating Pydf instance from cols_dol with keyfield specified
        cols_dol = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
        result_pydf = Pydf.from_cols_dol(cols_dol, keyfield='A')
        expected_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 4, 7], [2, 5, 8], [3, 6, 9]], keyfield='A')
        self.assertEqual(result_pydf, expected_pydf)

    def test_from_cols_dol_with_dtypes(self):
        # Test creating Pydf instance from cols_dol with specified dtype
        cols_dol = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
        dtypes = {'A': int, 'B': float, 'C': str}
        result_pydf = Pydf.from_cols_dol(cols_dol, dtypes=dtypes)
        expected_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 4.0, '7'], [2, 5.0, '8'], [3, 6.0, '9']], dtypes=dtypes)
        self.assertEqual(result_pydf, expected_pydf)

    # # to_dict
    # def test_to_dict_empty_pydf(self):
        # # Test to_dict() on an empty Pydf instance
        # pydf = Pydf()
        # #result_dict = pydf.to_dict()
        # #expected_pydf = {'cols': [], 'lol': []}
        # self.assertEqual(pydf.lol, [])
        # self.assertEqual(pydf.kd, {})
        # self.assertEqual(pydf.kd, {})

    # def test_to_dict_with_data(self):
        # # Test to_dict() on a Pydf instance with data
        # pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        # #result_dict = pydf.to_dict()
        # expected_pydf = Pydf('cols'= ['A', 'B', 'C'], 'lol'= [[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        # self.assertEqual(result_pydf, expected_pydf)

    # def test_to_dict_with_keyfield_and_dtypes(self):
        # # Test to_dict() on a Pydf instance with keyfield and dtype
        # pydf = Pydf(cols=['A', 'B', 'C'], 
                    # lol=[[1, 4, 7], [2, 5, 8], [3, 6, 9]], 
                    # keyfield='A', 
                    # dtypes={'A': int, 'B': float, 'C': int})
        # #result_dict = pydf.to_dict()
        # expected_pydf = Pydf('cols'= ['A', 'B', 'C'], 'lol'= [[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        # self.assertEqual(result_pydf, expected_pydf)

    # apply_formulas
    def test_apply_formulas_basic_absolute(self):
        # Test apply_formulas with basic example
        example_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 0], [4, 5, 0], [7, 8, 0], [0, 0, 0]])
        formulas_pydf = Pydf(cols=['A', 'B', 'C'],
                             lol=[['', '', "$d[0,0]+$d[0,1]"],
                                  ['', '', "$d[1,0]+$d[1,1]"],
                                  ['', '', "$d[2,0]+$d[2,1]"],
                                  ["sum($d[0:3,$c])", "sum($d[0:3,$c])", "sum($d[0:3,$c])"]]
                             )
        expected_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 3], [4, 5, 9], [7, 8, 15], [12, 15, 27]])

        example_pydf.apply_formulas(formulas_pydf)
        self.assertEqual(example_pydf, expected_pydf)

    def test_apply_formulas_basic_relative(self):
        # Test apply_formulas with basic example
        example_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 0], [4, 5, 0], [7, 8, 0], [0, 0, 0]])
        formulas_pydf = Pydf(cols=['A', 'B', 'C'],
                             lol=[['', '', "$d[$r,0]+$d[$r,1]"],
                                  ['', '', "$d[$r,($c-2)]+$d[$r,($c-1)]"],
                                  ['', '', "sum($d[$r,0:2])"],
                                  ["sum($d[0:3,$c])", "sum($d[:-1,$c])", "sum($d[:$r,$c])"]]
                             )
        expected_result = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 3], [4, 5, 9], [7, 8, 15], [12, 15, 27]])

        example_pydf.apply_formulas(formulas_pydf)
        self.assertEqual(example_pydf, expected_result)

    def test_apply_formulas_no_changes(self):
        # Test apply_formulas with no changes expected
        example_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 0, 0]])
        formulas_pydf = Pydf(cols=['A', 'B', 'C'], lol=[['', '', ''], ['', '', ''], ['', '', ''], ['', '', '']])
        expected_result = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 0, 0]])

        example_pydf.apply_formulas(formulas_pydf)
        self.assertEqual(example_pydf, expected_result)

    def test_apply_formulas_excessive_loops(self):
        # Test apply_formulas resulting in excessive loops
        example_pydf = Pydf(cols=['A', 'B', 'C'], lol=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 0, 0]])
        formulas_pydf = Pydf(cols=['A', 'B', 'C'],
                             lol=[['', '', "$d[0,0]+$d[0,1]"],
                                  ['', '', "$d[1,0]+$d[1,1]"],
                                  ['$d[2,2]', '', "$d[2,0]+$d[2,1]"],     # this is circular
                                  ["sum($d[0:3,'A'])", "sum($d[0:3,'B'])", "sum($d[0:3,'C'])"]]
                             )

        with self.assertRaises(RuntimeError) as context:
            example_pydf.apply_formulas(formulas_pydf)

        self.assertIn("apply_formulas is resulting in excessive evaluation loops.", str(context.exception))

    def test_generate_spreadsheet_column_names_list(self):
        # Test for 0 columns
        self.assertEqual(Pydf._generate_spreadsheet_column_names_list(0), [])

        # Test for 1 column
        self.assertEqual(Pydf._generate_spreadsheet_column_names_list(1), ['A'])

        # Test for 5 columns
        self.assertEqual(Pydf._generate_spreadsheet_column_names_list(5), ['A', 'B', 'C', 'D', 'E'])

        # Test for 27 columns
        self.assertEqual(Pydf._generate_spreadsheet_column_names_list(27), ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA'])

        # Test for 52 columns
        self.assertEqual(Pydf._generate_spreadsheet_column_names_list(52), ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ'])

        # Test for 53 columns
        self.assertEqual(Pydf._generate_spreadsheet_column_names_list(53), ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA'])


    # from_lod_to_cols
    def test_from_lod_to_cols_empty_lod(self):
        result = Pydf.from_lod_to_cols([], cols=['A', 'B', 'C'], keyfield='Key')
        self.assertEqual(result.columns(), ['A', 'B', 'C'])
        self.assertEqual(result.lol, [])

    def test_from_lod_to_cols_no_cols_specified(self):
        lod = [{'A': 1, 'B': 2, 'C': 3}, {'A': 4, 'B': 5, 'C': 6}, {'A': 7, 'B': 8, 'C': 9}]
        result = Pydf.from_lod_to_cols(lod, keyfield='key')
        self.assertEqual(result.columns(), ['key', 'A', 'B', 'C'])
        self.assertEqual(result.lol, [['A', 1, 4, 7], ['B', 2, 5, 8], ['C', 3, 6, 9]])

    def test_from_lod_to_cols_with_cols(self):
        lod = [{'A': 1, 'B': 2, 'C': 3}, {'A': 4, 'B': 5, 'C': 6}, {'A': 7, 'B': 8, 'C': 9}]
        result = Pydf.from_lod_to_cols(lod, cols=['Feature', 'Try 1', 'Try 2', 'Try 3'], keyfield='Feature')
        self.assertEqual(result.columns(), ['Feature', 'Try 1', 'Try 2', 'Try 3'])
        self.assertEqual(result.lol, [['A', 1, 4, 7], ['B', 2, 5, 8], ['C', 3, 6, 9]])

    # apply
    def test_apply_row(self):
        pydf = Pydf.from_lod([  {'a': 1, 'b': 2}, 
                                {'a': 3, 'b': 4}])

        def transform_row(
                row: dict, 
                cols=None,                      # columns included in the reduce operation.
                **kwargs):
            return {'a': row['a'] * 2, 'b': row['b'] * 3}

        result_pydf = pydf.apply(transform_row, by='row')
        expected_result = Pydf.from_lod([{'a': 2, 'b': 6}, {'a': 6, 'b': 12}])

        self.assertEqual(result_pydf, expected_result)

    # def test_apply_col(self):
        # pydf = Pydf.from_lod([  {'a': 1, 'b': 2}, 
                                # {'a': 3, 'b': 4}])

        # def transform_col(col, cols, **kwargs):
            # col[0] = col[0] * 2
            # col[1] = col[1] * 3
            # return col

        # result_pydf = pydf.apply(transform_col, by='col')
        # expected_result = Pydf.from_lod([
                                # {'a': 2, 'b': 4}, 
                                # {'a': 9, 'b': 12}])

        # self.assertEqual(result_pydf, expected_result)


    def test_set_col2_from_col1_using_regex_select(self):
        # Initialize an instance of your class
        
        # Set up sample data for testing
        cols_dol = {'col1': ['abc (123)', 'def (456)', 'ghi (789)'],
                'col2': [None, None, None]}
        my_pydf = Pydf.from_cols_dol(cols_dol)

        # Call the method to apply the regex select
        my_pydf.set_col2_from_col1_using_regex_select('col1', 'col2', r'\((\d+)\)')
        
        col2_expected = Pydf(lol=[['123'], ['456'], ['789']], cols=['col2'])
        
        # Assert the expected results
        self.assertEqual(my_pydf[:, 'col2'], col2_expected)
        

    def test_groupby_cols_reduce(self):

        groupby_colnames = ['gender', 'religion', 'zipcode']
        reduce_colnames  = ['cancer', 'covid19', 'gun', 'auto']
            
        cols = ['gender', 'religion', 'zipcode', 'cancer', 'covid19', 'gun', 'auto']
        lol = [
            ['M', 'C', 90001,  1,  2,  3,  4],
            ['M', 'C', 90001,  5,  6,  7,  8],
            ['M', 'C', 90002,  9, 10, 11, 12],
            ['M', 'C', 90002, 13, 14, 15, 16],
            ['M', 'J', 90001,  1,  2,  3,  4],
            ['M', 'J', 90001, 13, 14, 15, 16],
            ['M', 'J', 90002,  5,  6,  7,  8],
            ['M', 'J', 90002,  9, 10, 11, 12],
            ['M', 'I', 90001, 13, 14, 15, 16],
            ['M', 'I', 90001,  1,  2,  3,  4],
            ['M', 'I', 90002,  4,  3,  2,  1],
            ['M', 'I', 90002,  9, 10, 11, 12],
            ['F', 'C', 90001,  4,  3,  2,  1],
            ['F', 'C', 90001,  5,  6,  7,  8],
            ['F', 'C', 90002,  4,  3,  2,  1],
            ['F', 'C', 90002, 13, 14, 15, 16],
            ['F', 'J', 90001,  4,  3,  2,  1],
            ['F', 'J', 90001,  1,  2,  3,  4],
            ['F', 'J', 90002,  8,  7,  6,  5],
            ['F', 'J', 90002,  1,  2,  3,  4],
            ['F', 'I', 90001,  8,  7,  6,  5],
            ['F', 'I', 90001,  5,  6,  7,  8],
            ['F', 'I', 90002,  8,  7,  6,  5],
            ['F', 'I', 90002, 13, 14, 15, 16],
            ]
            
        data_table_pydf = Pydf(cols=cols, lol=lol)
            
            
        grouped_and_summed_pydf = data_table_pydf.groupby_cols_reduce(
            groupby_colnames=groupby_colnames, 
            func = Pydf.sum_np,
            by='table',                                     # determines how the func is applied.
            reduce_cols = reduce_colnames,                  # columns included in the reduce operation.
            )

        expected_lol = [
            ['M', 'C', 90001,  6,  8, 10, 12],
            ['M', 'C', 90002, 22, 24, 26, 28],
            ['M', 'J', 90001, 14, 16, 18, 20],
            ['M', 'J', 90002, 14, 16, 18, 20],
            ['M', 'I', 90001, 14, 16, 18, 20],
            ['M', 'I', 90002, 13, 13, 13, 13],
            ['F', 'C', 90001,  9,  9,  9,  9],
            ['F', 'C', 90002, 17, 17, 17, 17],
            ['F', 'J', 90001,  5,  5,  5,  5],
            ['F', 'J', 90002,  9,  9,  9,  9],
            ['F', 'I', 90001, 13, 13, 13, 13],
            ['F', 'I', 90002, 21, 21, 21, 21],
            ]

        self.assertEqual(grouped_and_summed_pydf.lol, expected_lol)
        

    def test_is_d1_in_d2(self):
        # Test case where d1 is a subset of d2
        d1 = {'a': 1, 'b': 2}
        d2 = {'a': 1, 'b': 2, 'c': 3}
        assert utils.is_d1_in_d2(d1, d2) == True

        # Test case where d1 is equal to d2
        d1 = {'a': 1, 'b': 2}
        d2 = {'a': 1, 'b': 2}
        assert utils.is_d1_in_d2(d1, d2) == True

        # Test case where d1 is not a subset of d2
        d1 = {'a': 1, 'b': 2}
        d2 = {'a': 1, 'c': 3}
        assert utils.is_d1_in_d2(d1, d2) == False

        # Test case where d1 is an empty dictionary
        d1 = {}
        d2 = {'a': 1, 'b': 2}
        assert utils.is_d1_in_d2(d1, d2) == True

        # Test case where d2 is an empty dictionary
        d1 = {'a': 1, 'b': 2}
        d2 = {}
        assert utils.is_d1_in_d2(d1, d2) == False

        # Test case where both d1 and d2 are empty dictionaries
        d1 = {}
        d2 = {}
        assert utils.is_d1_in_d2(d1, d2) == True

        # Test case with mixed types of keys and values
        d1 = {'a': 1, 2: 'b', 'c': True}
        d2 = {'a': 1, 'b': 2, 'c': True}
        assert utils.is_d1_in_d2(d1, d2) == False

        # Test case where d1 has additional fields not present in d2
        d1 = {'a': 1, 'b': 2, 'd': 4}
        d2 = {'a': 1, 'b': 2}
        assert utils.is_d1_in_d2(d1, d2) == False


    def test_set_lol_with_new_lol(self):
        # Create a Pydf instance for testing
        self.cols = ['ID', 'Name', 'Age']
        self.lol = [[1, 'John', 30], [2, 'Alice', 25], [3, 'Bob', 35]]
        self.pydf = Pydf(cols=self.cols, lol=self.lol)

        # Define a new list-of-lists (lol)
        new_lol = [[4, 'David', 40], [5, 'Eve', 28]]

        # Call the set_lol method with the new lol
        self.pydf.set_lol(new_lol)

        # Check if lol is set correctly
        self.assertEqual(self.pydf.lol, new_lol)

    def test_set_lol_with_empty_lol(self):
        # Create a Pydf instance for testing
        self.cols = ['ID', 'Name', 'Age']
        self.lol = [[1, 'John', 30], [2, 'Alice', 25], [3, 'Bob', 35]]
        self.pydf = Pydf(cols=self.cols, lol=self.lol)

        # Define an empty lol
        new_lol = []

        # Call the set_lol method with the empty lol
        self.pydf.set_lol(new_lol)

        # Check if lol is set correctly to empty list
        self.assertEqual(self.pydf.lol, new_lol)

    def test_set_lol_recalculates_kd(self):
        # Create a Pydf instance for testing
        self.cols = ['ID', 'Name', 'Age']
        self.lol = [[1, 'John', 30], [2, 'Alice', 25], [3, 'Bob', 35]]
        self.pydf = Pydf(cols=self.cols, lol=self.lol)

        # Define a new list-of-lists (lol)
        new_lol = [[4, 'David', 40], [5, 'Eve', 28]]

        # Call the set_lol method with the new lol
        self.pydf.set_lol(new_lol)

        # Check if kd is recalculated
        self.assertIsNotNone(self.pydf.kd)
        

if __name__ == '__main__':
    unittest.main()
