import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CweStats } from '../models/cwe-stats.model';

@Injectable({ providedIn: 'root' })
export class CweStatsService {
  private http = inject(HttpClient);
  private url = 'http://localhost:8080/api/cwe-stats';

  getAll(): Observable<CweStats[]> {
    return this.http.get<CweStats[]>(this.url);
  }
}
