from functools import lru_cache

import numpy as np
import pandas as pd

from wmb.files import *
from ..annot import BROADTENXCellAnnotation
from ..genome import mm10


class BROAD(AutoPathMixIn):
    def __init__(self):
        self.BROAD_TENX_SAMPLE_METADATA_PATH = BROAD_TENX_SAMPLE_METADATA_PATH

        self.BROAD_TENX_ZARR_PATH = BROAD_TENX_ZARR_PATH
        self.BROAD_TENX_V2_ZARR_PATH = BROAD_TENX_V2_ZARR_PATH

        self.BROAD_TENX_OUTLIER_IDS_PATH = BROAD_TENX_OUTLIER_IDS_PATH

        self.BROAD_TENX_CELL_TYPE_ANNOTATION_PATH = BROAD_TENX_CELL_TYPE_ANNOTATION_PATH
        self.BROAD_TENX_CELL_TYPE_V2_ANNOTATION_PATH = BROAD_TENX_CELL_TYPE_V2_ANNOTATION_PATH

        self.BROAD_TENX_GENE_MAP_PATH = BROAD_TENX_GENE_MAP_PATH

        self.BROAD_TENX_GENE_CHUNK_ZARR_PATH = BROAD_TENX_GENE_CHUNK_ZARR_PATH
        self.BROAD_TENX_GENE_CHUNK_V2_ZARR_PATH = BROAD_TENX_GENE_CHUNK_V2_ZARR_PATH

        # cluster aggregate zarr path
        self.BROAD_TENX_CLUSTER_L4_SUM_ZARR_PATH = BROAD_TENX_CLUSTER_L4_SUM_ZARR_PATH
        self.BROAD_TENX_CLUSTER_L4Region_SUM_ZARR_PATH = BROAD_TENX_CLUSTER_L4Region_SUM_ZARR_PATH

        self._gene_zarr = None
        self._cell_million_reads = None
        self._gene_index = None

        # validate path or auto change prefix
        self._check_file_path_attrs()
        return

    def get_tenx_gene_map(self):
        return pd.read_csv(self.BROAD_TENX_GENE_MAP_PATH, index_col=0, header=0).squeeze()

    def get_tenx_sample_metadata(self):
        df = pd.read_csv(self.BROAD_TENX_SAMPLE_METADATA_PATH, index_col=0)
        df.index.name = 'sample'
        return df

    def get_tenx_outlier_ids(self):
        ids = pd.read_csv(self.BROAD_TENX_OUTLIER_IDS_PATH, index_col=0, header=None).index
        ids.name = 'cell'
        return ids

    def get_tenx_annot(self, version='v2'):
        if version == 'v2':
            path = self.BROAD_TENX_CELL_TYPE_V2_ANNOTATION_PATH
        else:
            path = self.BROAD_TENX_CELL_TYPE_ANNOTATION_PATH
        return BROADTENXCellAnnotation(path,
                                       self.get_tenx_sample_metadata(),
                                       version=version)

    def _open_gene_chunk_zarr(self, version):
        import xarray as xr
        if version == 'v2':
            path = self.BROAD_TENX_GENE_CHUNK_V2_ZARR_PATH
        else:
            path = self.BROAD_TENX_GENE_CHUNK_ZARR_PATH
        self._gene_zarr = xr.open_zarr(path)
        self._cell_million_reads = self._gene_zarr['umi_count'].to_pandas()
        self._cell_million_reads /= 1000000
        self._gene_index = self._gene_zarr.get_index('gene')
        return

    @lru_cache(maxsize=200)
    def get_tenx_gene_data(self, gene, normalize=True, log=True, version='v2'):
        if self._gene_zarr is None:
            self._open_gene_chunk_zarr(version=version)

        # check if gene is gene name:
        if version == 'v2':
            if gene not in self._gene_index:
                gene = mm10.gene_name_to_id(gene, allow_nan=False)
        else:
            if gene not in self._gene_index:
                # gene is gene name
                gene = mm10.gene_id_to_name(gene, allow_nan=False)

        # raw counts
        gene_data = self._gene_zarr['gene_da_fc'].sel(
            gene=gene).to_pandas()

        # normalize to CPM
        if normalize:
            gene_data /= self._cell_million_reads

        # log transform
        if log:
            gene_data = np.log1p(gene_data)
        return gene_data


broad = BROAD()
