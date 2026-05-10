import { Component, inject, signal, effect, untracked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { VulnerabilityService } from '../../services/vulnerability.service';
import { VulnerabilityPage } from '../../models/vulnerability.model';

@Component({
  selector: 'app-vulnerabilities',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './vulnerabilities.html',
})
export class VulnerabilitiesComponent {
  private service = inject(VulnerabilityService);

  page = signal<VulnerabilityPage | null>(null);
  currentPage = signal(0);
  pageSize = 20;
  source        = signal<string | undefined>(undefined);
  severity      = signal<string | undefined>(undefined);
  search        = signal('');
  reloadTrigger = signal(0);

  readonly sources = [
    { label: 'Todos',  value: undefined },
    { label: 'CISA',   value: 'cisa' },
    { label: 'Nuclei', value: 'nuclei' },
  ];
  readonly severities = [
    { label: 'Todas',    value: undefined },
    { label: 'CRITICAL', value: 'CRITICAL' },
    { label: 'HIGH',     value: 'HIGH' },
    { label: 'MEDIUM',   value: 'MEDIUM' },
    { label: 'LOW',      value: 'LOW' },
  ];

  constructor() {
    effect(() => {
      const p   = this.currentPage();
      const src = this.source();
      const sev = this.severity();
      const q   = this.search();
      this.reloadTrigger();

      untracked(() => {
        this.service.getAll(p, this.pageSize, src, sev, q || undefined)
          .subscribe(result => this.page.set(result));
      });
    });
  }

  setSearch(value: string) {
    this.search.set(value);
    this.currentPage.set(0);
  }

  setSource(value: string | undefined) {
    this.source.set(value);
    this.currentPage.set(0);
  }

  setSeverity(value: string | undefined) {
    this.severity.set(value);
    this.currentPage.set(0);
  }

  goTo(p: number) {
    this.currentPage.set(p);
  }

  delete(id: string) {
    if (confirm(`¿Eliminar ${id}?`)) {
      this.service.delete(id).subscribe(() => {
        if (this.currentPage() === 0) {
          this.reloadTrigger.update(n => n + 1);
        } else {
          this.currentPage.set(0);
        }
      });
    }
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
