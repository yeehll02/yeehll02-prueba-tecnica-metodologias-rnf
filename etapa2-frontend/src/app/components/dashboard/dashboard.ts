import { Component, inject, signal, computed, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { StatsService } from '../../services/stats.service';
import { Stats } from '../../models/stats.model';
import { Timeline } from '../../models/timeline.model';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.html',
})
export class DashboardComponent implements OnInit {
  private service = inject(StatsService);

  stats    = signal<Stats | null>(null);
  timeline = signal<Timeline | null>(null);

  bars = computed(() => {
    const t = this.timeline();
    if (!t) return [];
    const entries = Object.entries(t.conteo_mensual);
    const max = Math.max(...entries.map(([, v]) => v));
    return entries.map(([month, count]) => ({
      month,
      count,
      height: `${Math.round((count / max) * 100)}%`,
      isPeak: t.meses_pico.includes(month),
    }));
  });

  ngOnInit() {
    this.service.get().subscribe(s => this.stats.set(s));
    this.service.getTimeline().subscribe(t => this.timeline.set(t));
  }

  sourcePercent(value: number): string {
    const total = this.stats()!.totalCves;
    return total ? `${Math.round((value / total) * 100)}%` : '0%';
  }

  severityPercent(value: number): string {
    const total = this.stats()!.totalCves;
    return total ? `${Math.round((value / total) * 100)}%` : '0%';
  }
}
