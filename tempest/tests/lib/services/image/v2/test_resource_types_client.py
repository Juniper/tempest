# Copyright 2016 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.lib.services.image.v2 import resource_types_client
from tempest.tests.lib import fake_auth_provider
from tempest.tests.lib.services import base


class TestResourceTypesClient(base.BaseServiceTest):
    FAKE_LIST_RESOURCETYPES = {
        "resource_types": [
            {
                "created_at": "2014-08-28T18:13:04Z",
                "name": "OS::Glance::Image",
                "updated_at": "2014-08-28T18:13:04Z"
            },
            {
                "created_at": "2014-08-28T18:13:04Z",
                "name": "OS::Cinder::Volume",
                "updated_at": "2014-08-28T18:13:04Z"
            },
            {
                "created_at": "2014-08-28T18:13:04Z",
                "name": "OS::Nova::Flavor",
                "updated_at": "2014-08-28T18:13:04Z"
            },
            {
                "created_at": "2014-08-28T18:13:04Z",
                "name": "OS::Nova::Aggregate",
                "updated_at": "2014-08-28T18:13:04Z"
            },
            {
                "created_at": "2014-08-28T18:13:04Z",
                "name": u"\u2740(*\xb4\u25e1`*)\u2740",
                "updated_at": "2014-08-28T18:13:04Z"
            }
        ]
    }

    FAKE_CREATE_RESOURCE_TYPE_ASSOCIATION = {
        "created_at": "2020-03-07T18:20:44Z",
        "name": "OS::Glance::Image",
        "prefix": "hw:",
        "updated_at": "2020-03-07T18:20:44Z"
    }

    FAKE_LIST_RESOURCE_TYPE_ASSOCIATION = {
        "resource_type_associations": [
            {
                "created_at": "2020-03-07T18:20:44Z",
                "name": "OS::Nova::Flavor",
                "prefix": "hw:"
            },
            {
                "created_at": "2020-03-07T18:20:44Z",
                "name": "OS::Glance::Image",
                "prefix": "hw_"
            }
        ]
    }

    def setUp(self):
        super(TestResourceTypesClient, self).setUp()
        fake_auth = fake_auth_provider.FakeAuthProvider()
        self.client = resource_types_client.ResourceTypesClient(fake_auth,
                                                                'image',
                                                                'regionOne')

    def _test_list_resource_types(self, bytes_body=False):
        self.check_service_client_function(
            self.client.list_resource_types,
            'tempest.lib.common.rest_client.RestClient.get',
            self.FAKE_LIST_RESOURCETYPES,
            bytes_body)

    def _test_create_resource_type_association(self, bytes_body=False):
        self.check_service_client_function(
            self.client.create_resource_type_association,
            'tempest.lib.common.rest_client.RestClient.post',
            self.FAKE_CREATE_RESOURCE_TYPE_ASSOCIATION,
            bytes_body, status=201,
            namespace_id="OS::Compute::Hypervisor",
            name="OS::Glance::Image", prefix="hw_",
            )

    def _test_list_resource_type_association(self, bytes_body=False):
        self.check_service_client_function(
            self.client.list_resource_type_association,
            'tempest.lib.common.rest_client.RestClient.get',
            self.FAKE_LIST_RESOURCE_TYPE_ASSOCIATION,
            bytes_body,
            namespace_id="OS::Compute::Hypervisor",
            )

    def test_list_resource_types_with_str_body(self):
        self._test_list_resource_types()

    def test_list_resource_types_with_bytes_body(self):
        self._test_list_resource_types(bytes_body=True)

    def test_delete_resource_type_association(self):
        self.check_service_client_function(
            self.client.delete_resource_type_association,
            'tempest.lib.common.rest_client.RestClient.delete',
            {}, status=204,
            namespace_id="OS::Compute::Hypervisor",
            resource_name="OS::Glance::Image",
            )

    def test_create_resource_type_association_with_str_body(self):
        self._test_create_resource_type_association()

    def test_create_resource_type_association_with_bytes_body(self):
        self._test_create_resource_type_association(bytes_body=True)

    def test_list_resource_type_association_with_str_body(self):
        self._test_list_resource_type_association()

    def test_list_resource_type_association_with_bytes_body(self):
        self._test_list_resource_type_association(bytes_body=True)
