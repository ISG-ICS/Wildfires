import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class SearchService {

    searchDataLoaded = new EventEmitter();

    constructor(private http: HttpClient) {

    }

    getSearch(userInput): Observable<object> {
        return this.http.get<object>('http://127.0.0.1:5000/search', {params: new HttpParams().set('keyword', userInput)});
    }

}

