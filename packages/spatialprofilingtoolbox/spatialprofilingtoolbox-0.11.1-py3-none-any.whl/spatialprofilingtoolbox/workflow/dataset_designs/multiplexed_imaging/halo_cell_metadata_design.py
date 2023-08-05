import pathlib
import os
from os.path import join
from os.path import exists
import re

import pandas as pd

from ....standalone_utilities.log_formats import colorized_logger

logger = colorized_logger(__name__)


class HALOCellMetadataDesign:
    """
    This class provides the schema necessary to interpret cell metadata manifests
    exported from the HALO software.
    """
    def __init__(self,
        elementary_phenotypes_file: str=None,
        compartments_file: str=None,
        **kwargs,
    ):
        self.elementary_phenotypes = pd.read_csv(
            elementary_phenotypes_file,
            keep_default_na=False,
        )
        if compartments_file is not None:
            self.compartments = open(compartments_file, 'rt').read().strip('\n').split('\n')

    @staticmethod
    def solicit_cli_arguments(parser):
        parser.add_argument(
            '--elementary-phenotypes-file',
            dest='elementary_phenotypes_file',
            type=str,
            required=True,
        )
        parser.add_argument(
            '--compartments-file',
            dest='compartments_file',
            type=str,
            required=True,
        )

    def get_FOV_column(self, table=None):
        """
        Returns:
            str:
                The column name for the column in the HALO-exported CSV which indicates
                the field of view in which the cell corresponding to a table record
                appears.
        """
        column = 'Image Location'
        if not table is None:
            if not column in table.columns:
                column = re.sub(' ', '_', column)
                if not column in table.columns:
                    raise ValueError('Could not find "%s" even with underscore replacement, among: %s' % (column, str(list(table.columns))))
        return column

    @staticmethod
    def get_cell_area_column():
        """
        :return: The name of the table column containing cell area values.
        :rtype: str
        """
        return 'Cell Area'

    def normalize_fov_descriptors(self, table):
        """
        Modifies field of view descriptor column of ``table`` *in-place*, sanitizes each
        according to the assumption that each value is a Windows-style path string
        for which only the file basename is needed.

        This was needed because in some datasets, field of view descriptors were not
        used consistently. Note that this function may be deprecated if a more rigorous
        data model is eventually enforced with respect to the field of view descriptor
        strings.

        :param table: Dataframe containing a field of view descriptor column.
        :type table: pandas.DataFrame
        """
        column = self.get_FOV_column(table=table)
        table[column] = table[column].apply(self.normalize_fov_descriptor)

    def normalize_fov_descriptor(self, fov):
        """
        Returns an normalized path string (file basename).

        :param fov: A field of view descriptor string to normalize (i.e. to put into
            normal form).
        :type fov: str

        :return: The normal form. Currently just the file basename, assuming that the
            original descriptor is a Windows-style file path string.
        :rtype: str
        """
        if r'\\' in fov:
            return pathlib.PureWindowsPath(fov).name
        else:
            return fov

    @staticmethod
    def get_cell_manifest_descriptor():
        return 'HALO software cell manifest'

    @staticmethod
    def validate_cell_manifest_descriptor(descriptor):
        return descriptor in [
            HALOCellMetadataDesign.get_cell_manifest_descriptor(),
            'simulated HALO-exported cell manifest',
        ]

    @staticmethod
    def get_compartment_column_name():
        return 'Classifier Label'

    @staticmethod
    def get_compartment_file_identifier():
        return 'Compartments list'

    def get_compartments(self):
        """
        Returns:
            list:
                A list of the expected compartment names (i.e. "Classifier Label"
                values). This method may need to be migrated to a more specific
                dataset design module, or else obtain its values from a separate
                metadata file, as it will potentially vary by dataset.
        """
        return self.compartments

    def get_elementary_phenotype_names(self):
        """
        Returns:
            list:
                A list of the phenotype or channel names, as they appear in the
                various header/column names in the HALO-exported CSV files.
        """
        return list(self.elementary_phenotypes['Name'])

    def get_box_limit_column_names(self):
        """
        Returns:
            list:
                [xmin, xmax, ymin, ymax]. The column names, in reference to the HALO-
                exported cell manifest CSV, indicating the bounding box for each cell.
        """
        xmin = 'XMin'
        xmax = 'XMax'
        ymin = 'YMin'
        ymax = 'YMax'
        return [xmin, xmax, ymin, ymax]

    def get_indicator_prefix(self, phenotype_name, metadata_file_column='Column header fragment prefix'):
        """
        Args:
            phenotype_name (str):
                One of the elementary phenotype names.
            metadata_file_column (str):
                The name of the column of the elementary phenotypes metadata file to
                search through.

        Returns:
            str:
                The prefix which appears in many CSV column names, for which these
                columns pertain to the given phenotype.
        """
        e = self.elementary_phenotypes
        row = e.loc[e['Name'] == phenotype_name].squeeze()
        value = row[metadata_file_column]
        return str(value)

    def get_cellular_sites(self):
        """
        Returns:
            list:
                The string names of the cellular sites pertinent to the HALO-exported
                CSV. (E.g. "Cytoplasm", "Nucleus", "Membrane".)
        """
        return ['Cytoplasm', 'Nucleus', 'Membrane']

    def get_intensity_column_names(self, with_sites=True):
        """
        Returns:
            list:
                All column names for columns in the HALO-exported cell manifest CSV for
                columns which are channel intensities along a given cellular site.
        """
        columns_by_elementary_phenotype = {}
        sites = self.get_cellular_sites()
        if not with_sites:
            sites = ['']
        for site in sites:
            for e in sorted(list(self.elementary_phenotypes['Name'])):
                parts = []
                prefix = self.get_indicator_prefix(e)
                infix = site
                suffix = 'Intensity'
                if site == '':
                    column = prefix + ' ' + suffix
                    key = e + ' ' + 'intensity'
                else:
                    column = prefix + ' ' + infix + ' ' + suffix
                    key = e + ' ' + site.lower() + ' ' + 'intensity'
                columns_by_elementary_phenotype[key] = column
        return columns_by_elementary_phenotype

    def munge_name(self, signature):
        """
        Args:
            signature (dict):
                The keys are typically phenotype names and the values are "+" or "-". If
                a key is not a phenotype name, it is presumed to be the exact name of
                one of the columns in the HALO-exported CSV. In this case the value
                should be an exact string of one of the cell values of this CSV.

        Returns:
            str:
                A de-facto name for the class delineated by this signature, obtained by
                concatenating key/value pairs in a standardized order.
        """
        keys = sorted(list(signature.keys()))
        feature_list = [key + signature[key] for key in signature]
        name = ''.join(feature_list)
        return name

    def get_pandas_signature(self, table, signature):
        """
        Args:
            table (pd.DataFrame):
                The HALO cell metadata dataframe, unprocessed.
            signature (dict):
                The keys are typically phenotype names and the values are "+" or "-". If
                a key is not a phenotype name, it is presumed to be the exact name of
                one of the columns in the HALO-exported CSV. In this case the value
                should be an exact string of one of the cell values of this CSV.

        Returns:
            pd.Series:
                The boolean series indicating the records in table that express the
                provided signature.
        """
        if signature is None:
            logger.error('Can not get subset with no information about signature (None).')
            return None
        if table is None:
            logger.error('Can not find subset of empty data; table is None.')
            return None
        fn = self.get_feature_name
        v = self.interpret_value_specification
        for key in signature.keys():
            feature_name = fn(key, table=table)
            if not feature_name in table.columns:
                logger.warning('Key "%s" was not among feature/column names: %s', feature_name, str(list(table.columns)))
                feature_name = re.sub(' ', '_', feature_name)
                if not feature_name in table.columns:
                    logger.error('Key "%s" was not among feature/column names: %s', feature_name, str(list(table.columns)))
        pandas_signature = self.non_infix_bitwise_AND([table[fn(key, table=table)] == v(value) for key, value in signature.items()])
        return pandas_signature

    def non_infix_bitwise_AND(self, args):
        """
        Args:
            args (list):
                A list of boolean lists/series of the same length.

        Returns:
            list:
                The component-wise boolean AND operation output.
        """
        accumulator = args[0]
        if len(args) > 1:
            for arg in args[1:len(args)]:
                accumulator = accumulator & arg
        return accumulator

    def get_feature_name(self, key, table=None):
        """
        Args:
            key (str):
                A phenotype/channel name (usually).

        Returns:
            str:
                The exact column name for the column in the HALO-exported CSV which
                indicates (boolean) thresholded positivity for the given phenotype.
                If the key is not a phenotype name, then the key is returned unchanged.
        """
        separator = ' '
        if not table is None:
            if '_'.join([self.get_indicator_prefix(key), 'Positive']) in table.columns:
                separator = '_'
        if key in self.get_elementary_phenotype_names():
            return separator.join([self.get_indicator_prefix(key), 'Positive'])
        else:
            return key

    def interpret_value_specification(self, value):
        """
        This function provides an abstraction layer between the table cell values as
        they actually appear in original data files and more semantic tokens in the
        context of signature definition.

        In the future this may need to be made column-specific.

        Args:
            value:
                Typically "+" or "-", but may be an arbitrary expected table cell value.

        Returns:
            The corresponding value as it is expected to appear as a table cell value
            in the HALO-exported CSV.
        """
        special_cases = {
            '+' : 1,
            '-' : 0,
        }
        if value in special_cases.keys():
            return special_cases[value]
        else:
            return value

    def get_compartmental_signature(self, table, compartment):
        """
        Args:
            table (pd.DataFrame):
                The HALO cell metadata dataframe, unprocessed.
            compartment (str):
                The name of a compartment to focus on.

        Returns:
            pd.Series:
                The boolean series indicating the records in table (i.e. cells) which
                should be regarded as part of the given compartment. This is currently
                just finding the records marked for this compartment, but more
                functionality may need to be modified for specific cases (e.g. involving
                additional knowledge of the expected characteristics of the
                compartment.)
        """
        signature = None

        if compartment in self.get_compartments():
            column = HALOCellMetadataDesign.get_compartment_column_name()
            if (not column in table.columns) and (self.get_compartments() == ['<any>']) and (compartment == '<any>'):
                signature = [True for i in range(table.shape[0])]
            else:
                signature = self.get_pandas_signature(table, {column : compartment})

        if signature is None:
            logger.error('Could not define compartment %s, from among %s', compartment, self.get_compartments())
            return [False for i in range(table.shape[0])]
        else:
            return signature

    def get_combined_intensity(self, table, elementary_phenotype):
        """
        Args:
            table (pd.DataFrame):
                The HALO cell metadata dataframe, unprocessed.
            elementary_phenotype (str):
                The name of a phenotype/channel.

        Returns:
            list:
                A list representation of the sum of the columns containing the
                intensities at each cellular site for the given phenotype.
        """
        intensity_column = self.get_intensity_column_name(elementary_phenotype)
        if intensity_column in table.columns:
            return table[intensity_column]
        prefix = self.get_indicator_prefix(elementary_phenotype)
        suffixes = [site + ' Intensity' for site in self.get_cellular_sites()]
        feature = [' '.join([prefix, suffix]) for suffix in suffixes]
        return list(table[feature[0]] + table[feature[1]] + table[feature[2]])

    def add_combined_intensity_column(self, table, elementary_phenotype):
        for phenotype in self.get_elementary_phenotype_names():
            column = self.get_intensity_column_name(phenotype)
            table[column] = self.get_combined_intensity(table, phenotype)

    def get_intensity_column_name(self, elementary_phenotype):
        """
        Currently only used for manually-created intensity column.
        """
        return self.get_indicator_prefix(elementary_phenotype) + ' Intensity'

