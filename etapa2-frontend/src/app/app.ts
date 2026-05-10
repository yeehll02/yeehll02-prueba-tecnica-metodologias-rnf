import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top px-4" style="background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);">
      <span class="navbar-brand fw-bold fs-5 text-white">🛡 CVE Dashboard</span>
      <div class="navbar-nav ms-4">
        <a class="nav-link px-3" routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
        <a class="nav-link px-3" routerLink="/vulnerabilities" routerLinkActive="active">Vulnerabilidades</a>
        <a class="nav-link px-3" routerLink="/cwe-stats" routerLinkActive="active">CWE Stats</a>
        <a class="nav-link px-3" routerLink="/cpe-ranking" routerLinkActive="active">CPE Ranking</a>
      </div>
    </nav>
    <router-outlet />
  `,
  styles: [`
    .nav-link.active {
      color: #ffffff !important;
      border-bottom: 2px solid #00d4ff;
      font-weight: 600;
    }
    .nav-link {
      color: rgba(255,255,255,0.7) !important;
      transition: color 0.2s;
    }
    .nav-link:hover {
      color: #ffffff !important;
    }
  `]
})
export class App {}
