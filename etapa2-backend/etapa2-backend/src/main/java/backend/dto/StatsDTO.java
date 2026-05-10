package backend.dto;

import lombok.Data;

@Data
public class StatsDTO {
    private long totalCves;
    private long critical;
    private long high;
    private long medium;
    private long low;
    private long cisaOnly;
    private long nucleiOnly;
    private long both;
    private String topCwe;
    private long topCweCount;
    private String topCpe;
    private long topCpeCount;
    private String topVendor;
    private long topVendorCount;
    private String lastAdded;
}
