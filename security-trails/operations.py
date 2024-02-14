""" Copyright start
    MIT License
    Copyright (c) 2024 Fortinet Inc
  Copyright end """
import requests
from connectors.core.connector import get_logger, ConnectorError
logger = get_logger('security-trails')


class SecurityTrails(object):

    def __init__(self, config):
        self.server_url = config.get('server_url').strip()
        self.api_key = config.get('api_key')
        self.headers = {'accept': 'application/json', 'APIKEY': self.api_key}
        if not self.server_url.startswith('https://') and not self.server_url.startswith('http://'):
            self.server_url = 'https://{0}/'.format(self.server_url)

    def make_api_call(self, endpoint=None, method='GET', headers=None, health_check=False):
        url = self.server_url + endpoint
        logger.debug('API Service Endpoint: {0}'.format(url))
        if headers:
            self.headers.update(headers)
        try:
            logger.debug('Making a request with {0} method and {1} headers.'.format(method, self.headers))
            response = requests.request(method, url, headers=self.headers)
            if response.status_code in [200]:
                if health_check:
                    return response
                try:
                    logger.debug(
                        'Converting the response into JSON format after returning with status code: {0}'.format(
                            response.status_code))
                    response_data = response.json()
                    return {'status': response_data['status'] if 'status' in response_data else 'Success',
                            'data': response_data}
                except Exception as e:
                    response_data = response.content
                    logger.error('Failed with an error: {0}. The response details are: {1}'.format(e, response_data))
                    return {'status': 'Failure', 'data': response_data}
            else:
                logger.error('Failed with response {0}'.format(response))
                raise ConnectorError(
                    {'status': 'Failure', 'status_code': str(response.status_code), 'response': response})
        except Exception as e:
            logger.exception(str(e))
            raise ConnectorError(str(e))


def get_associated_ips(config, params):
    """
    Retrieves a list of all associated IPs for a company domain from securitytrails.
    :param config: config
    :param params: params
    :return: List of all associated IPs for a company domain from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/company/{0}/associated-ips'.format(params.get('domain'))
    return obj.make_api_call(endpoint=endpoint)


def get_domain_details(config, params):
    """
    Retrieves a list of current data about the given hostname,current statistics associated with a particular record from securitytrails.
    :param config: config
    :param params: params
    :return: List of current data about the given hostname,current statistics associated with a particular record from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/domain/{0}'.format(params.get('host'))
    return obj.make_api_call(endpoint=endpoint)


def get_subdomain_details(config, params):
    """
    Retrieves a list of all child and sibling subdomains for a given hostname from securitytrails.
    :param config: config
    :param params: params
    :return: List of all child and sibling subdomains for a given hostname  from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/domain/{0}/subdomains'.format(params.get('host'))
    return obj.make_api_call(endpoint=endpoint)


def get_domain_tags_details(config, params):
    """
    Retrieves a list of all tags for a given hostname from securitytrails.
    :param config: config
    :param params: params
    :return: List of all tags for a given hostname from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/domain/{0}/tags'.format(params.get('host'))
    return obj.make_api_call(endpoint=endpoint)


def get_domain_whois_details(config, params):
    """
    Retrieves a list of all the current WHOIS data about a given hostname with the stats merged together from securitytrails.
    :param config: config
    :param params: params
    :return: List of all the current WHOIS data about a given hostname with the stats merged together from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/domain/{0}/whois'.format(params.get('host'))
    return obj.make_api_call(endpoint=endpoint)


def get_whois_history(config, params):
    """
    Retrieves a list of all the current WHOIS data about a given hostname with the stats merged together from securitytrails.
    :param config: config
    :param params: params
    :return: List of all the current WHOIS data about a given hostname with the stats merged together from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/history/{0}/whois'.format(params.get('host'))
    return obj.make_api_call(endpoint=endpoint)


def get_associated_domains(config, params):
    """
    Retrieves a list of all specific historical information about the given hostname parameter from securitytrails.
    :param config: config
    :param params: params
    :return: List of all specific historical information about the given hostname parameter from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/domain/{0}/associated'.format(params.get('host'))
    return obj.make_api_call(endpoint=endpoint)


def get_ips_neighbors(config, params):
    """
    Retrieves a list of all the neighbors in any given IP level range and essentially allows you to explore closeby IP addresses from securitytrails.
    :param config: config
    :param params: params
    :return: List of all the neighbors in any given IP level range and essentially allows you to explore closeby IP addresses from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/ips/nearby/{0}'.format(params.get('ip_address'))
    return obj.make_api_call(endpoint=endpoint)


def get_whois_ips(config, params):
    """
    Fetch current IP information for a single IPv4 address from securitytrails.
    :param config: config
    :param params: params
    :return: Fetch current IP information for a single IPv4 address from securitytrails.
    """
    obj = SecurityTrails(config)
    endpoint = '/v1/ips/{0}/whois'.format(params.get('ip_address'))
    return obj.make_api_call(endpoint=endpoint)


def _check_health(config):
    try:
        obj = SecurityTrails(config)
        obj.make_api_call(endpoint='/v1/ping', health_check=True)
        return True
    except Exception as err:
        logger.exception('Health check failed with: {0}'.format(err))
        raise ConnectorError('Health check failed with: {0}'.format(err))


operations = {
    'get_associated_ips': get_associated_ips,
    'get_domain_details': get_domain_details,
    'get_subdomain_details': get_subdomain_details,
    'get_domain_tags_details': get_domain_tags_details,
    'get_domain_whois_details': get_domain_whois_details,
    'get_associated_domains': get_associated_domains,
    'get_whois_history': get_whois_history,
    'get_ips_neighbors': get_ips_neighbors,
    'get_whois_ips': get_whois_ips
}
