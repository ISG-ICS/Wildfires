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
        return this.http.post('http://127.0.0.1:5000/data/fire-with-id', JSON.stringify({
            id: id,
            size: size,
        }));
    }

    searchSeparatedFirePolygon(id, size): Observable<object> {
        return this.http.post('http://127.0.0.1:5000/data/fire-with-id-seperated', JSON.stringify({
            id: id,
            size: size,
        })).pipe(map(data => {
            console.log('fire-polygon DATA ', data);
            return {type: 'FeatureCollection', features: data};
        }));
    }
}
