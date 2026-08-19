"""probe for weaviate/weaviate#11741  Tenant creation accepts empty string for activityStatus
version: 1.38.0 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestTenant')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'TestTenant', 'multiTenancyConfig': {'enabled': True},
    })
    emit('c1', http_status=st1, obs='POST schema TestTenant (multi-tenancy enabled): got HTTP %s' % st1)
    # control: valid ACTIVE tenant should be accepted
    st2, b2, _ = http('POST', BASE + '/schema/TestTenant/tenants',
                      [{'name': 'tenant_valid', 'activityStatus': 'ACTIVE'}])
    emit('c2', http_status=st2, obs='CONTROL create tenant activityStatus="ACTIVE": got HTTP %s' % st2)
    # bug: empty activityStatus accepted 200
    st3, b3, _ = http('POST', BASE + '/schema/TestTenant/tenants',
                      [{'name': 'tenant_empty', 'activityStatus': ''}])
    emit('c3', http_status=st3,
         obs='POST tenant activityStatus="": got HTTP %s (bug: 200 created tenant with empty activityStatus; correct: 422)' % st3)
    print('probe_weaviate_11741 done')

if __name__ == '__main__':
    main()
