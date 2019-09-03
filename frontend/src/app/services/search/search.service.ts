import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class SearchService {

    searchDataLoaded = new EventEmitter();

    constructor(private http: HttpClient) {

    }

    getSearch(userInput): Observable<object> {
        return this.http.get<object>('http://' + environment.host + ':' + environment.port + '/search',
            {params: new HttpParams().set('keyword', userInput)});
    }

}

