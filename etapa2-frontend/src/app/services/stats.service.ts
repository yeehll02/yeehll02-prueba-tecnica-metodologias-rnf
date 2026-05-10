import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Stats } from '../models/stats.model';
import { Timeline } from '../models/timeline.model';

@Injectable({ providedIn: 'root' })
export class StatsService {
  private http = inject(HttpClient);
  private base = 'http://localhost:8080/api/stats';

  get(): Observable<Stats> {
    return this.http.get<Stats>(this.base);
  }

  getTimeline(): Observable<Timeline> {
    return this.http.get<Timeline>(`${this.base}/timeline`);
  }
}
