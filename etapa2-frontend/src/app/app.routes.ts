import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard';
import { VulnerabilitiesComponent } from './components/vulnerabilities/vulnerabilities';
import { VulnerabilityDetailComponent } from './components/vulnerability-detail/vulnerability-detail';
import { VulnerabilityFormComponent } from './components/vulnerability-form/vulnerability-form';
import { CweStatsComponent } from './components/cwe-stats/cwe-stats';
import { CpeRankingComponent } from './components/cpe-ranking/cpe-ranking';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'vulnerabilities', component: VulnerabilitiesComponent },
  { path: 'vulnerabilities/new', component: VulnerabilityFormComponent },
  { path: 'vulnerabilities/:id', component: VulnerabilityDetailComponent },
  { path: 'vulnerabilities/:id/edit', component: VulnerabilityFormComponent },
  { path: 'cwe-stats', component: CweStatsComponent },
  { path: 'cpe-ranking', component: CpeRankingComponent },
];
