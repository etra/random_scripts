import fire
import ipaddress
from pathlib import Path
import geoip2.database
from geoip2.models import Country
import json
from dotenv import dotenv_values

# This reader object should be reused across lookups as creation of it is
# expensive.


class Extractor(object):
    """A simple calculator class."""

    ips = None
    file_path = None
    config = None

    def __init__(self):
        self.ips = []
        self.config = dotenv_values(".env")

    def _iterate_ip_range(self, start_ip, end_ip):
        # Convert start and end IP addresses to IPv4Address objects
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        
        # Check if the start IP is less than or equal to the end IP
        if start > end:
            raise ValueError("Start IP must be less than or equal to End IP.")
        
        # Iterate over the range of IP addresses
        for ip_int in range(int(start), int(end) + 1):
            yield str(ipaddress.IPv4Address(ip_int))

    def _write_to_file(self):
        path = Path(self.file_path)
        path.parent.mkdir(exist_ok=True)
        with open(path, mode='w') as fh:
            fh.writelines(json.dumps(line) + '\n' for line in self.ips)

    def _add_to_ips(self, ip):
        try:
            response = dict()
            response['ip'] = ip
            response['geo_country'] = self.geoip_country(ip)
            response['geo_city'] = self.geoip_city(ip)
            response['geo_asn'] = self.geoip_asn(ip)

            self.ips.append(response)
        except Exception as e:
            raise Exception(f"Error processing IP: {ip}. Error: {e}") from e
    
    def _reset_ips(self):
        self.ips = []

    def geoip_country(self, ip):
        with geoip2.database.Reader(self.config['GEOIP_COUNTRY']) as reader:
            response: Country = reader.country(ip)
            return response.raw
    
    def geoip_city(self, ip):
        with geoip2.database.Reader(self.config['GEOIP_CITY']) as reader:
            response = reader.city(ip)
            return response.raw

    def geoip_asn(self, ip):
        with geoip2.database.Reader(self.config['GEOIP_ASN']) as reader:
            response = reader.asn(ip)
            return response.raw

    def run(self, destination_prefix: str, start:str, end: str):
        for ip in self._iterate_ip_range(start, end):
            new_file_path = f"./{destination_prefix}/{ip.split('.')[0]}_{ip.split('.')[1]}_{ip.split('.')[2]}.json"
            if self.file_path is None:
                self.file_path = new_file_path

            if self.file_path == new_file_path:
                self._add_to_ips(ip)
            else:
                self._write_to_file()
                self._reset_ips()
                self._add_to_ips(ip)
                self.file_path = new_file_path
        
        self._write_to_file()



if __name__ == '__main__':
    fire.Fire(Extractor)
