"""
A script that converts an Excel file into the request format.

The Excel file has to be in one of the supported formats, which examples can
be found in the data_formats directory.

To run the script on a supported Excel file, do:

    $ python excel_to_request_format.py <Excel file path> <output file path>

This prints out the request format of the excel file into `<output file path>`.

To see all the possible arguments, run:

    $ python excel_to_request_format.py --help
"""
import argparse
import json
from contextlib import suppress

import pathlib
import xlrd
import openpyxl

from data_formats import request_format


class FormatUnsupportedError(Exception):
    """The Excel format is not supported."""


def convert(excel_file):
    """
    Convert the excel file into the request format.

    Args:
        excel_file: The path to the excel file

    Returns:
        The request format as a Python dict
    """
    last_exception = None
    for subclass in Converter.__subclasses__():
        converter = subclass(excel_file)

        # Assume that any errors are due to the format and nothing else
        try:
            return converter.convert()
        except Exception as exc:
            last_exception = exc

    # Found no converter for the excel file
    raise FormatUnsupportedError from last_exception


class Converter:
    """
    The SuperClass for all Excel-to-request-format converters.

    All a subclass needs to do is implement all the abstract methods and the
    superclass does the rest of the work.
    """

    def __init__(self, excel_file):
        """
        Create a new converter for the Excel file.

        Args:
            excel_file: The path to the excel file
        """
        self._excel_file = excel_file

        self._file_extension = pathlib.Path(excel_file).suffix
        if self._file_extension not in [".xls", ".xlsx"]:
            raise FormatUnsupportedError(f'File must be of format ".xls" or ".xlsx".')
        
        if self._file_extension=='.xls':
            self._file = xlrd.open_workbook(excel_file)
        else:
            self._file = openpyxl.load_workbook(excel_file)

    def _get_columns(self, sheet_name, start=0):
        if self._file_extension=='.xls':
            sheet = self._file.sheet_by_name(sheet_name) # xlrd style
            for colx in range(start, sheet.ncols):
                yield sheet.col_values(colx)[1:]   # ipysheet didn't allow editable column names,
                                                    # so added an index row to sheets and slicing it off here
        else:
            sheet = self._file[sheet_name] # openpyxl style
            for i,colx in enumerate(sheet.columns): # Different writing with openpyxl
                if i<start: continue; # Skip until start line is reached (generator can't skip earlier)
                
                column = [c.value if c.value is not None else '' for c in colx]
                if all([c=='' for c in column]): # openpyxl captures rows and rows of useless NaN.
                    continue;
                yield column[1:]


    def _get_general(self):
        raise NotImplementedError

    def _get_capacities(self):
        raise NotImplementedError

    def _get_streams(self):
        raise NotImplementedError

    def _get_converters(self):
        raise NotImplementedError

    def _get_storages(self):
        raise NotImplementedError

    def _get_system_types(self):
        raise NotImplementedError

    def _get_time_series(self):
        raise NotImplementedError

    def _get_network_nodes(self):
        raise NotImplementedError

    def _get_network_links(self):
        raise NotImplementedError

    def convert(self):
        """
        Convert the file into the request format.

        Returns:
            The request format
        """
        request = {
            'version': '0.1.0',
            'general': self._get_general(),
            'capacities': self._get_capacities(),
            'streams': self._get_streams(),
            'converters': self._get_converters(),
            'storages': self._get_storages(),
            'system_types': self._get_system_types(),
            'time_series': self._get_time_series(),
            # 'network': {
            #     'nodes': self._get_network_nodes(),
            #     'links': self._get_network_links(),
            # }
        }

        return request


class _NewFormatConverter(Converter):
    def _get_columns(self, sheet_name, start=1):
        # The first column holds all the names for the rows
        return super()._get_columns(sheet_name, start=start)

    def _get_general(self):
        if self._file_extension=='.xls': # xlrd stype
            sheet = self._file.sheet_by_name('General')

            return {
                'interest_rate': float(sheet.cell(2,1).value),  # cell(2, 1) in xlrd as skip 1st row and col 
            }
        else: # openpyxl style
            sheet = self._file['General']

            return {
                'interest_rate': float(sheet.cell(3,2).value),  # true location cell(3,2) in openpyxl
            }

    def _get_capacities(self):
        capacities = []
        for column in self._get_columns('Capacities'):
            (name, units, item_type, options, lower_bound,
             upper_bound) = column

            if name not in ['#', '']:
                capacity = {
                    'name': name,
                    'units': units,
                    'type': item_type,
                }

                if options:
                    if item_type == 'List':
                        options = [int(x) for x in options.split(',')]

                    capacity['options'] = options

                if lower_bound != '' or upper_bound != '':
                    capacity['bounds'] = {}

                    with suppress(ValueError):
                        capacity['bounds']['lower'] = int(lower_bound)

                    with suppress(ValueError):
                        capacity['bounds']['upper'] = int(upper_bound)

                capacities.append(capacity)

        return capacities

    def _get_streams(self):
        streams = []
        for column in self._get_columns('Streams'):
            (name, importable, exportable, timeseries, price, export_price, co2, co2credit) = column

            if name not in ['#', '']:
                with suppress(ValueError):
                    name = str(name)

                with suppress(ValueError):
                    importable = int(importable)

                with suppress(ValueError):
                    exportable = int(exportable)

                with suppress(ValueError):
                    timeseries = str(timeseries)

                with suppress(ValueError):
                    price = float(price)

                with suppress(ValueError):
                    export_price = float(export_price)

                with suppress(ValueError):
                    co2 = float(co2)

                with suppress(ValueError):
                    co2credit = float(co2credit)


                stream = {
                    'name': name,
                    'importable': importable,
                    'exportable': exportable,
                    'timeseries': timeseries,
                    'price': price,
                    'export_price': export_price,
                    'co2': co2,
                    'co2_credit': co2credit
                }

                streams.append(stream)

        return streams

    def _get_converters(self):
        converters = []
        for column in self._get_columns('Converters'):
            (name, capacity, fixed_capital_cost, capital_cost,
             annual_maintenance_cost, usage_maintenance_cost, efficiency,
             lifetime, output_ratio, min_load, inputs, outputs) = column

            if name not in ['#', '']:
                converter = {
                    'name': name.strip(),
                    'efficiency': float(efficiency),
                }

                with suppress(ValueError):
                    converter['fixed_capital_cost'] = float(fixed_capital_cost)

                if capacity is not None:
                    try:
                        capacity = float(capacity)
                    except ValueError:
                        # References a capacity in the capacities
                        capacity = str(capacity)

                    converter['capacity'] = capacity

                with suppress(ValueError):
                    converter['capital_cost'] = float(capital_cost)

                with suppress(ValueError):
                    annual_maintenance_cost = float(annual_maintenance_cost)
                    converter['annual_maintenance_cost'] = annual_maintenance_cost

                with suppress(ValueError):
                    usage_maintenance_cost = float(usage_maintenance_cost)
                    converter['usage_maintenance_cost'] = usage_maintenance_cost

                with suppress(ValueError):
                    converter['lifetime'] = float(lifetime)

                with suppress(ValueError):
                    converter['output_ratio'] = float(output_ratio)

                with suppress(ValueError):
                    converter['min_load'] = float(min_load)

                if inputs:
                    converter['inputs'] = [in_.strip()
                                           for in_ in inputs.split(',')]

                if outputs:
                    converter['outputs'] = [output.strip()
                                            for output in outputs.split(',')]

                converters.append(converter)

        return converters

    def _get_storages(self):
        storages = []
        for column in self._get_columns('Storages'):
            (name, stream, capacity, cost, annual_maintenance_cost, fixed_capital_cost, lifetime, charge_efficiency,
             discharge_efficiency, decay, max_charge, max_discharge,
             min_state) = column

            if name not in ['#', '']:
                storage = {
                    'name': name,
                    'stream': stream,
                    'cost': float(cost),
                    'lifetime': float(lifetime),
                    'charge_efficiency': float(charge_efficiency),
                    'discharge_efficiency': float(discharge_efficiency),
                    'decay': float(decay),
                    'max_charge': float(max_charge),
                    'max_discharge': float(max_discharge),
                    'min_state': float(min_state),
                }

                try:
                    capacity = int(capacity)
                except ValueError:
                    # References a capacity
                    capacity = str(capacity)
                storage['capacity'] = capacity

                with suppress(ValueError):
                    annual_maintenance_cost = float(annual_maintenance_cost)
                    storage['annual_maintenance_cost'] = annual_maintenance_cost

                with suppress(ValueError):
                    fixed_capital_cost = float(fixed_capital_cost)
                    storage['fixed_capital_cost'] = fixed_capital_cost

                storages.append(storage)

        return storages

    def _get_system_types(self):
        system_types = []
        for column in self._get_columns('System types'):
            (name, *technologies) = column

            if name not in ['#', '']:
                technologies = [tech for tech in technologies
                                if tech]

                system_type = {
                    'name': name,
                    'technologies': technologies
                }
                system_types.append(system_type)

        return system_types

    def _get_time_series(self):
        time_series_list = []
        for column in self._get_columns('Time series'):
            (series_id, series_type, stream, node, units, source,
             *rest) = column

            if series_id not in ['#', '']:
                data = rest[3:]  # Remove empty lines

                time_series = {
                    'id': series_id,
                    'type': series_type,
                    'stream': stream,
                    'units': units,
                    'data': [float(d) for d in data if d is not None and d != ''],
                }

                if source:
                    time_series['source'] = source

                if node:
                    time_series['node'] = int(node)

                time_series_list.append(time_series)

        return time_series_list

def parse_args():
    """Parses the command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Converts an excel file into a EHub Request format.')
    parser.add_argument(
        'excel_file', help='The excel file to convert',
    )
    parser.add_argument(
        'output_file', help='The file to output the results to',
    )
    return parser.parse_args()


def main():
    """The function that runs the script."""
    args = parse_args()

    content = convert(args.excel_file)

    # Ensure the format is correct
    request_format.validate(content)

    with open(args.output_file, 'w') as file:
        file.write(json.dumps(content))

if __name__ == "__main__":
    main()
