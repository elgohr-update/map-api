from map.config import API_PREFIX


def test_revoke_access_token(client, admin_headers):
    resp = client.delete('/auth/revoke_access', headers=admin_headers)
    assert resp.status_code == 200

    resp = client.get(f'{API_PREFIX}/users', headers=admin_headers)
    assert resp.status_code == 401


def test_revoke_refresh_token(client, admin_refresh_headers):
    resp = client.delete('/auth/revoke_refresh', headers=admin_refresh_headers)
    assert resp.status_code == 200

    resp = client.post('/auth/refresh', headers=admin_refresh_headers)
    assert resp.status_code == 401