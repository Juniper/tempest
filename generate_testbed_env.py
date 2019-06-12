import yaml,os

with open('/contrail-test/contrail_test_input.yaml', 'r') as fd:
    configs = yaml.load(fd)

contrail_configs = configs.get('contrail_configuration') or {}
orchestrator_configs = configs.get('orchestrator_configuration') or {}

keystone_service_host = contrail_configs.get('KEYSTONE_AUTH_HOST')
api_server_ip = contrail_configs.get('CONFIG_API_VIP') or ''
api_server_host_string = 'root@'+api_server_ip

# openstack related configs
keystone_configs = orchestrator_configs.get('keystone') or {}
keystone_version = keystone_configs.get('version') or 'v3'
admin_username = keystone_configs.get('username') or \
                          os.getenv('OS_USERNAME', 'admin')
admin_password = keystone_configs.get('password') or \
                          os.getenv('OS_PASSWORD', 'c0ntrail123')
admin_tenant = keystone_configs.get('tenant') or \
                        os.getenv('OS_TENANT_NAME', 'admin')
admin_domain = keystone_configs.get('domain') or \
                        os.getenv('OS_DOMAIN_NAME', 'default')
region_name = keystone_configs.get('region') or \
                       os.getenv('OS_REGION_NAME', 'RegionOne')

internal_vip = api_server_ip if api_server_ip else orchestrator_configs.get('internal_vip') or ''
external_vip = orchestrator_configs.get('external_vip') or internal_vip

#test related configs
test_configs = configs.get('test_configuration') or {}
public_network_subnet = test_configs.get('public_subnet') or \
                            os.getenv('PUBLIC_NETWORK_SUBNET', '')
public_network_rt = test_configs.get('public_rt') or \
                            os.getenv('PUBLIC_NETWORK_RT', '')

fh = open('testbed_env','w')
fh.write('export KEYSTONE_SERVICE_HOST=%s\n' % (keystone_service_host))
fh.write('export API_SERVER_IP=%s\n' % (internal_vip))
fh.write('export API_SERVER_HOST_STRING=%s\n' % (api_server_host_string))
fh.write('export API_SERVER_HOST_PASSWORD=%s\n' % ('c0ntrail123'))
fh.write('export PUBLIC_NETWORK_SUBNET=%s\n' % (public_network_subnet))
fh.write('export PUBLIC_NETWORK_RT=%s\n' % (public_network_rt))
fh.write('export OS_AUTH_VERSION=%s\n' % (keystone_version))
fh.write('export OS_PASSWORD=%s\n' % (admin_password))
fh.write('export OS_USERNAME=%s\n' % (admin_username))
fh.write('export OS_TENANT_NAME=%s\n' % (admin_tenant))
fh.close()

