from typing import Dict, Any, Optional, List
from requests import get, post, patch, delete, put, Response, exceptions
from sys import exit
import datetime


class Nitra:
    def __init__(
        self,
        username: str,
        secret: str,
        base_url: str,
        ensure_connected: bool = True
    ):
        self.username = username
        self.secret = secret
        self.base_url = base_url
        if ensure_connected:
            res = self.ping()
            if res.status_code != 200:
                try:
                    json = res.json()
                    print(f'Unable to talk with backend.\nReceived status code {res.status_code}\nReceived json: {json}')
                    exit(1)
                except exceptions.JSONDecodeError:
                    print(f'Unable to talk with backend.\nReceived status code {res.status_code} with invalid json body')
                    exit(1)
    
    def req(
        self,
        endpoint: str,
        method: str = 'GET',
        body: Optional[Dict[str, Any]] = None
    ) -> Response:
        # define request method func
        request = get
        if method == 'POST':
            request = post
        elif method == 'PATCH':
            request = patch
        elif method == 'DELETE':
            request = delete
        elif method == 'PUT':
            request = put
        elif method != 'GET':
            raise Exception(f'Method "{method}" is not supported')

        # define headers
        headers = {
            'Authorization': f'Bearer {self.username}:{self.secret}',
            'Accept': 'application/json',
            'X-Nitra': 'OK'
        }

        # define payload
        payload = None
        if method != 'GET' and not (not body):
            payload = body

        # define url
        url = self.base_url + endpoint 

        # send request and return response
        response = request(url=url, json=payload, headers=headers)
        return response


    def ping(self) -> Response:
        return self.req('/ping')


    def delete_job_postings_by_source_id(
        self,
        source_ids: List[str]
    ) -> Response:
        body = {'source_ids': source_ids}
        return self.req(
            '/job_postings/by_source_ids',
            'DELETE',
            body
        )


    def delete_job_postings_by_uuid(
        self,
        ids: List[str]
    ) -> Response:
        body = {'ids': ids}
        return self.req(
            '/job_postings/by_uuids',
            'DELETE',
            body
        )


    def insert_job_postings(
        self,
        job_postings: List[dict]
    ) -> Response:
        
        for job_posting in job_postings:
            job_posting["id"] = str(job_posting["id"])
            job_posting["job_area_id"] = str(job_posting["job_area_id"])

        body = {'job_postings': job_postings}

        return self.req(
            '/job_postings/bulk_insert',
            'POST',
            body
        )

    def parse_date(
        self,
        d: Any
    ) -> Optional[str]:
        if type(d) == datetime.date:
            return d.isoformat()
        elif type(d) == datetime.datetime:
            return d.isoformat()
        elif type(d) == str:
            return d
        else:
            return None


    def update_job_postings(
        self,
        job_posting_patches: List[dict]
    ) -> Response:
        for patch in job_posting_patches:
            patch["id"] = str(patch["id"])
            if 'job_area_id' in patch:
                patch["job_area_id"] = str(patch["job_area_id"])
            if 'job_title_id' in patch:
                patch["job_title_id"] = str(patch["job_title_id"])
            if 'expiry_date' in patch:
                patch['expiry_date'] = self.parse_date(patch['expiry_date'])
            if 'date' in patch:
                patch['date'] = self.parse_date(patch['date'])
            if 'industry_code' in patch:
                patch['industry_code'] = str(patch['industry_code'])
            if 'esco_code' in patch:
                patch['esco_code'] = str(patch['esco_code'])
            if 'esco_code_short' in patch:
                patch['esco_code_short'] = str(patch['esco_code_short'])
            if 'zip' in patch:
                patch['zip'] = str(patch['zip'])

        body = {'job_postings': job_posting_patches}

        return self.req(
            '/job_postings/bulk_update',
            'PATCH',
            body
        )


    def insert_job_posting_skills(
        self,
        job_posting_skills: List[dict]
    ) -> Response:
        
        for jps in job_posting_skills:
            jps["skill_id"] = str(jps["skill_id"])
            jps["job_posting_id"] = str(jps["job_posting_id"])

        body = {'job_posting_skills': job_posting_skills}

        return self.req(
            '/job_posting_skills/bulk_insert',
            'POST',
            body
        )


    def get_skills(self) -> Response:
        return self.req(
            '/skills',
            'GET'
        )


    def get_job_areas(self) -> Response:
        return self.req(
            '/job_areas',
            'GET'
        )


if __name__ == '__main__':
    print('Nitra should not be executed. Import it instead')
    exit(1)
