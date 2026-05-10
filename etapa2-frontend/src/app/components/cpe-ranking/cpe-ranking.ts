import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CpeRankingService } from '../../services/cpe-ranking.service';
import { VulnerabilityService } from '../../services/vulnerability.service';
import { CpeRanking } from '../../models/cpe-ranking.model';
import { Vulnerability } from '../../models/vulnerability.model';

@Component({
  selector: 'app-cpe-ranking',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './cpe-ranking.html',
})
export class CpeRankingComponent implements OnInit {
  private cpeService = inject(CpeRankingService);
  private vulnService = inject(VulnerabilityService);

  ranking = signal<CpeRanking[]>([]);
  search = signal('');
  selectedCpe = signal<string | null>(null);
  cvesByCpe = signal<Vulnerability[]>([]);
  severityFilter = signal<string | undefined>(undefined);

  filteredRanking = computed(() => {
    const q = this.search().toLowerCase();
    return q ? this.ranking().filter(r => r.vendorProduct.toLowerCase().includes(q)) : this.ranking();
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
    const cves = this.cvesByCpe();
    if (!sev) return cves;
    return cves.filter(v => v.cvssV31BaseSeverity?.toUpperCase() === sev);
  });

  ngOnInit() {
    this.cpeService.getAll().subscribe(r => this.ranking.set(r));
  }

  selectCpe(vendorProduct: string) {
    this.selectedCpe.set(vendorProduct);
    this.severityFilter.set(undefined);
    this.vulnService.getByCpe(vendorProduct).subscribe(v => this.cvesByCpe.set(v));
  }

  maxCount(): number {
    return this.ranking()[0]?.cveCount ?? 1;
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
