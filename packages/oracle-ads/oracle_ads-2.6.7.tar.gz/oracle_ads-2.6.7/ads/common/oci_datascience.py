#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021, 2022 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import oci.data_science
from ads.common.oci_mixin import OCIModelMixin


class OCIDataScienceMixin(OCIModelMixin):
    @classmethod
    def init_client(cls, **kwargs) -> oci.data_science.DataScienceClient:
        return cls._init_client(client=oci.data_science.DataScienceClient, **kwargs)

    @property
    def client(self) -> oci.data_science.DataScienceClient:
        return super().client


class DSCNotebookSession(OCIDataScienceMixin, oci.data_science.models.NotebookSession):
    """Represents a data science notebook session

    To get the information of an existing notebook session:
    >>> notebook = DSCNotebookSession.from_ocid(NOTEBOOK_OCID)
    Get the name of the notebook session
    >>> notebook.display_name
    Get the subnet ID of the notebook session
    >>> notebook.notebook_session_configuration_details.subnet_id
    """
