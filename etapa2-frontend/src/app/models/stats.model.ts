export interface Stats {
  totalCves: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  cisaOnly: number;
  nucleiOnly: number;
  both: number;
  topCwe: string;
  topCweCount: number;
  topCpe: string;
  topCpeCount: number;
  topVendor: string;
  topVendorCount: number;
  lastAdded: string;
}
