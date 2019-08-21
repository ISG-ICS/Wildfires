import {Injectable} from '@angular/core';

import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class FireService {

    constructor(private http: HttpClient) {

    }

    searchFirePolygon(id, size): Observable<object> {
        return this.http.post('http://0.0.0.0:2334/data/fire-with-id', JSON.stringify({id, size}));
    }

    searchSeparatedFirePolygon(id, size): Observable<object> {
        return this.http.post('http://0.0.0.0:2334/data/fire-with-id-seperated', JSON.stringify({
            id, size,
        })).pipe(map(data => {
            return {type: 'FeatureCollection', features: data};
        }));
    }
}
