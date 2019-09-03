import {Injectable} from '@angular/core';

import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';

import {environment} from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class FireService {

    constructor(private http: HttpClient) {

    }

    searchFirePolygon(id, size): Observable<object> {
        return this.http.post('http://' + environment.host + ':' + environment.port + '/data/fire-with-id', JSON.stringify({
            id,
            size
        }));
    }

    searchSeparatedFirePolygon(id, size): Observable<object> {
        return this.http.post('http://${environment.host}:${environment.port}/data/fire-with-id-seperated', JSON.stringify({
            id, size,
        })).pipe(map(data => {
            return {type: 'FeatureCollection', features: data};
        }));
    }
}
