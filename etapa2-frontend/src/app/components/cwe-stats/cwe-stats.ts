import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CweStatsService } from '../../services/cwe-stats.service';
import { VulnerabilityService } from '../../services/vulnerability.service';
import { CweStats } from '../../models/cwe-stats.model';
import { Vulnerability } from '../../models/vulnerability.model';

@Component({
  selector: 'app-cwe-stats',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './cwe-stats.html',
})
export class CweStatsComponent implements OnInit {
  private cweService = inject(CweStatsService);
  private vulnService = inject(VulnerabilityService);

  stats = signal<CweStats[]>([]);
  search = signal('');
  selectedCwe = signal<string | null>(null);
  cvesByCwe = signal<Vulnerability[]>([]);
  severityFilter = signal<string | undefined>(undefined);

  filteredStats = computed(() => {
    const q = this.search().toLowerCase();
    return q ? this.stats().filter(s => s.cweId.toLowerCase().includes(q)) : this.stats();
  });

  readonly severities = [
    { label: 'Todas',    value: undefined },
    { label: 'CRITICAL', value: 'CRITICAL' },
    { label: 'HIGH',     value: 'HIGH' },
    { label: 'MEDIUM',   value: 'MEDIUM' },
    { label: 'LOW',      value: 'LOW' },
  ];

  filteredCves = computed(() => {
    const sev = this.severityFilter();
    const cves = this.cvesByCwe();
    if (!sev) return cves;
    return cves.filter(v => v.cvssV31BaseSeverity?.toUpperCase() === sev);
  });

  ngOnInit() {
    this.cweService.getAll().subscribe(s => this.stats.set(s));
  }

  selectCwe(cweId: string) {
    this.selectedCwe.set(cweId);
    this.severityFilter.set(undefined);
    this.vulnService.getByCwe(cweId).subscribe(v => this.cvesByCwe.set(v));
  }

  maxCount(): number {
    return this.stats()[0]?.cveCount ?? 1;
  }

  barWidth(count: number): string {
    return `${(count / this.maxCount()) * 100}%`;
  }

  severityClass(s: string): string {
    switch (s?.toUpperCase()) {
      case 'CRITICAL': return 'badge bg-danger';
      case 'HIGH':     return 'badge bg-warning text-dark';
      case 'MEDIUM':   return 'badge bg-info text-dark';
      case 'LOW':      return 'badge bg-success';
      default:         return 'badge bg-secondary';
    }
  }
}
