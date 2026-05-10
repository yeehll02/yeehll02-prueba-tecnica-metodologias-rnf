import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CpeRanking } from '../models/cpe-ranking.model';

@Injectable({ providedIn: 'root' })
export class CpeRankingService {
  private http = inject(HttpClient);
  private url = 'http://localhost:8080/api/cpe-ranking';

  getAll(): Observable<CpeRanking[]> {
    return this.http.get<CpeRanking[]>(this.url);
  }
}
